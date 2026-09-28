# DEVELOPER GUIDE

## Regla principal
Agregar capacidades como módulos. Evitar lógica de proveedores en UI/core.

## Convenciones
- `src/components`: componentes UI reutilizables
- `src/modules`: módulos de producto
- `src/lib`: contratos/utilidades sin dependencia de UI
- `adapters`: proveedores externos
- `workers`: trabajos asíncronos
- `infrastructure`: despliegue portable y overrides por proveedor
- `core`: dominio compartido
