'use client';
import { useState } from 'react';
import { moduleCatalog } from '@/lib/catalog';

type View = 'home'|'new'|'audit'|'modules';
const projects = [
  {name:'NovaShop',type:'E-commerce moderno',state:'Listo para producción',tone:'ok'},
  {name:'TerraMaps',type:'Plataforma de mapas',state:'En desarrollo',tone:'info'},
  {name:'Fintek',type:'App financiera',state:'En diseño',tone:'draft'}
];

export function AppShell(){
  const [view,setView]=useState<View>('home');
  return <main className="shell">
    <header className="topbar"><div className="brand"><span className="mark">A</span>RQUITEKTA</div><button className="avatar">MV</button></header>
    <section className="content">
      {view==='home' && <Home onNew={()=>setView('new')} onAudit={()=>setView('audit')} onModules={()=>setView('modules')} />}
      {view==='new' && <NewApp onBack={()=>setView('home')} />}
      {view==='audit' && <Audit onBack={()=>setView('home')} />}
      {view==='modules' && <Modules onBack={()=>setView('home')} />}
    </section>
    <nav className="bottomNav">
      <button className={view==='home'?'active':''} onClick={()=>setView('home')}>⌂<span>Inicio</span></button>
      <button onClick={()=>setView('home')}>▣<span>Proyectos</span></button>
      <button className={view==='modules'?'active':''} onClick={()=>setView('modules')}>◫<span>Módulos</span></button>
      <button className={view==='audit'?'active':''} onClick={()=>setView('audit')}>✓<span>Auditoría</span></button>
      <button>○<span>Perfil</span></button>
    </nav>
  </main>
}

function Home({onNew,onAudit,onModules}:{onNew:()=>void;onAudit:()=>void;onModules:()=>void}){
  return <>
    <div className="hero"><div><p className="eyebrow">Tu espacio de creación</p><h1>Inicio</h1></div><button className="primary" onClick={onNew}>+ Nueva app</button></div>
    <div className="stats"><Stat n="8" l="Proyectos"/><Stat n="3" l="En desarrollo"/><Stat n="2" l="En auditoría"/><Stat n="3" l="Listos"/></div>
    <SectionTitle title="Proyectos recientes" action="Ver todos" />
    <div className="projectList">{projects.map(p=><button className="project" key={p.name} onClick={onAudit}><div className="projectIcon">◇</div><div className="projectMain"><strong>{p.name}</strong><small>{p.type}</small></div><span className={'pill '+p.tone}>{p.state}</span></button>)}</div>
    <SectionTitle title="Módulos disponibles" action="Ver catálogo" onAction={onModules}/>
    <div className="moduleGrid">{moduleCatalog.map(m=><button className="moduleCard" key={m.id} onClick={onModules}><span className="moduleGlyph">◈</span><b>{m.name}</b><small>{m.group}</small></button>)}</div>
  </>
}
function NewApp({onBack}:{onBack:()=>void}){
 const [selected,setSelected]=useState(new Set(['auth','api','ai','storage','deployment']));
 const toggle=(id:string)=>setSelected(prev=>{const n=new Set(prev);n.has(id)?n.delete(id):n.add(id);return n});
 return <><SubHeader title="Nueva app" onBack={onBack}/><div className="steps"><b>1</b><span>Información</span><i/> <b>2</b><span>Producto</span><i/><b>3</b><span>Módulos</span><i/><b>4</b><span>Revisión</span></div>
 <section className="panel"><h2>Información básica</h2><label>Nombre de la app<input defaultValue="NovaFit"/></label><label>Objetivo<textarea defaultValue="Plataforma para entrenamiento personalizado con planes, rutinas y seguimiento."/></label><div className="choiceRow"><button className="choice active">App web</button><button className="choice">App móvil</button><button className="choice">SaaS</button><button className="choice">API</button></div></section>
 <section className="principle"><span>◈</span><div><b>Principio 0</b><strong>Modular y escalable desde el nacimiento.</strong><small>La arquitectura debe poder crecer sin reescribir el core.</small></div></section>
 <section className="panel"><h2>Seleccioná los módulos</h2><div className="toggleList">{moduleCatalog.map(m=><button key={m.id} onClick={()=>toggle(m.id)}><span>{m.name}</span><i className={selected.has(m.id)?'switch on':'switch'} /></button>)}</div></section>
 <div className="stickyActions"><button className="secondary" onClick={onBack}>Volver</button><button className="primary">Siguiente →</button></div></>
}
function Audit({onBack}:{onBack:()=>void}){return <><SubHeader title="Auditoría MVA" onBack={onBack}/><div className="auditHero"><div className="score">78%</div><div><h2>Cumplimiento MVA</h2><p>28 de 36 criterios implementados correctamente.</p></div></div><AuditBlock tone="green" title="Cumple" count="28" items={['Estructura modular','Gestión de entorno','Seguridad de autenticación']}/><AuditBlock tone="orange" title="Faltante" count="4" items={['Notificaciones','Pruebas automatizadas']}/><AuditBlock tone="red" title="Desactualizado" count="2" items={['Dependencias','Configuración de despliegue']}/><AuditBlock tone="purple" title="Riesgo" count="2" items={['Exposición potencial de claves','Permisos excesivos']}/><button className="fix">Corrección automática disponible · 3</button></>}
function Modules({onBack}:{onBack:()=>void}){return <><SubHeader title="Catálogo de módulos" onBack={onBack}/><p className="lead">Bloques reutilizables. Cada integración se conecta mediante contratos y adapters.</p><div className="moduleGrid wide">{moduleCatalog.map(m=><article className="moduleCard detailed" key={m.id}><span className="moduleGlyph">◈</span><b>{m.name}</b><small>{m.description}</small><em>{m.status==='ready'?'Base lista':'Planificado'}</em></article>)}</div></>}
function Stat({n,l}:{n:string;l:string}){return <div><b>{n}</b><span>{l}</span></div>}
function SectionTitle({title,action,onAction}:{title:string;action:string;onAction?:()=>void}){return <div className="sectionTitle"><h2>{title}</h2><button onClick={onAction}>{action} ›</button></div>}
function SubHeader({title,onBack}:{title:string;onBack:()=>void}){return <div className="subHeader"><button onClick={onBack}>←</button><h1>{title}</h1><span/></div>}
function AuditBlock({tone,title,count,items}:{tone:string;title:string;count:string;items:string[]}){return <section className={'auditBlock '+tone}><header><b>{title}</b><span>{count}</span></header>{items.map(i=><p key={i}>✓ {i}</p>)}</section>}
