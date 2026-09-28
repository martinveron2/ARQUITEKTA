# SYSTEM STATES

## Proyecto
DRAFT → DESIGNING → BUILDING → AUDITING → READY_FOR_APPROVAL → APPROVED → DEPLOYING → LIVE

Estados de excepción: BLOCKED · NEEDS_USER · FAILED · ROLLED_BACK.

## Regla
No saltar de BUILDING a LIVE. Producción requiere auditoría y aprobación explícita.
