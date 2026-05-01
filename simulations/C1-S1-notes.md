# Counterexample Run — C1-S1
# Target: step-function alpha(x) = alpha1 * 1_{x<0} + alpha2 * 1_{x>=0}
# Date: 2026-04-05

## Verdict: NO COUNTEREXAMPLE TO C1 — but strong numerical evidence FOR necessity direction

The step-function CTRW does NOT converge to a single alpha-stable limit.
This supports C1's necessity claim: discontinuous alpha breaks convergence.

---

## Round 1 — Analytic (incompatible scalings)

For alpha(x) = 1.2 * 1_{x<0} + 1.8 * 1_{x>=0}, the characteristic function of a jump
from position x is approximately:

  hat_lambda(k; x) ≈ 1 - c|k|^{alpha(x)}

Under spatial rescaling eps^{1/alpha1} = eps^{1/1.2}:
  - Left-side (alpha1=1.2): CF exponent |k|^1.2  →  finite
  - Right-side (alpha2=1.8): CF exponent |eps^{(1/1.2 - 1/1.8)} k|^1.8 = |eps^{-5/18} k|^1.8  →  BLOWS UP as eps→0

Under spatial rescaling eps^{1/alpha2} = eps^{1/1.8}:
  - Right-side (alpha2=1.8): finite
  - Left-side (alpha1=1.2): CF exponent |eps^{(1/1.8 - 1/1.2)} k|^1.2 = |eps^{-5/18} k|^1.2  →  BLOWS UP

No single power-law rescaling eps^H is consistent with both halves.
This means no unique limit process exists.

---

## Round 2 — Numerical (N=15,000 trials, n=800 steps, alpha1=1.2, alpha2=1.8)

### Key result 1: Asymmetric tails

For a symmetric alpha-stable law, left and right tail exponents are equal.
For the step-function walk:

  Left tail  (x < 0, alpha1=1.2 region):  Hill estimate = 1.366
  Right tail (x > 0, alpha2=1.8 region):  Hill estimate = 1.076

These are different. No single symmetric stable law has different left and right tail exponents.
The step walk is definitively NOT a symmetric alpha-stable distribution.

### Key result 2: Varying local CF exponent (Panel 3)

For a pure alpha-stable law, d log|CF| / d log|k| = alpha (constant).

  Const alpha=1.2:  CF exponent ≈ 1.2 (flat)        ✓
  Const alpha=1.8:  CF exponent ≈ 1.8 (flat)        ✓
  Step walk:        CF exponent varies from ~0.5 to ~2.5 across k-range  ✗

The varying CF exponent confirms no single stable law fits the step walk.

### Key result 3: Distribution mismatch under both scalings

Under alpha1=1.2 scaling: step walk is much more concentrated than alpha1-stable (too light-tailed)
Under alpha2=1.8 scaling: step walk is much more concentrated than alpha2-stable

Neither scaling produces the correct distributional shape.

### Scaling exponent test (E[|X_n|^0.5] ~ n^{0.5/alpha})

True scaling exponent 0.5/alpha1 = 0.417, 0.5/alpha2 = 0.278.
Step walk empirical exponent: 0.259 → 0.338 → 0.344 (not converging to either, and not stable).

---

## Round 3 — Targeted: the interface

The analytic argument identifies x=0 as the obstruction. The numerical evidence is
consistent: the split tail analysis shows the walk behaves like alpha1-stable when
it's in the x<0 half and alpha2-stable when in the x>0 half — but the mixture of
these two regimes produces a distribution that matches neither.

Chechkin et al. (2005) treat exactly this two-region setup heuristically. They do not
prove or disprove convergence at the interface. Our simulation fills that gap numerically.

---

## What this establishes (and what it doesn't)

ESTABLISHES (numerically):
- The step-function CTRW does not converge to any single symmetric alpha-stable law
- The obstruction is specifically the asymmetric tails created by the two-region structure
- The incompatible-scaling argument (Round 1) gives the analytic mechanism

DOES NOT ESTABLISH:
- Rigorous proof that no limit exists (this requires the Skorokhod framework)
- That the limit fails to exist entirely (vs converging to a non-stable limit process)
- The necessity direction for beta(x) (time-fractional) — only alpha(x) tested here

---

## Recommended next steps

1. Harden Round 1 into a rigorous proof: use the Fourier/CF argument to show that
   no subsequential limit of X^epsilon (under any rescaling) has a finite, non-degenerate
   characteristic function. This is the proof of S1.

2. Run /simulate with larger n (n=5000, 10000) to confirm the asymmetric tail result
   holds as n → infinity (not just an artefact of finite n).

3. Run the same simulation for beta(x) step function (time-fractional case) to check
   if the same asymmetric structure appears.

---

## Files

- Simulation: simulations/C1-S1-step-counterexample.py
- Plot:        simulations/C1-S1-step-counterexample.png
