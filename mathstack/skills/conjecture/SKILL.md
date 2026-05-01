# /conjecture

Takes a rough intuition and turns it into a precise mathematical statement.
Does not attempt to prove it — that's `/derive`. Does not attempt to disprove it — that's `/counterexample`.

---

## Preamble

```bash
echo "=== Conjecture ==="
if [ -f research-state.yaml ]; then
  cat research-state.yaml
fi
```

---

## Inputs

The user provides a rough idea. It might be:
- A sentence ("I think the spectral gap scales like 1/n")
- A pattern observed in simulation output
- An analogy from another field ("this looks like the Perron-Frobenius situation")
- A failed proof that almost worked

Read it carefully. Do not rush to formalise. Ask one clarifying question if the mathematical object isn't clear — what space, what operator, what measure.

---

## Workflow

**1. Identify the mathematical objects.**
Name everything: the space, the operator, the measure, the parameter. If any are ambiguous, flag them. Do not proceed with a vague object — a conjecture about "a matrix" is not a conjecture.

**2. Write the rough statement.**
One sentence. Use quantifiers explicitly. "For all...", "there exists...", "as n → ∞...". Do not bury assumptions in prose.

**3. Check the trivial cases.**
Before anything else:
- Does it hold for the simplest non-trivial example? Work it out.
- Does it hold in the degenerate case? (n=1, empty set, identity operator, etc.)
- Does it reduce to a known result in a special case? If yes, name it — this is evidence for the conjecture and a proof strategy hint.

**4. Check the boundary cases.**
Where might the conjecture break? Name the conditions under which you'd expect it to fail. These are the assumptions that need to appear in the statement.

**5. Write the formal statement.**
LaTeX. Include:
- All quantifiers
- All assumptions (even obvious ones — "let H be a separable Hilbert space")
- The precise claim
- The regime if it's an asymptotic result ("as n → ∞, uniformly in...")

**6. Suggest a stepping-stone hierarchy.**
What is a strictly weaker version that still has value if proved? What is a strictly stronger version that would be more useful? Write both. The weaker version is usually where to start.

**7. Assign a conjecture ID.**
Read existing IDs in research-state.yaml and assign the next one (C1, C2, ...).

---

## Output

Add to `open_conjectures` in research-state.yaml:

```yaml
- id: CN
  statement: "LaTeX statement"
  precision: formalised
  trivial_cases_checked: true
  stepping_stone: "weaker version to prove first"
  evidence_for: []
  evidence_against: []
  next_step: "Run /counterexample, then attempt stepping-stone version"
  weeks_active: 0
```

Also write the full statement with context to `conjectures/CN.md`:
- Motivation (where did this come from?)
- Formal statement
- Special cases and what they give
- Stepping-stone hierarchy
- Initial proof ideas (brief — not a proof attempt, just angles)

---

## Voice

Precise. A conjecture is only as good as its statement. If the statement has an ambiguous quantifier, the conjecture is not stated. Push back on vagueness even if the researcher seems certain.

---

## Completion

- **DONE** — formal statement written, trivial cases checked, research-state.yaml updated
- **NEEDS_CONTEXT** — the mathematical object is not clear enough to formalise; state exactly what's missing
- **DONE_WITH_CONCERNS** — statement formalised but one or more assumptions may be too strong to be interesting; flag for research director review
