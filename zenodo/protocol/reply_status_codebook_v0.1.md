# Reply-status codebook v0.1

**Status: DRAFT — NOT FROZEN**  
**Version:** `0.1.0`  
**Date:** 2026-10-01  
**Hash:** compute at freeze (`sha256` of this file); not frozen yet.

Primary literature anchors (verified Phase 0): Bull (1994); Bull & Mayer (1993);
PMQs applications (e.g. Bull & Strawson 2020). Spanish genre context: Fuentes
Rodríguez (2011/2012); Santos López (2010). See
`_internal/literature/REPLY_STATUS_FRAMEWORK.md`.

---

## 0. Design principle

This instrument measures **responsiveness to the question**.

It does **not** measure:

- honesty or truthfulness;
- quality of policy;
- political effectiveness;
- morality;
- whether the annotator agrees with the speaker;
- whether the answer is persuasive or rhetorically skilled.

A response may strongly disagree with the questioner and still be an **explicit
reply**. A fluent, persuasive speech may be a **non-reply** if it never answers
the registered request.

---

## 1. Unit of annotation

Each unit consists of three fields shown to annotators:

1. `registered_question` — official written oral-question formulation (`180/`);  
2. `Q1` — questioner’s opening spoken turn;  
3. `R1` — Prime Minister’s first response.

Réplica / dúplica are **out of scope** for this code.

**Anchoring rule.** Code responsiveness primarily to the **registered question**.
Use Q1 only to resolve reference (who/what “this” means) or to see how the ask
was delivered. If Q1 expands far beyond the registered text, still judge whether
R1 answers the **registered** information request.

---

## 2. Primary field

`reply_status` ∈ {

- `explicit_reply`
- `intermediate_reply`
- `non_reply`

}

Optional diagnostics (not primary outcomes):

- `borderline` ∈ {true, false}
- `confidence` ∈ {low, medium, high}
- `notes` — free text (brief)

Do not invent additional outcome variables in v0.1.

---

## 3. Category definitions

### 3.1 Explicit reply

**Positive criteria (any one sufficient if clear):**

- R1 states a clear yes/no (or equivalent) to a yes/no registered ask; **or**
- R1 supplies the concrete information requested (who/what/when/how much/whether); **or**
- R1 clearly **denies**, **rejects**, or **refutes** the asked proposition while
  still addressing that proposition; **or**
- R1 gives a clear alternative factual answer to the asked slot (“not X but Y”)
  that fills the request.

**Exclusion criteria:**

- Only context, praise, attack, or government-record narrative without answering
  the ask → not explicit.
- Promise to answer later / “we will study it” **alone** → not explicit (see
  intermediate / non-reply).
- Answering a **different** question clearly → not explicit.

**Borderline:** Answer buried after long preamble but still clearly stated once —
prefer `explicit_reply` and set `borderline=true`.

**Tie-break:** If a clear answer to the registered ask is present anywhere in R1,
prefer `explicit_reply` over `intermediate_reply`.

### 3.2 Intermediate reply

**Positive criteria:**

- R1 addresses the registered topic but leaves the requested slot incomplete; **or**
- Conditional / hedged answer that never settles the ask; **or**
- Partial answer to a multi-part registered question (some parts answered, others
  not); **or**
- Soft procedural deferral that still engages the substance incompletely
  (“depending on…”, “in part…”).

**Exclusion criteria:**

- Full clear answer present → upgrade to explicit.
- No engagement with the ask → non-reply.

**Borderline:** Heavy reframing that still half-answers — prefer intermediate
with `borderline=true` rather than guessing explicit.

**Tie-break:** When unsure between intermediate and non-reply, ask: does R1
**attempt** to fill the registered information slot at all? If yes → intermediate;
if no → non-reply.

### 3.3 Non-reply

**Positive criteria:**

- Topic change unrelated to the registered ask; **or**
- Attack on the questioner/party **without** answering; **or**
- Answers a different question (straw question); **or**
- Pure procedure / speaking-time / “as I already said” with no substance on the
  ask; **or**
- Generic government-record speech that never contacts the registered
  proposition.

**Exclusion criteria:**

- Clear answer to the ask is present → not non-reply even if attack co-occurs.

**Tie-break:** Attack + clear answer → `explicit_reply` (attack is extra).  
Attack + no answer → `non_reply`.

---

## 4. Hard-case rules (v0.1)

| Pattern | Default code | Note |
|---------|--------------|------|
| Direct denial of the asked claim | `explicit_reply` | Denial answers a whether-claim |
| Partial answer | `intermediate_reply` | |
| Reframing then clear answer | `explicit_reply` | borderline if hard to find |
| Reframing only | `non_reply` or `intermediate_reply` | intermediate only if partial fill of slot |
| Changing topic | `non_reply` | |
| Attacking the questioner only | `non_reply` | |
| Context/preamble then answer | `explicit_reply` | |
| Answering a different question | `non_reply` | |
| Procedural only | `non_reply` | |
| Promise of future action only | `intermediate_reply` if tied to ask; else `non_reply` | Prefer intermediate when the promise is the sole response to a “will you…?” ask without committing now |
| General government record | `non_reply` unless it fills the asked slot | |

Illustrative Spanish examples will be filled from the **development set** during
refinement (not from calibration/main). Development examples must not leak
alignment metadata into the public codebook beyond anonymised snippets if needed.

---

## 5. Annotation procedure

1. Read registered question; identify the information slot.  
2. Skim Q1 for reference only.  
3. Read R1 fully.  
4. Assign `reply_status`.  
5. Set `borderline` / `confidence` / `notes` if needed.  
6. Do **not** look up party, group, or alignment (packets are blinded).

---

## 6. Calibration plan (design only; seeds unset)

| Round | N | Rule |
|-------|---|------|
| Calibration 1 | 20 | Independent coding → discussion → allowed guideline revision |
| Calibration 2 | 20 fresh | Independent coding → discussion → allowed guideline revision |
| Then | — | Freeze codebook (hash) before main sample |

Development set (n=15) is **not** for reliability estimation.

Proposed reliability metrics at freeze (thresholds TBD, not chosen for results):

- Krippendorff’s α (nominal) on three-level `reply_status`;  
- Cohen’s κ (two coders);  
- Optional ordinal/weighted agreement if treating the three levels as ordered
  (explicit > intermediate > non-reply) — justify at freeze because the
  primary endpoint later dichotomises explicit vs other.

---

## 7. Provenance fields (required on every future label row)

`unit_id`, `annotator_id`, `codebook_version`, `codebook_hash`,
`packet_version`, `coded_on`  
(plus packet/condition metadata in the schema).

---

## 8. Change log

| Version | Date | Notes |
|---------|------|-------|
| 0.1.0 | 2026-10-01 | Initial draft for development; not frozen |
