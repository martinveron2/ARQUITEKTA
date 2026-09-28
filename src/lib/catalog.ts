export type ModuleDefinition = { id: string; name: string; group: string; status: 'ready'|'planned'; description: string };
export const moduleCatalog: ModuleDefinition[] = [
  ['core-ui','Core UI/UX','Foundation','planned','Sistema visual y componentes reutilizables'],
  ['orchestrum','ORCHESTRUM','Intelligence','planned','Orquestación multi-agente'],
  ['auth','Auth','Platform','ready','Identidad y autorización'],
  ['database','Database','Platform','ready','Persistencia de datos'],
  ['api','API','Platform','ready','Contratos y gateway'],
  ['ai','AI','Intelligence','ready','Capacidades de IA por adapters'],
  ['jobs','Jobs/Workers','Runtime','ready','Procesamiento asíncrono'],
  ['payments','Payments','Business','planned','Pagos desacoplados'],
  ['maps','Maps','Business','planned','Geolocalización y mapas'],
  ['notifications','Notifications','Platform','ready','Push/email/in-app'],
  ['storage','Storage','Platform','ready','Archivos y objetos'],
  ['analytics','Analytics','Operations','planned','Eventos y producto'],
  ['deployment','Deployment','Operations','ready','Deploy verificable'],
  ['portability','Portability','Operations','ready','Export/restore/cutover'],
  ['ledger','Ledger','Governance','ready','Memoria operativa persistente'],
  ['backup','Backup/Restore','Operations','ready','Recuperación y reversibilidad']
].map(([id,name,group,status,description]) => ({id,name,group,status: status as 'ready'|'planned',description}));
