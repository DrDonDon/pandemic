# /simulate

Numerical experiments. Tests conjectures, explores parameter space, surfaces patterns.
Feeds back into `/conjecture` and `/derive` — not a replacement for proof.

---

## Preamble

```bash
echo "=== Simulate ==="
if [ -f research-state.yaml ]; then
  cat research-state.yaml
fi
CONJECTURE_ID="${1:-}"
if [ -n "$CONJECTURE_ID" ] && [ -f "conjectures/${CONJECTURE_ID}.md" ]; then
  cat "conjectures/${CONJECTURE_ID}.md"
fi
# Check available Python packages
python3 -c "import numpy, scipy, matplotlib; print('numpy scipy matplotlib: OK')" 2>/dev/null || echo "Some packages missing"
```

---

## Inputs

A conjecture ID, a question ("how does X scale with n?"), or a specific experiment to run.

---

## Workflow

**1. State the experiment.**
Before writing code, state in one sentence what question the experiment will answer. "Does the spectral gap scale as O(1/n) for random adjacency matrices?" Not "let's see what happens."

**2. Design the experiment.**
- What is being measured?
- What parameters are being varied, and over what range?
- What is the sample size / number of trials?
- What would confirm the conjecture? What would refute it?

**3. Write and run the code.**

Standard template:
```python
import numpy as np
import scipy
import matplotlib.pyplot as plt
from pathlib import Path

# Experiment: [state what this tests]
# Conjecture: [CN — brief statement]

np.random.seed(42)
results = []

ns = [10, 20, 50, 100, 200, 500]  # parameter range
n_trials = 50                       # trials per parameter value

for n in ns:
    trial_values = []
    for _ in range(n_trials):
        # Generate instance
        # ...

        # Compute quantity of interest
        value = ...

        trial_values.append(value)

    results.append({
        'n': n,
        'mean': np.mean(trial_values),
        'std': np.std(trial_values),
        'min': np.min(trial_values),
        'max': np.max(trial_values),
    })

# Print table
print(f"{'n':>8} {'mean':>12} {'std':>12} {'mean*n':>12}")
for r in results:
    print(f"{r['n']:>8} {r['mean']:>12.6f} {r['std']:>12.6f} {r['mean']*r['n']:>12.6f}")

# Plot
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
ns_arr = [r['n'] for r in results]
means = [r['mean'] for r in results]

axes[0].loglog(ns_arr, means, 'o-', label='empirical mean')
axes[0].loglog(ns_arr, [1/n for n in ns_arr], '--', label='1/n reference')
axes[0].set_xlabel('n'); axes[0].set_ylabel('value'); axes[0].legend()
axes[0].set_title('Log-log: empirical vs 1/n')

axes[1].plot(ns_arr, [r['mean'] * r['n'] for r in results], 'o-')
axes[1].set_xlabel('n'); axes[1].set_ylabel('mean × n')
axes[1].set_title('Rescaled: should be constant if O(1/n)')

Path('simulations').mkdir(exist_ok=True)
plt.savefig('simulations/[CONJECTURE_ID]-scaling.png', dpi=150, bbox_inches='tight')
print("Plot saved: simulations/[CONJECTURE_ID]-scaling.png")
```

Adapt this template to the specific conjecture. Run the code.

**4. Interpret the output.**
- Does the numerical evidence support the conjecture?
- What is the apparent scaling? (Fit a power law if relevant: `np.polyfit(np.log(ns), np.log(means), 1)`)
- Are there outliers or regime changes?
- What parameter range was explored? Note any range where behaviour looks different.

**5. Surface patterns for conjecturing.**
If the experiment reveals something unexpected, name it. "The rescaled quantity converges but is not 1 — it appears to converge to π²/6." Unexpected convergence values are conjectures waiting to happen.

---

## Output

Save code to `simulations/[CONJECTURE_ID]-[description].py`.
Save plots to `simulations/[CONJECTURE_ID]-[description].png`.

Write a brief experiment summary to `simulations/[CONJECTURE_ID]-notes.md`:
- What was tested
- What the results show
- Apparent scaling or convergence value
- Any new patterns observed

Update `evidence_for` or `evidence_against` in research-state.yaml with a one-line summary and reference to the simulation file.

---

## Voice

Distinguish what the simulation shows from what it proves. "Numerics suggest O(1/n) scaling over n ∈ [10, 500]" is not the same as "the conjecture holds." Note the range and the sample size.

Flag near-misses: if the conjecture holds in 9,990 out of 10,000 trials, that's evidence against it, not for it.

---

## Completion

- **DONE** — experiment run, results saved, research-state.yaml updated
- **DONE_WITH_CONCERNS** — results are noisy or parameter range is too narrow to draw conclusions; state what larger experiment would be needed
- **NEEDS_CONTEXT** — the conjecture is not computable without more specifics (e.g. which norm, which random model)
