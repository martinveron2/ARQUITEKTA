# ARQUITEKTA

> **La base de diseño de tu futura app.**

ARQUITEKTA crea, audita y gobierna proyectos reales bajo el estándar MVA. No reemplaza a los agentes de IA: define la arquitectura, aplica las reglas, selecciona módulos y conserva evidencia para que los agentes construyan dentro de una base consistente.

<p align="center">
  <img src="docs/screenshots/arquitekta-concept.webp" alt="ARQUITEKTA concept — mobile-first app factory" width="900" />
</p>

## PRINCIPIO 0
Todo proyecto nace **modular y escalable desde el primer día**. Una solución que resuelve el presente pero bloquea el crecimiento razonable futuro no cumple el estándar MVA.

## Flujo maestro

```text
ARQUITEKTA
  ↓
MVA-PROJECT-DESIGN
  ↓
MVA-PROJECT-TEMPLATE
  ↓
CORE UI/UX
  ↓
ORCHESTRUM
  ↓
Agentes IA
  ↓
GitHub
```

**GitHub es la fuente persistente de verdad.**

## Arquitectura + identidad

**La arquitectura es estándar. La identidad es tuya.**

ARQUITEKTA separa la arquitectura maestra MVA del lenguaje visual de cada producto. El módulo **DESIGN** puede partir de una entrevista, referencias, capturas o mockups; tras aprobación humana genera un **Design Profile** reutilizable para una app o una familia completa de apps.

Ver `docs/DESIGN_ENGINE.md`.

## Dos motores del MVP
### CREATE
Idea → Especificación → Arquitectura → Módulos → Repo → Código → Tests → Preview → Auditoría → Aprobación → Producción.

### AUDIT
Repo existente → análisis MVA → Cumple / Faltante / Desactualizado / Riesgo → propuesta de corrección → revisión → aplicación → evidencia.

## Módulos
DESIGN Engine · Design Profile · Reference Engine · Brand Engine · Layout Engine · Component Engine · Core UI/UX · ORCHESTRUM · Auth · Database · API · AI · Jobs/Workers · Payments · Maps · Notifications · Storage · Analytics · Deployment · Portability · Ledger · Backup/Restore.

## Gestión del proyecto

- GitHub Project: **ARQUITEKTA — PRODUCT & ENGINEERING ROADMAP (#9)**
- Roadmap versionado: `ROADMAP.md`
- Estado vivo: `PROJECT_STATUS.md`
- Ledger: `PROJECT_LEDGER.md`
- Issues #1–#7 representan las fases 0–6 del roadmap.

## Estado
Ver `PROJECT_STATUS.md` y `ROADMAP.md`.

## Desarrollo
```bash
npm install
npm run dev
```

## Auditoría local
```bash
npm run audit:mva
npm test
```

## Licencia
Software propietario. Ver `LICENSE`.
