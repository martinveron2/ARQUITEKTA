# PROJECT LEDGER

## 2026-10-21 — QUALITY PORTABLE / PEDIDO DE MARTÍN
**Tipo:** IMPLEMENTATION CHECKPOINT
**Estado:** CODED / PARTIALLY TESTED / NOT DEPLOYED

Pedido: conservar diseño/marca en ARQUITEKTA y agregar un motor enchufable multiapp que pruebe frontend responsive y recorridos, encuentre fallos, repare con Ollama local y vuelva a verificar; portabilidad Docker, código bajo control MVA.

Implementación: `modules/quality` con dashboard propio, API local con token, registry de proyectos, runner serializado, eventos, Git worktree, scopes de reparación, adapter `/api/chat`, Chromium en 320/390/768/1440 px, recorridos con aserciones, evidencia, patch/commit en rama. Enlace `/quality` desde Inicio. Sin proveedor pago, sin activar GPU, sin publicar cambios ni tocar servidores de apps existentes.

Validación: 4 unit tests PASS; smoke existente 6 checks PASS; compilación Python y sintaxis JS PASS. El E2E de botón roto + overflow intentado localmente quedó BLOCKED por ausencia de Playwright Python/Chromium y registro inaccesible; no se presenta como aprobado. Docker tampoco está disponible. Se agrega workflow CI para prueba Chromium real con inferencia doble de prueba. Modelo real aún no conectado.

Próximo paso: comprobar CI, levantar worker en host de pruebas con Ollama disponible, registrar un checkout de app y sus recorridos, verificar ciclo real y pantalla. Carga masiva, navegación autónoma y evaluación estética completa permanecen en roadmap; no se declaran operativas.

## 2026-09-28 — FOUNDATION
**Tipo:** DECISION
**Estado:** ACTIVE
**Decisión:** el proyecto se llama ARQUITEKTA y será la fábrica/gobierno de aplicaciones basadas en MVA-PROJECT-DESIGN.

## 2026-09-28 — PRODUCT PRINCIPLE
**Tipo:** DECISION
**Estado:** ACTIVE
**Decisión:** mobile-first, con experiencia desktop responsive secundaria.

## 2026-09-28 — ARCHITECTURE
**Tipo:** DECISION
**Estado:** ACTIVE
**Decisión:** ARQUITEKTA gobierna; MVA-PROJECT-DESIGN controla estándar; MVA-PROJECT-TEMPLATE genera base; CORE UI/UX provee componentes; ORCHESTRUM orquesta agentes; GitHub conserva verdad persistente.

## 2026-09-28 — VISUAL
**Tipo:** APPROVAL
**Estado:** APPROVED
**Decisión:** imagen conceptual ARQUITEKTA aprobada para README y documentación.


## 2026-09-28 — DESIGN OWNERSHIP
**Tipo:** DECISION
**Estado:** ACTIVE
**Decisión:** la arquitectura maestra MVA permanece fija como estándar técnico, mientras la identidad visual pertenece al usuario y se implementa mediante un módulo DESIGN desacoplado.

## 2026-09-28 — DESIGN PROFILE
**Tipo:** DECISION
**Estado:** ACTIVE
**Decisión:** ARQUITEKTA podrá entrevistar al usuario, recibir referencias o mockups, proponer diseños y, tras aprobación humana, generar un Design Profile versionado y reutilizable entre futuras apps o familias de apps.

## 2026-09-28 — DESIGN ENGINES
**Tipo:** ARCHITECTURE
**Estado:** ACTIVE
**Decisión:** Reference Engine, Design Engine, Brand Engine, Layout Engine, Component Engine y Style Memory deben ser enchufables mediante adapters. Ningún motor de diseño podrá acoplar la arquitectura a un proveedor único.

**Regla de producto:** “La arquitectura es estándar. La identidad es tuya.”


## 2026-09-28 — APP BOOK / ORCHESTRUM — BACKEND MILESTONE 0A
**Tipo:** APP CHECKPOINT  
**Estado:** IN PROGRESS  
**Repo:** `martinveron2/ORCHESTRUM`  
**Rama de trabajo:** `feat/backend-milestone-0a`

**Estado humano:** ORCHESTRUM está en el punto de convertir su backend de runtime en durable sobre PostgreSQL. La arquitectura quedó congelada en V1 pequeña de infraestructura y grande de arquitectura: Postgres como cola durable inicial; Redis queda diferido hasta necesidad medida.

**Implementado y verificado localmente:**
- modelos SQLAlchemy para `tasks`, `subtasks`, `execution_runs`, `events`
- migración Alembic inicial
- claim concurrente sobre PostgreSQL con `FOR UPDATE SKIP LOCKED`
- reclaim por lease vencido
- fencing mediante `run_id`
- idempotency key estable por subtask/efecto
- reserva de presupuesto por run
- `finalize_success` / `finalize_failure`
- reaper mínimo para `MAX_ATTEMPTS_EXHAUSTED` y cancelaciones READY
- heartbeat sin inflar el event log
- `ExecutionPort` + `FakeExecutor`
- base de `QueuePort` durable
- PostgreSQL 16 real levantado en Docker para pruebas

**Evidencia verificada:**
- 4 tests de concurrencia contra PostgreSQL real: PASS
- dos workers no reclaman la misma subtask
- zombie worker queda FENCED tras reclaim
- reaper cierra lease agotado
- reservas concurrentes no superan budget
- Alembic `upgrade head` probado desde schema limpio

**Todavía NO está DONE:**
- suite completa pendiente de resultado verificable
- SSE pendiente
- flujo E2E `POST /tasks → claim → FakeExecutor → event → SSE` pendiente
- cambios locales del runtime durable aún no confirmados como commit/push al momento de este checkpoint
- CI de GitHub para este hito aún no verificado
- no hay proveedor real conectado todavía

**Próximo checkpoint:** cerrar Milestone 0A con SSE + E2E + suite completa + commit/push + CI verde.

**Detalle:** `docs/ledger/apps/2026/ORCHESTRUM-M0A-2026-09-28.md`


## 2026-09-28 — APP BOOK / ORCHESTRUM — PROTOCOLO DE CIERRE M0A
**Tipo:** CLOSURE CHECKPOINT  
**Estado:** IN PROGRESS / SAFE TO RESUME  
**Repo:** `martinveron2/ORCHESTRUM`  
**Rama:** `feat/backend-milestone-0a`  
**Draft PR:** #12

**Hecho:** durable PostgreSQL runtime foundation, Alembic, claim/reclaim, fencing, idempotencia, budget reservation, reaper, FakeExecutor y tests de concurrencia.

**Evidencia:** suite local **14 passed in 1.63s**; Alembic verificado desde schema PostgreSQL 16 limpio; draft PR #12 creado; issue #2 actualizado.

**Pendiente:** FastAPI durable path, SSE + Last-Event-ID, E2E POST→worker→event→SSE, CI verde verificado.

**Regla de cierre:** M0A NO está DONE. Retomar exactamente por SSE/API durable y cerrar E2E antes de agregar DAG, planner, Redis o proveedores reales.


## 2026-09-28 — APP BOOK / ORCHESTRUM — CI #144 NO VERDE
**Tipo:** CLOSURE PROBLEM  
**Estado:** OPEN

Tras el cierre de M0A, GitHub Actions run #144 terminó en FAILURE. Los jobs reportados no mostraron pasos ejecutados y runner_id = 0; Python 3.11 quedó cancelled y web/Python 3.12 en failure.

**Importante:** la evidencia local sigue siendo válida (14 tests PASS sobre PostgreSQL 16), pero ORCHESTRUM no puede declararse CI-green ni M0A DONE.

**Próximo paso:** diagnosticar/reintentar CI antes de cerrar el hito.

