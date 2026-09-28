# AGENTS.md

## PRINCIPIO 0 — MODULAR Y ESCALABLE DESDE EL NACIMIENTO

Antes de modificar ARQUITEKTA, preservar siempre esta regla: cada módulo debe tener responsabilidad clara, contratos definidos, bajo acoplamiento y dependencias externas aisladas mediante adapters/connectors. Ninguna solución inmediata puede bloquear el crecimiento razonable futuro.

## Lectura obligatoria
1. AGENTS.md
2. README.md
3. PROJECT_STATUS.md
4. ROADMAP.md
5. ARCHITECTURE.md
6. PROJECT_LEDGER.md
7. MVA-PROJECT-DESIGN

Fuente maestra: https://github.com/martinveron2/MVA-PROJECT-DESIGN

## Reglas
- mobile-first; desktop responsive secundario
- cero botones muertos en producción
- mocks claramente identificados
- GitHub es la fuente persistente de verdad
- no declarar DONE sin implementar + probar + documentar + verificar
- cambios de arquitectura requieren actualización de ARCHITECTURE.md
- toda integración externa entra por adapters/connectors
- conservar portabilidad y estrategia de salida de proveedor
- producción sólo después de aprobación explícita
