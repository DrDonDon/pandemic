# /counterexample

Adversarially tries to disprove a conjecture before time is spent on a proof.
Cheap falsification first — numerical, then constructive.

Run this before `/derive`.

---

## Preamble

```bash
echo "=== Counterexample ==="
if [ -f research-state.yaml ]; then
  cat research-state.yaml
fi
# Check for existing conjecture file
CONJECTURE_ID="${1:-}"
if [ -n "$CONJECTURE_ID" ] && [ -f "conjectures/${CONJECTURE_ID}.md" ]; then
  echo "--- Conjecture file ---"
  cat "conjectures/${CONJECTURE_ID}.md"
fi
```

---

## Inputs

A conjecture ID (e.g. C1) or a statement passed directly.
Read the formal statement carefully, including all assumptions.

---

## Strategy: cheapest attack first

Work through these in order. Stop as soon as a counterexample is found.

**Round 1 — Boundary and degenerate cases (by hand)**
Try:
- The smallest non-trivial case (n=2, a 2×2 matrix, a 2-point space)
- The degenerate case (empty set, zero operator, constant function)
- The extremal case (maximum or minimum of any parameter)
- A case where the conclusion is as tight as possible

Work these out analytically. If any fails, you have a counterexample — stop and report.

**Round 2 — Random numerical search**
Write Python code to randomly sample instances and check the conjecture numerically.

```python
import numpy as np

# Template — adapt to the specific conjecture
np.random.seed(42)
N_TRIALS = 10000
violations = []

for trial in range(N_TRIALS):
    # Generate a random instance satisfying the assumptions
    # ...
    
    # Compute the quantity of interest
    # ...
    
    # Check whether the conjecture holds
    holds = ...  # boolean
    
    if not holds:
        violations.append({
            'trial': trial,
            'instance': ...,
            'lhs': ...,
            'rhs': ...,
        })

print(f"Violations found: {len(violations)} / {N_TRIALS}")
if violations:
    print("First violation:", violations[0])
```

Run this. Report the violation rate. If violations are found, extract the smallest/simplest one as the counterexample.

**Round 3 — Targeted search**
If Round 2 found no violations, search more deliberately:
- Near the boundary of the assumption region (just barely satisfying the conditions)
- At extreme parameter values (very large n, very small epsilon, highly non-symmetric cases)
- Cases inspired by known failure modes from adjacent results in the literature

**Round 4 — Structural attack**
Try to construct a counterexample analytically:
- Is there a family of examples where the conclusion degrades?
- Does the conjecture fail if you relax exactly one assumption?
- Is there a diagonalisation or adversarial construction that works?

---

## Output

**If counterexample found:**
1. State the counterexample explicitly and precisely
2. Verify it satisfies all assumptions
3. Verify it violates the conclusion
4. Move the conjecture to `disproved` in research-state.yaml with the counterexample
5. Add a full entry to `dead-ends.md` including the lesson
6. State what the counterexample tells us — is there a corrected conjecture?

**If no counterexample found:**
1. State what was tried (rounds 1–4), how many trials, what parameter ranges
2. Report any near-misses (cases where the conjecture barely held)
3. Add to `evidence_for` in the conjecture's entry in research-state.yaml
4. State: "No counterexample found in [N] trials across [parameter range]. Recommend proceeding to /derive."

---

## Voice

Adversarial but honest. The goal is to find a counterexample, not to confirm the conjecture. Report near-misses even if they didn't violate the conjecture — they inform the proof strategy.

Never say "the conjecture appears to be true" based on a finite numerical search. Say "no counterexample found in N trials."

---

## Completion

- **DONE** — counterexample found and logged, or no counterexample found and evidence recorded
- **DONE_WITH_CONCERNS** — no counterexample found but numerical evidence is thin (parameter range too narrow, n too small); state the limitation
- **NEEDS_CONTEXT** — conjecture statement is not computable (too abstract to implement); ask for a concrete specialisation
