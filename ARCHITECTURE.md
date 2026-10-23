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

## QUALITY Engine (2026-10-21)

Módulo independiente `modules/quality`: control plane HTTP local + registry de proyectos + runner serializado + browser adapter Playwright + inference adapter Ollama + reparación en Git worktree. La UI principal enlaza `/quality` y recibe sólo la URL del motor por configuración; no se acopla a sus proveedores.

Contrato: proyecto registrado → copia de prueba → recorridos responsive y verificación del proyecto → evidencia → propuesta estructurada → cambios permitidos → repetición de pruebas → rama revisable. No se publica automáticamente. Modelo, contexto editable, pasos de negocio y runtime de cada app son configurables. DESIGN sigue gobernando identidad visual; QUALITY preserva esa identidad y verifica comportamiento/encuadre.

Ejecución local o Docker Compose, con estado y evidencia portables en disco. Primera versión serializada; la cola distribuida, descubrimiento autónomo, carga masiva y adapter ORCHESTRUM son evoluciones pendientes, no capacidades operativas actuales. Detalles: `modules/quality/README.md`.



## Conector audit-only — 22/10/2026
connector.py expone metadatos del registro administrado por operador y persiste conexiones idempotentes por ID. HTTP no acepta rutas ni comandos nuevos. attach_readonly permite auditar una preview loopback existente con entorno test/datos synthetic/permisos audit; API y runner rechazan reparar y Playwright bloquea escrituras. La identidad entre checkout y target es declarada, no atestada; el informe lo explicita. MVA Cloud integra por enlace a /arkitekta/?project=ID; proxy local sólo para preview. Gateway productivo y autorización de despliegue permanecen separados.
