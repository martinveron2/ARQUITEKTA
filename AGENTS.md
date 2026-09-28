# AGENTS.md

## PRINCIPIO 0 — MODULAR, ESCALABLE Y PORTABLE DESDE EL NACIMIENTO

Antes de cualquier cambio, preservar esta regla: todo proyecto, app, servicio, módulo o nueva funcionalidad debe diseñarse **MODULAR, ESCALABLE Y PORTABLE desde el primer día**.

- responsabilidades aisladas;
- contratos/interfaces claros;
- bajo acoplamiento;
- adapters/connectors para dependencias externas;
- frontend, backend, core, datos e infraestructura capaces de evolucionar sin rehacer todo el sistema;
- ninguna solución inmediata puede cerrar el crecimiento razonable futuro.

## PRINCIPIO 0 — MODULAR, ESCALABLE Y PORTABLE DESDE EL NACIMIENTO

**REGLA OBLIGATORIA Y PRIORITARIA:** todo proyecto, app, servicio, módulo o nueva funcionalidad del ecosistema MVA debe diseñarse **MODULAR, ESCALABLE Y PORTABLE desde el primer día**.

Esto no es una mejora futura ni una optimización opcional. Es una condición de diseño previa a implementar.

- cada responsabilidad importante debe poder aislarse en módulos claros;
- los módulos deben tener contratos/interfaces definidos y bajo acoplamiento;
- frontend, backend, core, datos, infraestructura e integraciones deben poder evolucionar sin rehacer todo el sistema;
- proveedores externos deben entrar mediante adapters/connectors reemplazables;
- agregar un nuevo mercado, proveedor, portal, IA, broker, cloud, worker o interfaz no debe obligar a reescribir el core;
- escalar significa permitir crecimiento por necesidad medida, sin introducir complejidad prematura;
- toda excepción debe quedar documentada y justificada.

**Regla de aceptación:** si una solución resuelve el problema inmediato pero bloquea la modularidad o el crecimiento razonable del proyecto, no cumple el estándar MVA.

ANTES DE MODIFICAR ESTE PROYECTO, LEER COMPLETAMENTE:

1. AGENTS.md
2. README.md
3. PROJECT_STATUS.md
4. ROADMAP.md
5. PROJECT_LEDGER.md
6. ARCHITECTURE.md
7. MVA-PROJECT-DESIGN

Fuente maestra:
https://github.com/martinveron2/MVA-PROJECT-DESIGN

## Reglas obligatorias

- arquitectura modular, escalable y portable
- cero botones muertos
- mocks claramente identificados
- no presentar estados falsos
- actualizar documentación con cambios sustanciales
- previews de desarrollo en Cloudflare temporal
- producción sólo tras aprobación
- proteger secretos
- probar antes de declarar DONE
- toda decisión persistente debe quedar en GitHub
- mantener ROADMAP, PROJECT_STATUS y PROJECT_LEDGER actualizados
- mantener infraestructura provider-neutral y un camino verificable de export / restore / migrate / rollback
- mantener screenshots actuales en docs/screenshots/
- toda app con UI debe embeber al menos una captura real en el README
- mobile: captura vertical centrada, referencia 190 px
- desktop/web: captura centrada, 700–900 px
- documentar estados del sistema en docs/SYSTEM_STATES.md
- documentar seguridad en docs/SECURITY_MODEL.md
- mantener GitHub Project sincronizado con ROADMAP

- toda app con UI debe mostrar al menos una captura real directamente en README.md
- screenshots mobile: verticales, centrados, 180–220 px; usar 190 px por defecto
- screenshots desktop/web: centrados, 700–900 px
- no insertar screenshots mobile a tamaño completo
