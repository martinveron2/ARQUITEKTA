# ARQUITEKTA DESIGN ENGINE

## Directiva de producto

**La arquitectura es estándar. La identidad es tuya.**

ARQUITEKTA separa de forma explícita dos responsabilidades:

- **ARQUITEKTA CORE** gobierna cómo se construye el sistema.
- **ARQUITEKTA DESIGN** gobierna cómo se ve, se siente y se expresa el producto.

La identidad visual nunca debe obligar a modificar la arquitectura maestra MVA, y la arquitectura nunca debe imponer una estética fija al usuario.

## 1. ARQUITEKTA CORE — arquitectura maestra

La capa CORE mantiene las reglas no negociables del estándar MVA:

- modularidad y escalabilidad desde el nacimiento;
- responsabilidades e interfaces claras;
- bajo acoplamiento;
- frontend, backend, core, datos, infraestructura e integraciones evolucionables por separado;
- proveedores externos mediante adapters/connectors reemplazables;
- portabilidad entre nubes, VPS y local;
- GitHub como fuente persistente de verdad;
- ledger, roadmap, estado, documentación y evidencia;
- testing, observabilidad, seguridad y auditoría;
- aprobación humana antes de producción o acciones sensibles.

El usuario puede cambiar completamente el lenguaje visual sin romper estas garantías.

## 2. ARQUITEKTA DESIGN — identidad desacoplada

DESIGN es un módulo diferenciado y enchufable. Su misión es convertir intención visual, referencias y preferencias en un sistema de diseño reutilizable.

Debe aceptar, entre otros:

- descripción conversacional;
- capturas de apps o sitios de referencia;
- links de referencia;
- logos y activos de marca;
- paletas existentes;
- mockups;
- archivos o exports de herramientas de diseño;
- preferencias de tipografía, densidad, navegación, motion y tono.

## 3. Flujo de diseño

```text
Entrevista visual
      ↓
Referencias
      ↓
Propuestas / Mockups
      ↓
Aprobación humana
      ↓
DESIGN PROFILE
      ↓
Tokens + Componentes + Layouts + Responsive + Motion
      ↓
Aplicación / Familia de aplicaciones
```

Ningún mockup se considera aprobado hasta existir aprobación explícita del usuario.

## 4. DESIGN PROFILE

Una vez aprobado un concepto, ARQUITEKTA genera un **Design Profile** versionado.

Como mínimo puede contener:

- colores y roles semánticos;
- tipografías y escala tipográfica;
- spacing scale;
- radios, bordes, sombras y elevación;
- grid y breakpoints;
- navegación;
- patrones de cards, listas y formularios;
- botones, inputs y estados;
- iconografía;
- motion;
- dark/light;
- reglas mobile-first y desktop;
- accesibilidad;
- tono visual;
- reglas de marca.

El Design Profile pertenece al proyecto o al usuario y puede reutilizarse sin copiar el diseño interno de ARQUITEKTA.

## 5. Modos de reutilización

### Clone style
Misma identidad visual y mismos tokens base.

### Family
Misma familia de diseño con variaciones controladas entre productos.

### Fresh
Conserva principios y preferencias del Design Profile, pero propone una identidad nueva.

### Reference mix
Combina el Design Profile con nuevas referencias aportadas por el usuario.

## 6. App Family

Un Design Profile puede gobernar múltiples productos:

```text
Design Profile
   ├─ App A
   ├─ App B
   ├─ App C
   └─ futuras apps
```

Cada app puede extender el perfil sin modificar silenciosamente el perfil maestro.

## 7. Motores enchufables

DESIGN no depende de un proveedor único.

Capas previstas:

- **Reference Engine** — interpreta referencias y activos;
- **Design Engine** — propone lenguaje visual y mockups;
- **Brand Engine** — marca, tono e identidad;
- **Layout Engine** — navegación, responsive y composición;
- **Component Engine** — genera o adapta componentes;
- **Style Memory / Design Profile Store** — persiste decisiones aprobadas;
- **Preview Renderer** — muestra previews verificables.

Los modelos de IA, generadores de imágenes, librerías UI y herramientas externas deben conectarse mediante adapters reemplazables.

## 8. Contrato CORE ↔ DESIGN

CORE y DESIGN se comunican por contratos explícitos.

DESIGN puede definir presentación, pero no debe:

- saltarse límites de módulos;
- acoplar el core a un framework visual;
- insertar secretos;
- modificar infraestructura directamente;
- declarar producción sin verificación;
- crear dependencias irreemplazables sin documentarlas.

CORE puede imponer restricciones técnicas, seguridad, accesibilidad y compatibilidad, pero no debe imponer la estética de ARQUITEKTA sobre los proyectos generados.

## 9. Regla de aceptación

Una solución de diseño cumple ARQUITEKTA cuando:

1. respeta el Design Profile aprobado;
2. mantiene mobile-first y responsive;
3. no rompe contratos de arquitectura;
4. puede reemplazarse o evolucionar sin reescribir el core;
5. deja evidencia y versión en GitHub;
6. conserva trazabilidad de las decisiones relevantes.

## 10. Principio comercial

ARQUITEKTA no vende una plantilla visual propietaria.

Vende el motor capaz de transformar una intención visual en un sistema de diseño reutilizable, versionado y conectado a una arquitectura de software sólida.

> **MVA define cómo debe estar construido el sistema. El usuario define cómo debe verse.**
