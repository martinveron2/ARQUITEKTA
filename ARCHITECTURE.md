# ARCHITECTURE

## Principio 0
MODULAR · ESCALABLE · REEMPLAZABLE · OBSERVABLE · TESTEABLE · PORTABLE · DOCUMENTADO · AUDITABLE

## Flujo maestro
ARQUITEKTA → MVA-PROJECT-DESIGN → MVA-PROJECT-TEMPLATE → CORE UI/UX → ORCHESTRUM → AGENTES IA → GITHUB

GitHub es la fuente persistente de verdad.

## Capas
UI/PWA → API/Gateway → Application/Orchestration → Domain/Core → Workers/Engines → Adapters/Connectors → Data/Storage

Transversal: Security · Observability · Logging · Config · Testing · Ledger · Portability.

## Módulos iniciales
- project-catalog: proyectos y estados
- app-builder: wizard de creación
- module-catalog: catálogo enchufable
- mva-audit: cumplimiento y correcciones
- orchestrum-adapter: selección/orquestación de agentes
- github-adapter: persistencia de repositorios y evidencia
- portability: export/restore/cutover/rollback
- ledger: memoria operativa del proyecto

## Fronteras
La UI nunca conoce proveedores específicos. El core nunca depende directamente de GitHub, Vercel, AWS, GCP, Azure ni un proveedor de IA. Todo proveedor se implementa como adapter.


## Separación CORE ↔ DESIGN

ARQUITEKTA mantiene una frontera explícita entre arquitectura e identidad visual.

- **CORE** conserva la arquitectura maestra MVA y sus garantías técnicas.
- **DESIGN** transforma preferencias, referencias y mockups aprobados en un Design Profile reutilizable.
- El diseño puede cambiar sin reescribir el core.
- Un proveedor, framework visual o agente puede reemplazarse mediante adapters sin perder el Design Profile.

Directiva completa: `docs/DESIGN_ENGINE.md`.

**Regla:** la arquitectura es estándar; la identidad es del usuario.
