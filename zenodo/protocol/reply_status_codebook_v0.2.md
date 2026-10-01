# Reply-status codebook v0.2

**Status: DRAFT — NOT FROZEN**  
**Version:** `0.2.0`  
**Date:** 2026-10-01  
**Hash:** compute at freeze (`sha256` of this file); not frozen yet.

Supersedes v0.1 on the **target rule** (Q1 as judged ask; registered as
anchor) and adds draft **question-side** fields. Primary literature anchors
(verified Phase 0): Bull (1994); Bull & Mayer (1993); PMQs applications.
Spanish genre context: Fuentes Rodríguez; Santos López. See
`_internal/literature/REPLY_STATUS_FRAMEWORK.md`.

Development examples: out-of-pool only
(`zenodo/protocol/development_set_manifest.yaml`). Do **not** use XIV eligible
units for codebook practice.

---

## 0. Design principle

This instrument measures **responsiveness of the Prime Minister’s first
response (`R1`) to the oral question turn (`Q1`)**.

It does **not** measure honesty, truthfulness, policy quality, political
effectiveness, morality, annotator agreement, or persuasiveness.

A response may strongly disagree with the questioner and still be an
**explicit reply**. A fluent speech may be a **non-reply** if it never answers
the oral ask.

**Question-side codes describe the question, not the answer.** They must
**never** determine or overwrite `reply_status`.

---

## 1. Unit of annotation

Each unit contains:

1. `registered_question` — official written oral-question formulation (`180/`);  
2. `Q1` — questioner’s opening spoken turn;  
3. `R1` — Prime Minister’s **first** response.

Réplica / dúplica are **out of scope**.

---

## 2. Target rule (Q1 judged; registered as anchor)

**Judgement target:** the information request(s) in **`Q1`**.

**Institutional anchor:** the **registered question** identifies the official
slot and helps interpret elliptical oral wording (“eso”, “esta situación”).

### 2.1 `question_target_type` (draft)

| Value | When |
|-------|------|
| `match` | Q1 restates essentially the same information slot as the registered title |
| `oral_expansion` | Q1 keeps that slot but adds examples, pressure, or secondary detail |
| `multiple_question` | Q1 contains two or more **distinct** information requests |
| `oral_substitution` | Q1’s primary ask replaces the registered slot with a different request |

### 2.2 Multi-question rule

If Q1 contains several distinct asks, code `reply_status` against the **set of
oral asks**. Answering **only one** distinct ask → at most
`intermediate_reply`, unless the unanswered parts are clearly rhetorical
restatements of the **same** slot (then treat as one ask).

### 2.3 Coding order (recommended)

1. Read registered question (anchor).  
2. Read Q1; assign `question_target_type`, `question_form`,
   `question_confrontational` (**without** letting them decide the reply label).  
3. Read R1; assign `reply_status` to the oral ask(s).  
4. Optional: `borderline`, `notes`.

---

## 3. Question-side variables (not outcomes)

Coded from **Q1** (registered may help disambiguate form). Blind to reply
quality.

### 3.1 `question_form`

| Value | Definition |
|-------|------------|
| `yes_no` | Primary ask seeks affirmation/negation (¿ha…?, ¿va a…?, ¿es cierto…?) |
| `wh` | Primary ask seeks a specific slot (quién/qué/cuándo/cuánto/cómo + factual) |
| `evaluative` | Primary ask seeks valuation, assessment, or stance (¿qué valoración…?, ¿cómo valora…?) |

If mixed, code the **dominant** oral ask. Set `notes` if unsure.

### 3.2 `question_confrontational`

| Value | Definition |
|-------|------------|
| `no` | Ask does not embed a contentious presupposition or personalised attack as its load |
| `yes` | Ask embeds a loaded presupposition, accusation, or personalised attack that the answerer must navigate |

This is a **coarse** question feature for later descriptive stratification. It
is **not** a moral judgement and **must not** change `reply_status`.

---

## 4. Primary field: `reply_status`

`reply_status` ∈ {`explicit_reply`, `intermediate_reply`, `non_reply`}

Optional: `borderline` (boolean), `notes` (brief free text).

---

## 5. Category definitions

### 5.1 `explicit_reply`

**Definition.** R1 clearly fills the oral information slot (including clear
denial/refusal of the asked proposition).

**Positive criteria (any one sufficient if clear):**

- Clear yes/no (or equivalent) to a yes/no oral ask; **or**
- Concrete information requested (who/what/when/how much/whether); **or**
- Clear **denial**, **rejection**, or **refutation** of the asked proposition
  while addressing that proposition; **or**
- Clear alternative factual fill (“not X but Y”) of the asked slot; **or**
- For evaluative asks: a clear evaluative stance that answers the valuation
  request (praise, criticism, ranked judgement), not merely topic talk.

**Exclusions:**

- Only preamble, attack, or government-record narrative without answering;  
- Promise alone without committing the asked content now;  
- Answering a clearly different question.

**Borderline:** Answer buried after long preamble but clearly stated once →
prefer `explicit_reply` + `borderline=true`.

**Tie-break:** If a clear answer to the oral ask appears anywhere in R1, prefer
`explicit_reply` over `intermediate_reply`.

### 5.2 `intermediate_reply`

**Definition.** R1 engages the oral ask but leaves the requested slot
incomplete, hedged without settlement, partial, or only implied.

**Positive criteria:**

- Topic engaged but slot incomplete; **or**
- Conditional/hedged answer that never settles the ask; **or**
- Partial answer to a multi-part / multi-question oral turn; **or**
- Answer by implication only, without an overt fill; **or**
- Soft deferral that still touches the substance incompletely.

**Exclusions:**

- Full clear answer present → `explicit_reply`;  
- No engagement with the ask → `non_reply`.

**Borderline:** Heavy reframing that half-fills the slot → intermediate +
`borderline=true`.

**Tie-break:** Does R1 **attempt** to fill the oral slot at all? If yes →
intermediate; if no → non-reply.

### 5.3 `non_reply`

**Definition.** R1 does not answer the oral ask.

**Positive criteria:**

- Topic change unrelated to the ask; **or**
- Attack on questioner/party **without** answering; **or**
- Answers a different (straw) question; **or**
- Pure procedure / “as I already said” with no substance on the ask; **or**
- Generic government-record speech that never contacts the oral proposition.

**Exclusions:** Clear answer present → not non-reply even if attack co-occurs.

**Tie-break:** Attack + clear answer → `explicit_reply`. Attack + no answer →
`non_reply`.

---

## 6. Hard-case rules (worked)

| Pattern | Default | Note |
|---------|---------|------|
| Denial of premise but answering the whether/what slot | `explicit_reply` | Denial can be an answer |
| Criticism / attack on questioner **with** clear answer | `explicit_reply` | Attack is extra |
| Criticism / attack **without** answer | `non_reply` | |
| Political preamble then clear answer | `explicit_reply` | borderline if hard to locate |
| Partial answer | `intermediate_reply` | |
| Answers only one of multiple distinct oral asks | `intermediate_reply` | unless others are restatements |
| Procedural only | `non_reply` | |
| Future commitment only (“lo estudiaremos”) | `intermediate_reply` if the ask was “will you…?” without a present commitment; else often `non_reply` | Prefer intermediate when the promise is the sole response to a future-action ask |
| General government record | `non_reply` unless it fills the asked slot | |
| Evaluative ask (“¿cómo valora…?”) + clear stance | `explicit_reply` | Vague “estamos trabajando” without stance → intermediate or non-reply |
| Contests presupposition **and** answers the ask | `explicit_reply` | |
| Contests presupposition **only** (no slot fill) | usually `intermediate_reply` or `non_reply` | intermediate if it partially addresses; non-reply if pure rejection of framing with no content |

Illustrative Spanish snippets for training should come from the **out-of-pool**
development packet only (anonymised if later published).

---

## 7. Annotation fields (v0.2)

Required for study coding rows:

- `reply_status`
- `question_target_type`
- `question_form`
- `question_confrontational`

Optional diagnostics:

- `borderline`
- `notes`

Provenance (every label row): `unit_id`, `annotator_id`, `codebook_version`,
`codebook_hash`, `packet_version`, `coded_on`.

Do not add further outcome variables in v0.2.

---

## 8. Calibration plan (design only; seeds unset)

Out-of-pool corpus only (see `CALIBRATION_DESIGN.md`).

| Round | N | Rule |
|-------|---|------|
| Calibration 1 | 20 | Independent coding → discussion → guideline revision allowed |
| Calibration 2 | 20 fresh | Independent coding → discussion → guideline revision allowed |
| Then | — | Freeze codebook (hash) before XIV main coding |

Reliability after calibration (thresholds TBD at freeze): three-level α/κ plus
**explicit vs not-explicit** sensitivity. Development set is **not** for
reliability estimation.

---

## 9. Change log

| Version | Date | Notes |
|---------|------|-------|
| 0.1.0 | 2026-10-01 | Initial draft; registered-primary target |
| 0.2.0 | 2026-10-01 | Q1 target + question-side fields + hard cases; DRAFT |
