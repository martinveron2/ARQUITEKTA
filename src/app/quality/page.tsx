export default function QualityPage() {
  const engine = process.env.NEXT_PUBLIC_QUALITY_URL;
  const validEngine = engine && /^https?:\/\//.test(engine);
  return <main className="shell"><section className="content">
    <a href="/">← ARQUITEKTA</a>
    <p className="eyebrow">Módulo portable · QUALITY</p>
    <h1>Probar y reparar</h1>
    <p className="lead">Elegí una aplicación, ejecutá sus recorridos en móvil y escritorio y revisá los cambios que propone Ollama. El motor conserva capturas y prueba cada reparación en una rama.</p>
    <section className="panel"><h2>Motor de pruebas</h2>
      {validEngine ? <a className="primary" href={engine} target="_blank" rel="noopener noreferrer">Abrir centro de pruebas ↗</a> : <p>El motor todavía no está conectado a esta instalación. Configurá su dirección para habilitar el acceso. No hay pruebas ejecutándose desde esta pantalla.</p>}
      <p>Se comprueban recorridos configurados y tamaños de pantalla. Las reparaciones quedan listas para revisar; la publicación es un paso separado.</p>
    </section>
    <section className="panel"><h2>Qué vas a ver</h2><ol>
      <li>Aplicaciones registradas y ejecución en progreso.</li>
      <li>Botones fuera de pantalla, controles tapados y recorridos que fallan.</li>
      <li>Propuesta de reparación y resultado de repetir las pruebas.</li>
      <li>Rama con los cambios y evidencia para revisión.</li>
    </ol></section>
  </section></main>;
}
