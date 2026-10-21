# ROADMAP — ARQUITEKTA

## Fase 0 — Semillero ✅ — Issue #1
- [x] Principio 0
- [x] estructura modular
- [x] documentación MVA mínima
- [x] imagen conceptual aprobada
- [x] frontend mobile-first inicial
- [x] smoke test y auditor MVA local
- [x] repositorio GitHub creado y enlazado
- [x] GitHub Project canónico creado

## Fase 1 — MVP CREATE — Issue #2
- [ ] wizard completo Nueva App
- [ ] especificación de producto persistente
- [ ] selector de módulos
- [ ] generación desde MVA-PROJECT-TEMPLATE
- [ ] creación automática de repo GitHub
- [ ] generación README/AGENTS/ROADMAP/STATUS/LEDGER/ARCHITECTURE/LICENSE

## Fase 2 — MVP AUDIT — Issue #3
- [ ] conectar repo existente
- [ ] comparar contra MVA-PROJECT-DESIGN
- [ ] estados Cumple/Faltante/Desactualizado/Riesgo
- [ ] correcciones automáticas revisables
- [ ] evidencia por criterio

## Fase 3 — DESIGN ENGINE + CORE UI/UX — Issue #4
- [ ] entrevista visual y captura de preferencias
- [ ] intake de referencias, screenshots, links, logos y mockups
- [ ] generación de propuestas visuales
- [ ] aprobación humana de mockup
- [ ] Design Profile versionado
- [ ] modos Clone style / Family / Fresh / Reference mix
- [ ] App Family
- [ ] registry de componentes
- [ ] themes/tokens
- [ ] presets mobile/web
- [ ] screenshots automáticos
- [ ] adapters reemplazables para motores de diseño

## Fase 4 — ORCHESTRUM — Issue #5
- [ ] adapter estable
- [ ] routing de tareas por capacidad/costo
- [ ] Codex / Claude / Gemini / otros
- [ ] human-in-the-loop antes de acciones sensibles

## Fase 5 — Portabilidad — Issue #6
- [ ] baseline portable
- [ ] deploy adapters Vercel/AWS/GCP/Azure/local
- [ ] export/restore verificable
- [ ] rollback/cutover

## Fase 6 — Producción — Issue #7
- [ ] auth
- [ ] secretos
- [ ] observabilidad
- [ ] backups
- [ ] CI/CD
- [ ] auditoría final MVA
- [ ] aprobación explícita

## QUALITY Engine — 2026-10-21

| ID | Módulo | Prioridad / etapa | Estado | Aceptación / evidencia | Dependencia / próximo paso |
|---|---|---|---|---|---|
| QA-01 | core/adapters | P1 NOW | Codificado; unit tests locales pasan | Worktree aislado, scope de fuentes, JSON Ollama y propuestas exactas | Ejecutar E2E Chromium en CI |
| QA-02 | frontend/backend | P1 NOW | Codificado | Dashboard con token, selección, ejecutar, progreso y capturas; `/quality` integrado | Prueba visual real del dashboard y conexión de instancia |
| QA-03 | browser/QA | P1 NOW | Codificado; ejecución local bloqueada | Botón roto + overflow en fixture; reparación y verificación conservando original | Navegador/dependencias no disponibles en este host; workflow dedicado |
| QA-04 | integración | P1 NEXT | No iniciado | Un proyecto MVA real y Ollama local producen evidencia antes/después | Registrar checkout, modelo, runtime y recorridos |
| QA-05 | infra | P2 NEXT | Compose codificado; no ejecutado | Build y arranque Docker con volúmenes en otro host | Docker no disponible en este host |
| QA-06 | visual/accesibilidad | P2 LATER | No iniciado | Referencias Design Profile, revisión estética y axe | Contrato visual y motor de visión verificados |
| QA-07 | performance/core | P2 SCALE | No iniciado | Carga gradual, límites medidos y workers distribuidos | Recursos medidos y adapter ORCHESTRUM |

No declarar el módulo operativo globalmente hasta QA-03/04/05 con evidencia real. Hito versión 0.2: conectar un proyecto y verificar un ciclo con Ollama, sin merge/deploy automático.

