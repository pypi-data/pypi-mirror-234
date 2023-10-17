import pandas as pd
import numpy as np
import urllib
import json

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


# Database Write
class DatabaseWrite:
    def exec(self, flow_id, node_key, pin, settings):
        # import snowflake.connector
        # from google.cloud import bigquery
        # from google.oauth2 import service_account
        # from pymongo import MongoClient
        from sqlalchemy import create_engine

        df: pd.DataFrame = pin["In"].copy()
        script = []
        script.append("\n# DATABASE WRITE")

        if_exist = settings["if_exist"] if ("if_exist" in settings and settings["if_exist"] is not None) else ''
        host = settings["host"] if ("host" in settings and settings["host"] is not None) else None
        password = ':'+settings["password"] if ("password" in settings and settings["password"] is not None) else ''
        port = ':'+str(settings["port"]) if ("port" in settings and settings["port"] is not None) else ''
        user = settings["user"] if ("user" in settings and settings["user"] is not None) else None
        project = ( settings["project"] if ("project" in settings and settings["project"] is not None) else None)
        database = ( settings["database"] if ("database" in settings and settings["database"] is not None) else None)
        table = (settings["table"] if ("table" in settings and settings["table"] is not None) else None)
        source = ( settings["source"] if ("source" in settings and settings["source"] is not None) else None )
        # type_connection = ( settings["type_connection"] if ("type_connection" in settings and settings["type_connection"] is not None) else None )

        # # Validación principal
        # if not type_connection or not source:
        #     msg = "(database_write) Existen campos vacíos"
        #     return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        # if type_connection == "sql_database" and (
        #     not host or not user or not password or not database or not table
        # ):
        #     msg = "(database_write) Existen campos vacíos"
        #     return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        # if type_connection == "cloud_database":
        #     if source == "bigquery" and (not host or not project or not database or not table):
        #         msg = "(database_write) Existen campos vacíos"
        #         return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
        #     elif source == "snowflake" and (
        #         not host or not user or not password or not project or not database
        #     ):
        #         msg = "(database_write) Existen campos vacíos"
        #         return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        # if type_connection == "nosql_database" and (not host or not database or not table):
        #     msg = "(database_write) Existen campos vacíos"
        #     return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        try:
            script.append("\n# DATABASE WRITE")
            if source == 'postgresql' or source == 'mysql' or source == 'sqlite' or source == 'oracle' or source == 'sqlserver' or source == 'mariadb':
                # Se validan los campos de entrada
                if not host or not user or not source or not database or not table or not if_exist:
                    msg = '(database_write) Existen campos vacíos'
                    return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
                
                connection = self.get_url_connection(source, user, password, host, port, database)
                engine = create_engine(connection)
                df.to_sql(name=table, con=engine, if_exists=if_exist, index=False)
                engine.dispose()

            # elif source == "sqlserver_2000":
            #     # ['SQL Server', 'SQL Server Native Client 11.0', 'ODBC Driver 17 for SQL Server']
            #     connection = pyodbc.connect(
            #         "DRIVER={SQL Server};"
            #         + f"User={user};Password={password};Database={database};Server={host};Port={port};"
            #     )
            #     df.to_sql(schema=database, name=table, con=connection, if_exists=if_exist, index=False)
            #     connection.close()

            # elif source == "bigquery":
            #     with open(host) as file:
            #         host = json.load(file)
            #     credentials = service_account.Credentials.from_service_account_info(host)
            #     client = bigquery.Client(credentials=credentials)
            #     table_ref = client.dataset(database, project=project).table(table)
            #     rows = client.list_rows(table_ref)
            #     df = rows.to_dataframe()
            #     client.close()

            # elif source == "snowflake":
            #     connection = snowflake.connector.connect(
            #         user=user,
            #         password=password,
            #         account=host,
            #         database=project,
            #         schema=database,
            #     )

            #     query = f'SELECT * FROM "{table}"'
            #     cursor = connection.cursor()
            #     cursor.execute(query)
            #     results = cursor.fetchall()
            #     column_names = [desc[0] for desc in cursor.description]
            #     df = pd.DataFrame(results, columns=column_names)
            #     connection.close()
            #     cursor.close()

            # elif source == "mongodb":
            #     client = MongoClient(host)
            #     db = client[database]
            #     collection = db[table]
            #     data = list(collection.find())
            #     df = pd.DataFrame(data)
            #     client.close()
            else:
                msg = "(database_write) El tipo de conexión no coincide con ninguno"
                return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        except Exception as e:
            msg = "(database_write) Exception:" + str(e)
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