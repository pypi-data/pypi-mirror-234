import numpy as np
import pandas as pd
import urllib
import json

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


# Database
class Database:
    def exec(self, flow_id, node_key, pin, settings):
        from sqlalchemy import create_engine, text
        import snowflake.connector
        from google.cloud import bigquery
        from google.oauth2 import service_account
        from pymongo import MongoClient

        script = []
        script.append("\n# DATABASE")

        host = settings["host"] if ("host" in settings and settings["host"] is not None) else None
        user = settings["user"] if ("user" in settings and settings["user"] is not None) else None
        password = ':'+settings["password"] if ("password" in settings and settings["password"] is not None) else ''
        port = ':'+str(settings["port"]) if ("port" in settings and settings["port"] is not None) else ''
        table = settings["table"] if ("table" in settings and settings["table"] is not None) else None
        database = settings["database"] if ("database" in settings and settings["database"] is not None) else None
        project = settings["project"] if ("project" in settings and settings["project"] is not None) else None
        query = settings["query"] if ("query" in settings and settings["query"] is not None) else None
        source = settings["source"] if ("source" in settings and settings["source"] is not None) else None

        if not source:
            msg = "(database) No existe el tipo de Base de Datos"
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        try:
            script.append("\n# DATABASE")

            # Debe ser uno de esos recursos, debe venir host, user y pass, y debe venir tabla y database o query
            if source == 'postgresql' or source == 'mysql' or source == 'sqlite' or source == 'oracle' or source == 'sqlserver' or source == 'mariadb':
                if not (host and user and database and (query or table)):
                    msg = "(database) Existen campos vacíos"
                    return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
                
                connection = self.get_url_connection(source, user, password, host, port, database)
                engine = create_engine(connection)
                df = pd.read_sql(text(query if query else f'SELECT * FROM {table}'), con=engine.connect())
                engine.dispose()

            elif source == "bigquery":
                if not (host and database and table and project):
                    msg = "(database) Existen campos vacíos"
                    return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
                
                with open(host) as file:
                    host = json.load(file)

                credentials = service_account.Credentials.from_service_account_info(host)
                client = bigquery.Client(credentials=credentials)
                table_ref = client.dataset(database, project=project).table(table)
                rows = client.list_rows(table_ref)
                df = rows.to_dataframe()
                client.close()

            elif source == "snowflake":
                if not (user and password and host and project and database):
                    msg = "(database) Existen campos vacíos"
                    return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
                
                connection = snowflake.connector.connect(user=user, password=password, account=host, database=project, schema=database)
                query = f'SELECT * FROM "{table}"'
                cursor = connection.cursor()
                cursor.execute(query)
                results = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                df = pd.DataFrame(results, columns=column_names)
                connection.close()
                cursor.close()

            elif source == "nosql_database":
                if not (host and database and table):
                    msg = "(database) Existen campos vacíos"
                    return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
                
                if source == "mongodb":
                    client = MongoClient(host)
                    db = client[database]
                    collection = db[table]
                    data = list(collection.find())
                    df = pd.DataFrame(data)
                    client.close()

            else:
                msg = "(database) El recurso de conexión, no coincide con ninguno"
                return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        except Exception as e:
            msg = "(database) Exception:" + str(e)
            return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": df},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        bug_handler.console(f'[Nodo]: "{node_key}" almacenado en cache', "info", flow_id)
        script_handler.script += script
        return {"Out": df}
    
    def get_url_connection(self, source, user, password, host, port, database):
        if source == 'sqlserver':
            quoted = urllib.parse.quote_plus('DRIVER={SQL Server};'+f'User={user};Password={password};Server={host};Port={port};Database={database}')    
            return 'mssql+pyodbc:///?odbc_connect={}'.format(quoted)
        elif source == 'mysql':
            return f"mysql+pymysql://{user}{password}@{host}{port}/{database}"
        elif source == 'postgresql':
            return f"postgresql://{user}{password}@{host}{port}/{database}"