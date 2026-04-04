# /proof-review

Adversarial correctness check. Finds gaps. Challenges every step.
Does NOT review writing quality — that's `/editor`.

---

## Preamble

```bash
echo "=== Proof Review ==="
CONJECTURE_ID="${1:-}"
if [ -n "$CONJECTURE_ID" ] && [ -f "proofs/${CONJECTURE_ID}-draft.tex" ]; then
  echo "--- Proof draft ---"
  cat "proofs/${CONJECTURE_ID}-draft.tex"
elif [ -n "$CONJECTURE_ID" ] && [ -f "conjectures/${CONJECTURE_ID}.md" ]; then
  cat "conjectures/${CONJECTURE_ID}.md"
fi
if [ -f research-state.yaml ]; then
  cat research-state.yaml
fi
```

---

## Mindset

You are not trying to confirm the proof. You are trying to break it.
A proof that survives adversarial review is a proof. A proof that hasn't been attacked is a sketch.

---

## Review Process

Read the proof once for structure, then once for each step.

**Pass 1 — Structure**
- Does the proof strategy match the theorem? (Induction proofs need a base case and inductive step. Contradiction proofs need an explicit contradiction. Direct proofs need the conclusion to follow from the premises.)
- Is the proof outline correct even if the details are wrong?
- Are all major lemmas present?

**Pass 2 — Assumptions**
For every assumption in the theorem statement:
- Is it actually used in the proof?
- Where is it first used?
- What breaks if it's removed?

Flag any assumption that is never used — either the proof is wrong (the assumption is needed and was forgotten) or the theorem statement is too strong (the assumption can be dropped, which is a stronger result).

**Pass 3 — Each step**
For every step in the proof, ask:
1. **Is this step justified?** Name the lemma, theorem, or calculation that justifies it. If it's "obvious", make it explicit.
2. **Does the justification apply here?** The right lemma in the wrong conditions is not a justification. Check that all conditions of cited results are verified.
3. **Are there implicit steps?** Steps that "follow easily" often don't. Write out the calculation if there's any doubt.
4. **Are quantifiers consistent?** Swapping ∀ and ∃ is the most common error. Check every quantifier in every step.
5. **Are limits justified?** Every interchange of limit and integral, sum and limit, sup and inf requires a justification (dominated convergence, uniform convergence, monotone convergence, etc.).

**Pass 4 — Targeted attacks**
For conjectures that look plausible but feel tight:
- Try to construct a sequence that makes each bound sharp simultaneously
- Check whether the proof would also prove a slightly stronger claim (if so, either the proof is wrong or the theorem statement is weak)
- Try to adapt the proof to a related claim that is false — if the same proof would work, it's wrong

---

## Output

Write a review to `proofs/[CONJECTURE_ID]-review.md` with:

```markdown
## Proof Review — [CONJECTURE_ID] — [DATE]

### Verdict: VALID | GAPS_FOUND | INVALID

### Pass 1 — Structure
[findings]

### Pass 2 — Assumptions
[findings — list each assumption and whether it is used]

### Pass 3 — Step-by-step
[Step N: OK / NEEDS_JUSTIFICATION / GAP / WRONG]
[Details for any non-OK steps]

### Pass 4 — Targeted attacks
[What was tried, what was found]

### Summary
[If GAPS_FOUND: list gaps in order of severity]
[If INVALID: state the specific error and why it cannot be patched]
[If VALID: state what gives confidence — which steps were verified most carefully]
```

---

## Verdicts

- **VALID** — no gaps found; proof is correct to the best of this review
- **GAPS_FOUND** — specific steps are unjustified or wrong but the overall strategy may be salvageable; list each gap
- **INVALID** — the proof strategy itself is flawed, or a step is irreparably wrong; the proof must be reworked

---

## Voice

Precise about where the gap is. "Step 4 invokes dominated convergence but the integrand is not dominated by an integrable function in general — the bound at step 4 requires [additional assumption]." Not "step 4 seems unclear."

---

## Completion

- **DONE** — review written, verdict given, gaps listed if any
- **DONE_WITH_CONCERNS** — proof is likely correct but one step is too terse to verify; ask for expansion before declaring VALID
