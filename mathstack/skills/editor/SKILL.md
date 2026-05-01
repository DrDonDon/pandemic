# /editor

Reviews the technical paper for communication quality — structure, clarity, notation, narrative.
Does NOT check whether proofs are correct — that's `/proof-review`.

---

## Preamble

```bash
echo "=== Editor ==="
PAPER="${1:-paper/main.tex}"
if [ -f "$PAPER" ]; then
  echo "--- Paper ---"
  cat "$PAPER"
else
  echo "Paper not found at $PAPER — check path"
fi
if [ -f research-state.yaml ]; then
  cat research-state.yaml
fi
```

---

## What this review is for

A technically correct paper can still fail to communicate. The editor's job is to make sure the paper earns its reader's attention at every section.

The two failure modes:
1. **The reader gets lost** — structure is unclear, motivation is buried, notation shifts
2. **The reader doesn't trust the paper** — claims in the intro are stronger than what's proved, assumptions appear late, related work is dismissed

---

## Review Sections

Work through every section of the paper. Write a comment for each.

### Abstract

- Does it state what was proved, not just what was studied?
- Are claims in the abstract provably true given the paper? (Abstracts often overclaim)
- Does it name the technique or approach? Readers decide whether to read the paper from the abstract
- Is it self-contained? (No undefined notation, no citations)

### Introduction

- Is the problem motivated before the solution is stated?
- Does the introduction tell the reader what they will find, in the order they will find it?
- Is the main result stated in the introduction, not just "we prove results about X"?
- Is the paper's relationship to prior work clear from the introduction alone?

### Related Work

- Is every cited result characterised accurately?
- Are comparisons honest? ("We improve upon X" requires that the result is actually stronger under comparable assumptions)
- Is credit given correctly? Negative citations ("unlike X, we do not assume Y") should be used sparingly and verified

### Definitions and Notation

- Are all objects defined before they are used?
- Is notation consistent throughout? (Check: same symbol used for two things, or two symbols for the same thing)
- Are definitions placed where they're needed, not all at the front in a notation-dump?

### Theorem Statements

- Are assumptions listed before the conclusion?
- Are quantifiers explicit?
- Is the theorem statement the same as what the proof actually proves? (Not stronger, not weaker)
- Are informal "remarks" after theorems accurate?

### Proofs

The editor does not check correctness, but checks readability:
- Are long proofs broken into lemmas with named, motivated purposes?
- Are the hard steps signposted? ("The key step is...", "The difficulty is...")
- Are short proofs written as proofs, not as equations-with-no-words?

### Discussion / Conclusion

- Does it distinguish what was proved from what is conjectured?
- Are open problems stated precisely, not as vague "future work"?
- Does the discussion place the results in context of the adjacent results?

---

## Output

Write `paper/editorial-review.md`:

```markdown
## Editorial Review — [DATE]

### Overall assessment
[2–3 sentences: is this paper ready to submit? what is the main structural issue?]

### Abstract
[Comment]

### Introduction
[Comment]

### Related Work
[Comment]

### Definitions / Notation
[Notation conflicts: list any]

### Theorems
[Comment]

### Proofs
[Comment]

### Discussion
[Comment]

### Priority fixes (before submission)
1. [Most important]
2. ...

### Minor fixes
- [List]
```

---

## Voice

Editorial, not hostile. The goal is a better paper. For every "this doesn't work", say why and what would work. The most common editorial failure is saying "this is unclear" without explaining what would make it clear.

Be specific about notation conflicts — name the symbol and the two places it's used with different meanings.

---

## Completion

- **DONE** — editorial-review.md written
- **DONE_WITH_CONCERNS** — abstract overclaims relative to what is proved; flag explicitly, this blocks submission
