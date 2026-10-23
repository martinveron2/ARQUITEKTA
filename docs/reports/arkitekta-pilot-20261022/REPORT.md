# Piloto ARKITECTA ↔ MVA Cloud ↔ AEROVIGÍA — 22/10/2026
Estado: integración privada verificada; auditoría AEROVIGÍA con fallos. Sin publicación ni reparaciones.

## Alcance comprobado
- Se continuó `feat/quality-ollama-portable-20261021`, commit a897043, sin reconstruir el motor.
- Registro persistente por ID preconfigurado: repositorio, URL, tecnología, entorno y permisos. No acepta comandos por HTTP.
- MVA Cloud: botón en rama aislada; preview loopback 18788 → módulo loopback 18787.
- Navegador real: botón de MVA Cloud → ARKITECTA → conectar AEROVIGÍA → ver informe → abrir captura. Sin overflow del dashboard a 390 y 1440 px.
- API: conexión 200; auditoría 202; reparación de proyecto audit-only rechazada 400.
- Suite: 10 tests PASS, incluido Chromium real y reparación del fixture en worktree con inferencia simulada. No prueba Ollama real.
- Primera auditoría por API: 12 combinaciones, 3 recorridos × 4 viewports (320, 390, 768, 1440), 12 PNG y 12 trazas ZIP.
- Evidencia completa de la ejecución: `evidence/`. Pruebas: `tests.log`. Capturas de integración: `screenshots/`.

## Resultado real del piloto
Run: `20261023-024433-b86bbe42` (ID UTC; fecha local 22/10).
Estado del motor: FAIL. 47 señales, no 47 defectos independientes:
- 32 señales de runtime repetidas. Tres endpoints devolvieron HTTP 401:
  `/v1/operations/dashboard`, `/v1/operations/triage`, `/v1/automation/mail-activity`.
- 8 aserciones fallidas: inicio y lectura en las cuatro resoluciones, dependientes del acceso QA.
- 7 señales de controles cubiertos: candidatas a revisión manual; no se aplicó reparación basándose sólo en geometría.
- La navegación de las pestañas de consulta del día/total pasó en los cuatro tamaños. Esto no valida consultas de datos ni IA.

Reproducción del bloqueo: abrir la preview QA, cargar Inicio o Solicitudes; aparece “Iniciá sesión desde Configuración” y las peticiones anteriores responden 401. Ver cada PNG, traza y pasos de `report.json`.
Diagnóstico respaldado: acceso a la fuente de ensayo no autorizado. Una sesión inválida o vencida es una hipótesis; no se comprobó cuál es la causa.
Propuesta: verificar y renovar únicamente la identidad/sesión de ensayo del proxy QA, comprobar sus permisos de lectura y repetir los mismos recorridos. No cambiar autenticación productiva ni ocultar los 401.

## No verificado / pendiente
- Extracción del correo ficticio y semáforo con backend sano: bloqueados por 401.
- Circuito completo MR → RFQ → PO → Follow Up: no ejecutado en este piloto.
- Recorridos autónomos de todas las rutas, formularios y regresión de toda la aplicación: pendiente; cobertura declarativa.
- Diagnóstico con Ollama real, autorización por hallazgo, IGNORAR y validación manual persistente: pendientes.
- Reparación productiva, publicación y rollback real: no ejecutados.
- Integración pública: requiere gateway HTTPS autenticado y aprobación independiente. El script de preview no es un servicio productivo.
- Appium/dispositivos físicos: no disponibles; Chromium con viewports es emulación.

## Preservación y seguridad
No se modificaron fuentes, registros, correo, órdenes ni contenedores productivos de AEROVIGÍA.
La preview existente sólo admite lectura y el navegador también bloquea métodos distintos de GET/HEAD/OPTIONS.
Se conservaron cambios ajenos de otras QA. Modelo y pruebas de reparación continúan en worktree.
JSON redacta claves sensibles comunes y Bearer; esto no garantiza sanear imágenes/trazas ni cualquier secreto libre. Usar sólo datos de ensayo y proteger el directorio completo.
El primer ensayo exploratorio tuvo falsos positivos de sidebar/modal y un selector ambiguo: se corrigió el auditor y se repitió por API. No se contó como evidencia final.

## Próximo paso exacto
Restablecer acceso QA de sólo lectura y repetir el piloto; después revisar autorización y gateway para publicar el módulo.
