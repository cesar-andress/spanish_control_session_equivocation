# Guía de criterios: resolución directa de la demanda comunicativa v1.0-draft

**Estado: BORRADOR DE REDISEÑO — NO CONGELADO**  
**Versión:** `direct_resolution 1.0-draft`  
**Fecha:** 2026-10-15  

## Linaje y motivo del rediseño

El instrumento tricategorial `reply_status` v0.3
(`respuesta explícita` / `parcial o intermedia` / `ausencia de respuesta`)
**falló** la puerta de fiabilidad bloqueada de la Ronda 2 de calibración
(Gate C: α nominal ≈ 0,126; κ binario explícita-vs-resto ≈ 0,121; n = 20).

Ese resultado se conserva íntegro como evidencia metodológica.  
**No** se rescata v0.3 mediante colapso de etiquetas ni recodificación
retroactiva de la Ronda 2.

Este documento define un **constructo binario nuevo**:

**resolución directa de la demanda comunicativa principal**

Es un rediseño sustantivo, no una revisión menor v0.4.

---

## 0. Pregunta de codificación

¿La primera respuesta del Presidente del Gobierno resuelve directamente la
demanda comunicativa principal de la pregunta oral?

| Etiqueta humana | Valor interno |
|-----------------|---------------|
| **Sí — resolución directa** | `direct_resolution_yes` |
| **No — no resolución directa** | `direct_resolution_no` |

Opcional: caso dudoso (Sí/No); observación breve.

---

## 1. Unidad y anclas

Cada unidad muestra, en este orden:

1. **Pregunta registrada** — ancla institucional;  
2. **Pregunta oral (`Q1`)** — **objeto principal** del juicio;  
3. **Primera respuesta del Presidente (`R1`)**.

Réplica y dúplica quedan fuera de alcance.

Si registrada y oral no coinciden: juzgar la demanda principal de la oral;
usar la registrada para desambiguar elipses («doy por formulada…», «eso»).

---

## 2. Paso previo (obligatorio como decisión; no es variable de anotación)

Antes de marcar Sí/No, identificar mentalmente:

> ¿Qué se le pide al Presidente que afirme, niegue, explique, evalúe,
> justifique o comprometa?

Eso es la **demanda comunicativa principal**.  
En el estudio principal **no** se exige escribirla; en orientación puede
practicarse en voz alta.

### 2.1 Cómo elegir la demanda principal

1. Preferir la **interrogativa explícita final** de Q1 si funciona como
   pregunta central al Presidente.  
2. Si no hay interrogativa clara, usar la **pregunta registrada** como ancla
   del encargo.  
3. Si ambas son ambiguas, usar la demanda que el hablante presenta
   explícitamente como la pregunta («le pregunto…», «la pregunta es…»).

Subpreguntas retóricas o ejemplos al servicio de una sola cuestión central
**no** cuentan como demandas independientes.

---

## 3. Definición de «resuelve directamente»

### 3.1 Sí — resolución directa

R1 contiene una proposición, postura, evaluación, razón, compromiso, acción
(pretendida o realizada) o rechazo **identificable en el texto** que atiende
a la demanda principal de Q1.

No hace falta repetir las palabras de la pregunta.  
Sí hace falta que la respuesta necesaria se recupere del propio R1 sin
añadir hechos externos ni inferencias políticas amplias.

### 3.2 No — no resolución directa

R1, entre otras posibilidades:

- solo habla del mismo tema;  
- aporta contexto sin resolver lo pedido;  
- ataca a quien pregunta;  
- reencuadra el debate sin contestar la demanda;  
- enumera políticas relacionadas sin identificar lo pedido;  
- deja sin identificar la postura/acción/evaluación/justificación exigida.

### 3.3 Lo que este instrumento **no** usa

No se decide por impresiones de «suficiente detalle», «demasiado general»,
«parcialmente explícito» u otras escalas vagas de grado.

La frontera es **resolución recuperable vs no resolución**, no un continuo
de explicitud.

---

## 4. Reglas por tipo de pregunta

### 4.1 Preguntas de sí/no

**Sí** si R1 comunica una postura afirmativa o negativa recuperable, aunque
no diga literalmente «sí» o «no».  
**No** si esa postura hay que adivinarla a partir de discusión temática.

### 4.2 Preguntas de qué / acción

**Sí** si R1 identifica qué se ha hecho, se hará o se pretende respecto de
la acción pedida.  
**No** si solo hay política/contexto general sin identificar esa acción.

Si Q1 pide acción **futura/nueva** y R1 solo enumera gestiones pasadas sin
compromiso relativo a lo pedido → **No**.

### 4.3 Preguntas de por qué / justificación

**Sí** si aporta al menos una razón o justificación de la decisión/hecho
preguntado.  
**No** si solo describe o reitera la decisión sin razón.

### 4.4 Preguntas de cómo

**Sí** si identifica un mecanismo, procedimiento, medida o vía que atiende
al «cómo».  
**No** si solo reafirma el objetivo.

### 4.5 Preguntas evaluativas

**Sí** si comunica una evaluación o postura identificable sobre el objeto
preguntado (puede ser indirecta, pero recuperable en R1).  
**No** si el codificador debe aportar la evaluación desde conocimiento
político o del mundo, o si R1 solo cierra el incidente de forma procedimental
sin valorar el contenido preguntado.

### 4.6 Rechazo de premisa

El rechazo directo de la premisa cuenta como **Sí** cuando ese rechazo
**resuelve** la demanda.

Ejemplo de principio: ante «¿Por qué hizo X?», si R1 afirma con claridad
«No hicimos X», la demanda queda resuelta por rechazo de premisa → **Sí**.

Si solo se combate el encuadre sin resolver lo pedido → **No**.

### 4.7 Respuestas indirectas

No se exige eco literal de la interrogación.  
Una respuesta indirecta es **Sí** solo si la proposición/postura necesaria
se sigue de forma directa del texto de R1.  
No se admiten inferencias políticas amplias.

---

## 5. Preguntas con varios encargos

No hay categoría intermedia ni escala de completitud.

1. Reducir a **una** demanda principal con la regla del §2.1.  
2. Juzgar Sí/No solo respecto de esa demanda.  
3. Si hay varias demandas **genuinamente independientes** y ninguna prioridad
   del §2.1 las ordena, preferir la ancla registrada; anotar duda en
   observaciones.

Casos límite: dos ejes coiguales sin interrogativa final dominante → usar
registrada; si aun así hay empate, marcar dudoso y decidir Sí solo si **esa**
demanda ancla queda resuelta (no exigir resolver todas).

---

## 6. Salvaguardas

- El partido, la alineación o el voto de investidura **no** determinan el
  código.  
- Hablar del mismo tema **no** basta.  
- Una respuesta puede disentir abiertamente y ser **Sí**.  
- Un discurso fluido puede ser **No**.

---

## 7. Material antiguo (solo ilustración)

Los casos de desarrollo, Ronda 1 y Ronda 2 pueden usarse en una orientación
breve para explicar la regla.  
**Nunca** cuentan como evidencia de fiabilidad de este instrumento.  
**No** se recodifican para publicar κ/α del nuevo constructo.

---

## 8. Congelación

Este borrador se congela solo tras:

1. orientación conjunta mínima sobre la regla binaria;  
2. validación independiente en casos OOP genuinamente nuevos;  
3. cumplimiento de la puerta prospectiva documentada
   (κ ≥ 0,67 **y** acuerdo bruto ≥ 10/12).

Si esa puerta falla: **STOP**; no hay ronda automática adicional.
