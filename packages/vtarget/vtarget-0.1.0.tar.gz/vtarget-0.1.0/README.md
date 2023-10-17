# vTarget package

## Descripción

Este es un paquete de Python correr los flujos generados con el módulo de Dataprep de vTarget.

## Instalación

Para instalar este paquete, puedes usar `pip`:

```
pip install vtarget
```

## Uso

Para usar este paquete, primero debes importarlo en tu script de Python:

```python
import vtarget
```

Luego, puedes usar la función `run_flow` para correr un flujo generado por vTarget. Por ejemplo:

```python
nodos = vtarget.run_flow("Flow.json")
print(nodos["v_output"]["Out"])
```

## Contribuir

Puedes informar errores o sugerir mejoras a través del siguiente [formulario](https://docs.google.com/forms/d/e/1FAIpQLSfYzPEQsbf-FTtrWpFbjRG2TX3ZrIgNtlMJLhOKteJrhZXUpg/viewform "Soporte vTarget").


## Licencia

Este proyecto está licenciado bajo la licencia BSD. Consulta el archivo `LICENSE` para obtener más información.
