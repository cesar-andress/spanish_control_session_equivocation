# Guía de criterios: tipo de respuesta v0.3

**Estado: BORRADOR — NO CONGELADO**  
**Versión:** `0.3.0`  
**Fecha:** 2026-10-05  
**Hash:** calcular al congelar (`sha256` de este archivo); aún no congelado.

Sustituye a v0.2 como instrumento de trabajo para calibración futura.  
v0.2 se conserva intacta en `reply_status_codebook_v0.2.md`.

Anclas bibliográficas (verificadas en Fase 0): Bull (1994); Bull & Mayer (1993);
aplicaciones a PMQs. Contexto de género discursivo en español: Fuentes Rodríguez;
Santos López. Véase `_internal/literature/REPLY_STATUS_FRAMEWORK.md`.

Ejemplos de desarrollo: solo fuera de la población XIV
(`zenodo/protocol/development_set_manifest.yaml`). No usar unidades elegibles
de la XIV para practicar criterios.

Los juicios del ejercicio de desarrollo **no** son etiquetas de referencia,
oro, calibración ni fiabilidad.

---

## 0. Principio de diseño

Este instrumento mide la **responsividad** de la primera respuesta del
Presidente del Gobierno (`R1`) respecto de la demanda comunicativa de la
pregunta oral (`Q1`).

No mide honestidad, veracidad, calidad de la política, eficacia,
moralidad, acuerdo entre personas expertas ni persuasión.

Una respuesta puede discrepar abiertamente de quien pregunta y ser, aun así,
una **respuesta explícita**. Un discurso fluido puede ser **ausencia de
respuesta** si no atiende a lo preguntado.

Hablar del **mismo tema** no basta. La decisión depende de si la intervención
aporta información que resuelve, total o parcialmente, la **cuestión
planteada**.

Los códigos del lado de la pregunta describen la pregunta, no la respuesta.
**Nunca** determinan ni sustituyen el tipo de respuesta.

---

## 1. Unidad de anotación

Cada unidad contiene, en este orden:

1. **Pregunta registrada** (`registered_question`) — formulación escrita
   oficial de la pregunta oral (`180/`);  
2. **Pregunta oral** (`Q1`) — turno de apertura de quien pregunta en el
   hemiciclo;  
3. **Primera respuesta del Presidente del Gobierno** (`R1`).

Réplica y dúplica quedan **fuera de alcance**.

### 1.1 Regla obligatoria de presentación del paquete

En desarrollo, calibración y anotación principal, **toda** unidad debe mostrar
siempre los tres textos, en ese orden.

No hay excepciones salvo que la pregunta registrada resulte realmente
indisponible; en ese caso la unidad debe **marcarse antes** de anotar y no
entrar en el circuito ordinario.

Esta regla corrige un defecto de presentación del primer cuaderno humano
(casos 12 y 13 del ejercicio de desarrollo), donde la pregunta registrada no
se mostró. Las devoluciones originales de aquel ejercicio **no** se alteran
retroactivamente.

La validación de paquetes debe fallar si falta alguno de los tres campos o si
aparece vacío / solo espacios (salvo unidad previamente marcada como
registrada-indisponible).

---

## 2. Regla de objetivo (pregunta oral; registrada como ancla)

**Objeto del juicio:** la demanda o demandas comunicativas de **`Q1`**.

**Ancla institucional:** la **pregunta registrada** identifica el expediente
oficial y ayuda a interpretar formulaciones orales elípticas («eso», «esta
situación», «doy por formulada la pregunta»).

No se reduce la unidad a la pregunta registrada sola.  
No se ignora la pregunta registrada.

### 2.1 Cuando registrada y oral no coinciden

| Situación | Qué hacer |
|-----------|-----------|
| La oral reformula el mismo encargo | Juzgar por la oral; usar la registrada para confirmar el encargo |
| La oral amplía con ejemplos o presión | Juzgar por la oral (incluido el núcleo ampliado) |
| La oral sustituye el encargo registrado por otra petición | Juzgar por la petición **oral** principal; anotar el desajuste en observaciones |
| La oral es casi vacía («doy por formulada…») | Recuperar el encargo desde la registrada; sin registrada visible, no anotar |

### 2.2 `question_target_type` (borrador)

| Valor | Cuándo |
|-------|--------|
| `match` | Q1 reformula esencialmente el mismo encargo que el título registrado |
| `oral_expansion` | Q1 conserva ese encargo y añade ejemplos, presión o detalle secundario |
| `multiple_question` | Q1 contiene dos o más demandas informativas **distintas** |
| `oral_substitution` | La demanda principal de Q1 sustituye el encargo registrado |

### 2.3 Orden de codificación recomendado

1. Leer la pregunta registrada (ancla).  
2. Leer Q1; asignar `question_target_type`, `question_form`,
   `question_confrontational` (**sin** dejar que decidan el tipo de respuesta).  
3. Identificar la **cuestión principal** (y, si las hay, demandas coiguales).  
4. Leer R1; asignar el tipo de respuesta a esa(s) demanda(s).  
5. Opcional: caso dudoso (`borderline`), observaciones (`notes`).

---

## 3. Distinción central: tema frente a cuestión

### 3.1 Hablar del mismo tema

La respuesta menciona el mismo ámbito político, repite posiciones generales
del Gobierno, usa vocabulario relacionado o alude de forma amplia a una ley,
medida, propuesta, plan o fórmula.

Eso establece **relevancia temática**. Por sí solo **no** establece
responsividad.

### 3.2 Responder a la cuestión planteada

La respuesta aporta información, evaluación, afirmación, negación o rechazo
de premisa que **atiende a la demanda comunicativa** identificada en Q1
(con ayuda, si hace falta, de la pregunta registrada).

La decisión debe apoyarse en esa demanda, no en la mera continuidad temática.

### 3.3 Referencias genéricas (criterio discursivo-semántico)

Palabras como *ley*, *medida*, *propuesta*, *fórmula*, *plan* o *acción*
pueden coincidir temáticamente con la pregunta y, aun así, no aportar lo
pedido.

**Regla:** el solapamiento léxico o temático **no** basta. Una referencia
genérica solo cuenta cuando la proposición que la rodea aporta información
que atiende a lo solicitado.

No es una regla de palabras clave. Es un criterio de **demanda comunicativa**
y de **concreción proposicional**.

---

## 4. Variables del lado de la pregunta (no son resultados)

Se codifican a partir de **Q1** (la registrada puede ayudar a desambiguar).
Independientes del tipo de respuesta.

### 4.1 `question_form`

| Valor | Definición |
|-------|------------|
| `yes_no` | La demanda principal busca afirmación o negación |
| `wh` | La demanda principal busca un encaje factual concreto (quién/qué/cuándo/cuánto/cómo…) |
| `evaluative` | La demanda principal busca valoración o toma de postura |

Si hay mezcla, codificar la demanda **dominante**. Anotar duda en
observaciones.

### 4.2 `question_confrontational`

| Valor | Definición |
|-------|------------|
| `no` | La pregunta no carga una presuposición conflictiva ni un ataque personalizado como núcleo |
| `yes` | La pregunta incorpora presuposición cargada, acusación o ataque personalizado |

Rasgo grueso para estratificación descriptiva posterior. **No** es un juicio
moral y **no** debe cambiar el tipo de respuesta.

Una pregunta confrontativa puede recibir respuesta explícita.  
Una pregunta neutra puede recibir ausencia de respuesta.

---

## 5. Campo principal: tipo de respuesta (`reply_status`)

Valores internos (reproducibilidad):

`reply_status` ∈ {`explicit_reply`, `intermediate_reply`, `non_reply`}

Etiquetas humanas:

| Valor interno | Etiqueta |
|---------------|----------|
| `explicit_reply` | respuesta explícita |
| `intermediate_reply` | respuesta parcial o intermedia |
| `non_reply` | ausencia de respuesta |

Opcional: `borderline` (caso dudoso), `notes` (observaciones breves).

---

## 6. Definiciones de categoría

### 6.1 Respuesta explícita (`explicit_reply`)

**Definición.** R1 resuelve de forma directa la demanda comunicativa
principal de Q1.

Puede:

- afirmar;  
- negar;  
- rechazar una premisa **si** ese rechazo atiende a lo que la pregunta exige;  
- aportar la información o la valoración pedidas;  
- ofrecer un llenado alternativo claro del mismo encargo («no X, sino Y»).

**No basta:** solo preámbulo, ataque o relato de gestión sin atender al
encargo; promesa vaga sin comprometer ahora lo pedido; contestar a otra
pregunta.

**Caso dudoso:** la respuesta queda clara aunque venga tras un preámbulo
largo → preferir respuesta explícita y marcar caso dudoso.

**Desempate:** si en algún punto de R1 aparece una contestación clara a la
demanda oral, preferir respuesta explícita frente a parcial.

### 6.2 Respuesta parcial o intermedia (`intermediate_reply`)

**Definición.** R1 aporta información que incide en la cuestión planteada,
pero **no** la resuelve del todo.

Aplica cuando:

- al menos un componente sustantivo queda atendido y otro relevante permanece
  sin resolver;  
- se da información pertinente al encargo sin completarlo;  
- hace falta una inferencia, pero la conexión está razonablemente acotada por
  lo dicho;  
- hay compromiso o aplazamiento que toca la sustancia de forma incompleta.

**No** se define como «algo relacionado con el tema». Eso colapsaría la
frontera con la ausencia de respuesta.

**Exclusiones:**

- contestación clara y completa → respuesta explícita;  
- solo continuidad temática o cambio de foco sin aporte sustantivo → ausencia
  de respuesta.

**Desempate:** ¿aporta R1 algún contenido que **intente** llenar el encargo
oral? Si sí → parcial; si no → ausencia.

### 6.3 Ausencia de respuesta (`non_reply`)

**Definición.** R1 no aporta información que resuelva la demanda
comunicativa de Q1.

Aplica cuando:

- se queda solo en el tema general;  
- cambia el foco;  
- ataca o critica sin atender a la cuestión;  
- ofrece mensaje político genérico sin contestación sustantiva;  
- contesta a otra pregunta (hombre de paja);  
- se limita a procedimiento («ya lo dije») sin sustancia sobre el encargo.

La continuidad temática **no** impide esta clasificación.

**Desempate:** ataque + contestación clara → respuesta explícita.  
Ataque sin contestación → ausencia de respuesta.

---

## 7. Preguntas con varias demandas

Si Q1 contiene varias peticiones **genuinamente independientes**, identificar
las demandas comunicativas **sustantivas**. No contar mecánicamente cada
interrogativa retórica como pregunta distinta.

| Situación | Tipo de respuesta |
|-----------|-------------------|
| Todos los componentes centrales quedan atendidos de forma sustantiva | respuesta explícita |
| Al menos un componente central queda atendido y otro permanece sin resolver | respuesta parcial o intermedia |
| Ningún componente central queda atendido de forma sustantiva | ausencia de respuesta |

### 7.1 Eje cuantitativo y eje cualitativo

Algunas preguntas combinan un pedido factual/cuantitativo y un pedido
evaluativo («¿cuántos X y cómo valora Y?»).

Si ambos ejes son **coiguales** y la respuesta atiende solo a uno → en
general, **respuesta parcial o intermedia**.

Si el discurso deja claro que un eje es claramente subordinado, no forzar una
regla mecánica: identificar la demanda principal y las coiguales, y anotarlo
en observaciones cuando haya duda.

No se adoptan, por ahora, dos listados de categorías independientes
(cobertura frente a concreción). La cobertura de componentes se resuelve
dentro de las tres categorías anteriores.

---

## 8. Rechazo de premisa (frontera conocida)

Una respuesta que rechaza de forma explícita una presuposición **puede** ser
respuesta explícita si ese rechazo resuelve directamente la demanda
comunicativa de la pregunta.

Si quien habla solo ataca la premisa o a quien pregunta y no aporta la
información o valoración pedidas, el resultado puede ser parcial o ausencia,
según el contenido sustantivo que quede.

Esta frontera **no** quedó del todo cerrada en el ejercicio de desarrollo.
Debe revisarse de forma explícita en calibración.

---

## 9. Salvaguardas frente al sesgo político

El contexto político puede influir en la interpretación, sobre todo si quien
codifica se apoya en preferencias partidistas en lugar de en la relación
discursiva pregunta–respuesta.

Salvaguardas metodológicas:

- ocultar en el paquete metadatos de partido, grupo, alineación o voto;  
- presentar los mismos campos lingüísticos a ambas personas expertas;  
- exigir criterios discursivos explícitos (demanda, aporte, concreción);  
- pedir justificación textual en casos dudosos;  
- preservar juicios independientes antes de cualquier discusión;  
- analizar más adelante los resultados por persona experta.

El cegamiento político completo puede ser imposible cuando nombres o
referencias políticas aparecen **dentro** del texto parlamentario auténtico.
No se altera ese texto solo para neutralizarlo si ello cambia el discurso.

---

## 10. Caso frontera conocido (ejercicio de desarrollo)

**Caso 7** del ejercicio fuera de muestra (unidad de desarrollo; **fuera** de
calibración y de la evaluación principal).

Pregunta oral por medidas frente a la burbuja del alquiler; respuesta que
anuncia de forma genérica una futura ley de vivienda y gestos conexos.

Dos lecturas expertas siguen siendo plausibles:

- **parcial:** la respuesta aporta un compromiso legislativo en el ámbito de
  la vivienda, con conexión temática acotada al problema habitacional;  
- **ausencia:** se pregunta por el alquiler y se responde con una
  generalidad («ley de vivienda») que no especifica medidas sobre esa burbuja.

La frontera que expone es la de la sección 3 (tema frente a cuestión) y la
regla de referencias genéricas (sección 3.3).

v0.3 no fuerza una categoría para este caso. No identifica a una persona
experta como correcta. El caso permanece fuera de calibración y de la
evaluación principal.

---

## 11. Ejemplos orientativos (no son respuestas correctas)

Extraídos del material de desarrollo fuera de muestra. Sirven para ilustrar
el razonamiento. **No** son etiquetas de oro.

### 11.1 Tema sin resolver la cuestión (orientativo)

Pregunta oral que pide una reunión concreta para hablar de aplicar el
artículo 155; respuesta que vuelve a la pregunta registrada sobre la
situación política y no acepta ni rechaza la reunión pedida.

Razonamiento orientativo: continuidad temática posible; la demanda
comunicativa de la oral (reunión / 155) no queda resuelta → tiende a
**ausencia de respuesta**.

### 11.2 Continuidad temática con medidas ya hechas (orientativo)

Pregunta por medidas **nuevas** a impulsar; respuesta que enumera actuaciones
generales ya emprendidas sin comprometer lo pedido como futuro.

Razonamiento orientativo: habla del ámbito; no aporta el contenido exigido
por el verbo de la pregunta → tiende a **ausencia de respuesta**.

### 11.3 Compromiso genérico con algo de aporte (orientativo)

Pregunta por el compromiso con el autogobierno pactado; respuesta que afirma
la vigencia del marco estatutario sin detallar acciones concretas.

Razonamiento orientativo: hay aporte sustantivo incompleto sobre el
compromiso → puede situarse en **respuesta parcial o intermedia**.

### 11.4 Fórmula genérica ante un «cómo» (orientativo / frontera)

Pregunta por la mejor fórmula para decidir el futuro; respuesta que apela a
ley y diálogo en términos amplios.

Razonamiento orientativo: puede leerse como aporte incompleto a la «fórmula»
pedida o como mera generalidad. Exige aplicar la sección 3.3. No enseñar aquí
una única categoría como correcta cuando el grado de concreción es discutible.

### 11.5 Rechazo de premisa (orientativo / frontera de calibración)

Si R1 niega una presuposición y, al hacerlo, resuelve el sí/no o el qué
pedido → puede ser **respuesta explícita**.  
Si solo combate el encuadre sin aportar lo pedido → parcial o ausencia,
según el contenido restante (sección 8).

---

## 12. Tabla de patrones difíciles

| Patrón | Tendencia por defecto | Nota |
|--------|------------------------|------|
| Negación de premisa que resuelve el encargo | respuesta explícita | El rechazo puede ser la respuesta |
| Ataque **con** contestación clara | respuesta explícita | El ataque es añadido |
| Ataque **sin** contestación | ausencia de respuesta | |
| Preámbulo político y luego contestación clara | respuesta explícita | marcar dudoso si cuesta localizarla |
| Solo una de varias demandas centrales | respuesta parcial o intermedia | salvo reformulaciones del mismo encargo |
| Solo procedimiento | ausencia de respuesta | |
| Compromiso futuro vago («lo estudiaremos») | parcial o ausencia | parcial si el pedido era «¿va a…?» y el compromiso es la única sustancia |
| Relato general de gestión | ausencia, salvo que llene el encargo | |
| Pregunta evaluativa + postura clara | respuesta explícita | «estamos trabajando» sin postura → parcial o ausencia |
| Referencia genérica (*ley*, *medida*…) sin contenido que atienda al pedido | ausencia o, si hay aporte incompleto acotado, parcial | no decidir por la palabra sola |

---

## 13. Campos de anotación (v0.3)

Obligatorios en filas de estudio:

- `reply_status`
- `question_target_type`
- `question_form`
- `question_confrontational`

Diagnósticos opcionales:

- `borderline`
- `notes`

Procedencia (cada fila): `unit_id`, `annotator_id`, `codebook_version`,
`codebook_hash`, `packet_version`, `coded_on`.

No añadir más variables de resultado en v0.3.

---

## 14. Calibración (diseño; semillas aún no asignadas)

Solo corpus fuera de la población XIV (véase `CALIBRATION_DESIGN.md`).

| Ronda | N | Regla |
|-------|---|-------|
| Calibración 1 | 20 | Codificación independiente → discusión → cabe revisar la guía |
| Calibración 2 | 20 nuevas | Idem |
| Después | — | Congelar la guía (hash) antes de la anotación principal XIV |

El conjunto de desarrollo **no** sirve para estimar fiabilidad.  
El caso frontera conocido del desarrollo permanece fuera de calibración.

---

## 15. Historial de versiones

| Versión | Fecha | Notas |
|---------|-------|-------|
| 0.1.0 | 2026-10-01 | Borrador inicial; objetivo anclado en la registrada |
| 0.2.0 | 2026-10-01 | Objetivo en Q1 + variables de pregunta + casos difíciles |
| 0.3.0 | 2026-10-05 | Tema frente a cuestión; referencias genéricas; presentación obligatoria de los tres textos; preguntas múltiples; rechazo de premisa cauteloso; caso frontera conocido; salvaguardas de sesgo. **BORRADOR** |

Detalle de cambios: `reply_status_codebook_v0.2_to_v0.3_changes.md`.
