# MVA EXPERIENCE STANDARD — UX/UI transversal

Estado: ESPECIFICADO, PENDIENTE DE IMPLEMENTACIÓN Y VALIDACIÓN.
Propietario: ARQUITEKTA DESIGN + CORE UI/UX. Fuente normativa visual: MVA-PROJECT-DESIGN/MASTER_UI_RULES.md.
Alcance: Aerovigía, Arquitecta y cualquier aplicación presente o futura del ecosistema MVA.

## Propósito
**SIMPLE OUTSIDE. POWERFUL INSIDE.** Una aplicación debe hacer comprensible su complejidad, orientar a la persona hacia la siguiente acción y generar una experiencia satisfactoria, sin manipular su atención ni sacrificar velocidad operativa.

Este estándar complementa (no reemplaza) DESIGN_ENGINE.md: el Design Profile gobierna identidad y expresión; el Experience Profile gobierna comprensión, interacción, flujos y eficacia. La identidad visual puede variar por aplicación, pero los requisitos de usabilidad, accesibilidad y evidencia son comunes.

## Experience Profile portable
Guardar por producto un perfil versionado y legible por máquina, con:
- Personas, responsabilidades, permisos, objetivos y tareas prioritarias.
- Arquitectura de información y navegación por tarea.
- Top 5 recorridos críticos: disparador, contexto, acción, estados, confirmación, recuperación, éxito.
- Jerarquía de información: qué pasó, qué requiere atención y qué hago ahora.
- Patrones compartidos: navegación, formularios, buscador, tablas progresivas, filtros, confirmaciones, feedback.
- Estados reales: vacío, loading, error, éxito, offline, permiso denegado, datos parciales.
- Responsive: móvil, tablet y escritorio; targets táctiles y cero overflow accidental.
- Accesibilidad: teclado, foco visible, contraste, etiquetas semánticas, no depender solo del color, reduced motion.
- Microinteracciones que informen, nunca bloqueen ni distraigan del objetivo.
- Design Profile asociado y excepciones justificadas.
- Métricas y umbrales aceptados por tarea; versión, revisión y aprobador.

## Módulo UX EXPERIENCE AUDITOR — enchufable
Contrato conceptual:
`analyze(appUrl, repository, experienceProfile, testEnvironment) -> findings[]`
`propose(findings, constraints) -> changePlan`
`validate(changePlan, baseline) -> evidence + regressionResults`

Por cada hallazgo: ID, escenario, severidad, reproducción, captura/video, logs pertinentes, causa probable, propuesta, riesgo, prueba antes/después y resultado.

Inspeccionar navegación, desbordamientos, botones muertos, formularios, errores, estados vacíos, rendimiento percibido, accesibilidad, coherencia, tareas completables y regresiones. Usar Playwright para rutas y comparaciones visuales cuando esté disponible; complementarlo con revisión experta. Los modelos locales (p. ej. Ollama) pueden clasificar o proponer, pero no sustituyen evidencia reproducible.

## Flujo
1. Conectar aplicación y repositorio autorizados; establecer baseline real.
2. Identificar persona y tareas, observar flujos existentes y levantar fallos.
3. Proponer mapa de navegación y Experience Profile; obtener aprobación para cambios significativos.
4. Implementar cambios pequeños, reversibles y aislados.
5. Ejecutar pruebas desktop/móvil + accesibilidad + regresión funcional; aportar capturas reales.
6. Registrar evidencia, problemas pendientes, rollback, cambios de archivos y actualizar PROJECT_STATUS, ROADMAP y PROJECT_LEDGER.
7. Solicitar aprobación explícita antes de producción, permisos sensibles o acciones irreversibles.

## Criterios mínimos de aceptación
- Primer uso: se comprende finalidad, situación actual y siguiente acción sin tutorial obligatorio.
- Cada pantalla tiene un propósito claro y una acción principal reconocible.
- Ningún elemento aparenta ser interactivo si no funciona.
- Flujos críticos funcionan con datos reales o entorno de prueba claramente identificado.
- No hay desbordamientos ni controles inaccesibles en viewports objetivo.
- Un error dice qué ocurrió y cómo recuperar la tarea, sin perder el trabajo.
- Los estados operativos son legibles también sin color.
- Se conservan datos, API, autenticación, historial y lógica de negocio.
- Pruebas y evidencias están asociadas a cada criterio; sin evidencia no hay DONE.

## Piloto: Aerovigía
Dashboard inicial con: ¿qué pasó mientras no estaba?, ¿qué requiere atención?, ¿cuál es la próxima acción?
Tareas: detectar solicitud por Gmail → validar MR/matrícula/P/N/cantidad → RFQ supervisada → comparar cotizaciones → PO/seguimiento.
Prioridades visibles con texto: AOG / Critical / Normal. Catálogos amplios detrás de búsqueda, filtros y vistas avanzadas. No enviar correos ni PO sin la autorización requerida.

## Separación de responsabilidades
- MVA-PROJECT-DESIGN: estándar transversal.
- ARQUITEKTA DESIGN: Design Profile + Experience Profile.
- ARQUITEKTA AUDIT: diagnósticos, hallazgos y verificación.
- Motor de reparación futuro: cambios propuestos, pruebas y validación humana cuando corresponda.

**Estado de este documento:** especificación creada. No implica que el módulo esté programado, conectado, probado ni desplegado.
