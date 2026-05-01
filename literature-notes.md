# Literature Notes — Spatially Varying Anomalous Diffusion
# Conjecture C1: continuity of alpha(x), beta(x) as threshold for CTRW convergence
# Scout run: 2026-04-04

---

## What the field currently knows

The CTRW-to-fractional-PDE correspondence is well-established for **constant** exponents
(Meerschaert & Scheffler 2008; Gorenflo & Mainardi 2007). The spatially varying case is
substantially less settled. There are three clusters of results:

**Cluster 1 — Rigorous CTRW convergence, constant exponents.**
The foundational machinery (triangular array limits, Skorokhod convergence, time-changed
Lévy processes) is complete. These results are prerequisites but do not address the variable
exponent case.

**Cluster 2 — Variable beta(x), time-fractional only, CTRW side.**
Straka (2018) is the closest paper to C1. He rigorously derives VOFFPEs from CTRWs with
position-dependent beta(x) via a bivariate Langevin representation. This is a genuine
CTRW→PDE convergence result for spatially varying exponents — but time-fractional only.
The space-fractional (alpha(x)) case is not treated. The exact regularity assumed on beta(x)
is not stated in the abstract; it appears to require smoothness for the Langevin SDE to be
well-posed, but the precise threshold is not identified as a result.

**Cluster 3 — Variable-order PDE well-posedness, no CTRW.**
Wang & Zheng (2019) prove well-posedness for variable-order time-fractional diffusion PDEs.
Critically: their regularity condition is on the **temporal** behavior of the order function
at t=0, not on its spatial regularity. This suggests the spatial and temporal regularity
requirements may be decoupled — relevant to C1 but from the PDE side only.

---

## The 6 most important papers

### 1. Straka (2018) ★★★ CLOSEST TO C1
**Citation:** P. Straka, "Variable Order Fractional Fokker-Planck Equations derived from
Continuous Time Random Walks," *Physica A* 503:451-463. arXiv:1712.06767.

**What was proved:** VOFFPEs with position-dependent fractional order beta(x) are rigorously
derived as governing equations for the probability densities of scaling limits of spatially
inhomogeneous CTRWs with beta(x)-stable waiting time distributions. Convergence via weak
convergence of the bivariate Langevin process.

**Key assumptions:** beta(x) in (0,1) pointwise, spatially varying; drift and diffusion
coefficients smooth enough for Langevin SDE well-posedness. Exact smoothness threshold
on beta(x) not stated as a theorem.

**What was left open:** Space-fractional case (alpha(x) varying). Necessity direction
(discontinuous beta). Sharp regularity threshold on beta(x).

**How it relates to C1:** Proves sufficiency direction for beta(x), time-fractional only.
The sufficiency half of C1 for beta(x) may follow from this work. The space-fractional
alpha(x) case and the necessity direction are fully open.

---

### 2. Meerschaert & Straka (2014) ★★★
**Citation:** M.M. Meerschaert and P. Straka, "Semi-Markov approach to continuous time
random walk limit processes," *Annals of Probability* 42(4):1699-1723. arXiv:1206.1960.

**What was proved:** General semi-Markov theory for CTRW limits with coupled, space-time
dependent jump and waiting time distributions. Rigorous weak convergence in Skorokhod J1
topology. Explicit transition kernels for all finite-dimensional distributions.

**Key assumptions:** Heavy-tailed waiting times (infinite mean); space-time dependent
coupling allowed. Regularity conditions on the space-dependence are present but the
focus is on the general framework, not the sharp threshold.

**What was left open:** The sharp regularity threshold for spatial variation. Whether
discontinuous exponents cause convergence failure.

**How it relates to C1:** The framework accommodates spatially varying parameters in
principle. C1's necessity direction (discontinuous alpha fails) is not addressed.

---

### 3. Meerschaert & Scheffler (2008) ★★ FOUNDATIONAL
**Citation:** M.M. Meerschaert and H.-P. Scheffler, "Triangular array limits for
continuous time random walks," *Stochastic Processes and their Applications*
118:1606-1633.

**What was proved:** Functional limit theorems for CTRWs via triangular arrays.
The CTRW limit is a Lévy process time-changed by the hitting time of a subordinator.
Densities solve space-time fractional diffusion equations.

**Key assumptions:** Constant exponents. Power-law tails for both jumps and waiting times.

**How it relates to C1:** The baseline constant-exponent result. Proof strategy for C1
likely extends this via a localisation argument.

---

### 4. Wang & Zheng (2019) ★★ PDE SIDE
**Citation:** H. Wang and X. Zheng, "Wellposedness and regularity of the variable-order
time-fractional diffusion equations," *J. Math. Anal. Appl.* 475:1778-1802.

**What was proved:** Well-posedness of variable-order time-fractional diffusion PDEs in
multiple space dimensions. Solution has full regularity if the variable order has an
integer limit at t=0; exhibits singularities otherwise.

**Key finding relevant to C1:** The critical regularity condition is on the **temporal**
behavior of the order function at t=0, not on its spatial smoothness. This suggests
spatial regularity of alpha(x) may be a separate (and possibly weaker) condition.

**How it relates to C1:** PDE-side evidence that the sharp threshold may differ between
temporal and spatial variation. Does not address CTRW convergence.

---

### 5. Fedotov & Falconer (2012) ★★
**Citation:** S. Fedotov and S. Falconer, "Subdiffusive master equation with
space-dependent anomalous exponent and structural instability," *Phys. Rev. E* 85:031132.

**What was proved (rigorously):** The constant-exponent fractional Fokker-Planck equation
is structurally unstable — small spatial variation in mu(x) destroys the
Gibbs-Boltzmann stationary distribution and causes anomalous aggregation.

**What was derived (heuristically):** Master equation for CTRW with space-dependent
mu(x) via generating function / mean-field approach. Not a Skorokhod convergence proof.

**How it relates to C1:** The structural instability result is evidence that discontinuous
or rapidly varying beta(x) causes qualitative changes in behaviour — indirect support for
the necessity direction of C1.

---

### 6. Gorenflo & Mainardi (2007) ★ BACKGROUND
**Citation:** R. Gorenflo and F. Mainardi, "Continuous time random walk, Mittag-Leffler
waiting time and fractional diffusion: mathematical aspects," arXiv:0705.0797.

**What was proved:** Rigorous equivalence (via Fourier-Laplace) between power-law
waiting-time CTRWs and the time-fractional diffusion equation. Constant exponents only.

**How it relates to C1:** Foundation for the Fourier-Laplace approach; constant-exponent
baseline.

---

## Identified gaps (the open problems relevant to C1)

**Gap 1 — Space-fractional, CTRW side (OPEN).**
No paper treats the case where the SPACE-fractional exponent alpha(x) varies with
position in the CTRW→PDE convergence framework. Straka (2018) treats beta(x) only.
This is the primary open direction for C1.

**Gap 2 — Necessity direction (OPEN).**
No paper proves that discontinuous alpha or beta causes convergence failure. The
step-function counterexample (C1-S1) appears to be completely unaddressed.

**Gap 3 — Sharp regularity threshold (OPEN).**
No paper identifies the precise regularity class (C^0, Holder C^gamma, Lipschitz, C^1)
needed for convergence. Straka (2018) implicitly uses smoothness but does not
characterise the threshold.

**Gap 4 — Decoupling of alpha and beta regularity (OPEN).**
Wang & Zheng (2019) suggest spatial and temporal regularity requirements may differ.
Whether the regularity requirements on alpha(x) and beta(x) are independent in the
CTRW setting is not addressed anywhere.

---

## Assessment for C1

The sufficiency direction for beta(x) (time-fractional) is largely covered by Straka (2018).
The following components of C1 appear to be genuinely open:

| Component | Status |
|---|---|
| Sufficiency: alpha(x) in C^0, space-fractional | OPEN |
| Necessity: discontinuous alpha(x) fails | OPEN |
| Necessity: discontinuous beta(x) fails | OPEN |
| Sharp threshold (C^0 vs Holder) | OPEN |
| Decoupling of alpha and beta conditions | OPEN |

**Recommended priority:** Gap 2 (necessity — step-function counterexample). It is the
most self-contained, requires no new operator theory, and if proved establishes that
C1 is asking the right question.

**Key paper to read in full:** Straka (2018) arXiv:1712.06767 — the exact regularity
assumed on beta(x) in the Langevin SDE step will determine whether C1's sufficiency
direction for beta(x) is already settled or still requires work.
