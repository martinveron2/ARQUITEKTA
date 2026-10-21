# ARQUITEKTA QUALITY — Probar y reparar

Motor enchufable, independiente del frontend de ARQUITEKTA. Conserva DESIGN / Design Profile; suma pruebas de uso y reparación de código con inferencia local. Una sola instalación admite múltiples aplicaciones mediante un registro de proyectos.

## Estado real

Implementación inicial: dashboard HTTP con token, registry local, ejecuciones serializadas, eventos persistidos, Chromium en 4 viewports, recorridos declarativos, evidencia, adapter Ollama `/api/chat`, reparación limitada en worktree Git, repetición de las mismas pruebas, diff y commit aislado. No hace push, merge ni despliegue.

No es una certificación total. No incluye todavía descubrimiento autónomo de todas las pantallas, medición de carga masiva, acceso a Safari/iOS real, evaluación visual estética autónoma, axe completo, gestor distribuido de workers, ni sincronización con ORCHESTRUM. La configuración inicial de cada app es necesaria. Una prueba que no pudo ejecutarse queda BLOCKED, nunca aprobada.

Evidencia inicial de CI: [Chromium + reparación del fixture, 5 tests PASS](https://github.com/martinveron2/ARQUITEKTA/actions/runs/39696777490). La inferencia de esa prueba es un doble determinista; no valida un modelo Ollama real.

## Instalación local

Requiere Python 3.11+, Git y el runtime de cada aplicación. Usar checkouts de prueba con bases y credenciales de prueba; la reparación no se ejecuta dentro del checkout que sirve producción.

```bash
cd modules/quality
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m playwright install --with-deps chromium
cp projects.example.json projects.json
# Editar repo, start, verify, editable_files y journeys para cada app.
export QUALITY_TOKEN="un-token-local-largo-y-aleatorio"
export OLLAMA_URL="http://127.0.0.1:11434"
export OLLAMA_MODEL="nombre-exacto-del-modelo-local-instalado"
python -m arquitekta_quality.server
```

Abrir `http://127.0.0.1:8787`, ingresar el token y conectar. Elegir proyecto y **Probar aplicación** o **Probar y reparar con Ollama**. El token permanece sólo en memoria de la página. No compartir el puerto públicamente; para acceso remoto usar túnel SSH o proxy autenticado administrado por MVA.

El adapter no descarga modelos ni activa servidores GPU. Usar un modelo de código disponible en Ollama; definir `OLLAMA_VISION=1` sólo cuando ese modelo admite imágenes. En ese modo recibe hasta 3 capturas además de hallazgos y fuentes. La ausencia de Ollama no impide el modo de pruebas, pero bloquea reparación si se necesita. No hay API paga ni fallback remoto.

## Docker portable

```bash
export QUALITY_PROJECTS_DIR="/ruta/absoluta/a/checkouts-de-prueba"
# Cada repo de projects.json debe apuntar a /projects/nombre.
# QUALITY_TOKEN y OLLAMA_MODEL deben estar definidos como arriba.
docker compose up --build
```

Incluye Chromium, Python, Node 22, npm y Git. Otros runtimes se agregan en una imagen derivada. No montar Docker socket, SSH agent, directorio personal ni repos de producción. El contenedor se usa para ejecutar código de proyectos propios, no como sandbox de código hostil. El puerto sólo se publica en localhost. Ollama existente se conecta por `host.docker.internal`; URL configurable para Linux, VPS o redes Docker.

Para migrar: guardar `projects.json`, `quality-data`, los checkouts y las ramas Git; conservar rutas internas `/projects` y `/data`. Si cambia una ruta de worktree, ejecutar `git worktree repair` en el repo correspondiente. Los modelos se administran en Ollama por separado. Las capturas/trazas y logs contienen datos de prueba y deben protegerse igual que sus fuentes.

## Contrato de proyecto

- `id`, `name`, `repo`: checkout Git limpio, rutas locales del host o contenedor.
- `base_url`: exclusivamente `http://127.0.0.1:puerto/` (o localhost). El motor levanta y detiene esa copia; bloquea un puerto ocupado para no confundir versiones.
- `prepare`: argv opcional, por ejemplo `["npm", "ci"]`. Ejecutado en cada evaluación; puede requerir acceso a un registro.
- `start`: argv para iniciar la app en el puerto configurado. Debe ejecutar el proceso en primer plano.
- `verify`: argv obligatorio para tests/build del proyecto. Se ejecuta tras cerrar el servidor. Un error bloquea la aprobación.
- `editable_files`: lista explícita de fuentes editables, hasta 30 archivos / 160k caracteres. Tests, secretos, configuración de CI y archivos de dependencias quedan fuera.
- `journeys`: escenarios nombrados con `steps`; cada uno debe contener una aserción `expect_*`.
- `max_attempts`: de 1 a 3; por defecto 2. Ejecuciones serializadas para no saturar Ollama.

Acciones: `goto` con `path`, `fill` con `selector/value`, `click` con `selector`, `expect_text` con `selector/value`, `expect_visible` con `selector`, `reload`. Selectores estables como `data-testid` son recomendables. Login, persistencia, roles y formularios necesitan recorridos explícitos. Nunca se hace clic indiscriminadamente en pagos, envíos o eliminaciones. Los pedidos de navegador fuera del origen local se bloquean: simular integraciones en el backend de prueba o usar endpoints del mismo origen. El bloqueo de navegador no limita las conexiones del proceso backend: configurar sus servicios de ensayo.

## Estados y aprobación

`PREPARING → TESTING → ANALYZING → REPAIRING → VERIFYING`.

- `PASS_CONFIGURED_CHECKS`: pasan únicamente las comprobaciones configuradas.
- `REPAIRED_CONFIGURED_CHECKS`: se produjo un cambio que pasa esas comprobaciones; queda en rama `quality/<run>` con `repair.patch`, sin tocar la rama original.
- `FAIL`: persisten defectos o se solicitó sólo diagnóstico.
- `BLOCKED`: falta runtime, navegador, Ollama, contexto, puerto disponible o configuración; no equivale a un fallo de la aplicación.

El modelo no puede cambiar los criterios ni los tests para fabricar un PASS. Las propuestas usan reemplazos exactos únicos, lista de archivos permitidos y validación de symlinks/rutas. La publicación de la app sigue el gate humano del proyecto MVA. Para revisar o retirar una ejecución usar `git worktree list`, conservar el patch y, sólo tras revisarlo, aplicar/cherry-pick el commit. No eliminar worktrees con trabajo pendiente.

## API de control

Token `Authorization: Bearer …` en todos los endpoints `/api/*`.

- `GET /api/projects`: proyectos registrados (sin comandos ni fuentes).
- `POST /api/runs`: `{"project":"example","mode":"test"}` o `repair`; devuelve 202 o 409 si hay un trabajo activo.
- `GET /api/runs`: últimos 100 informes con eventos y resultados.
- `GET /api/evidence/<run>/before/mobile-0.png`: captura autenticada.

Registro operado desde archivo local, sin permitir comandos/rutas arbitrarios por HTTP. Al reiniciar, trabajos incompletos se marcan BLOCKED para evitar aprobaciones obsoletas. Traces ZIP, logs, propuestas y patches permanecen en disco para revisión local.

## Conexión con ARQUITEKTA

Página `/quality` y acceso desde Inicio. Configurar `NEXT_PUBLIC_QUALITY_URL` con la URL del motor accesible desde el navegador del operador. Sin URL aparece el estado desconectado explícito. La UI principal no conoce Ollama, Git ni Docker: sólo enlaza el control plane portable.

## Pruebas

```bash
python -m unittest discover -s tests -p test_engine.py -v
python -m unittest discover -s tests -p test_browser_repair.py -v
```

La primera suite prueba confinamiento de archivos, propuestas atómicas y protocolo HTTP de Ollama con un servidor doble. La segunda usa Chromium real y una app con botón roto y overflow responsive, verifica reparación en worktree y preservación del original; la inferencia es un doble determinista, no un modelo real. Documentar por separado toda ejecución con Ollama real y cada proyecto conectado.
