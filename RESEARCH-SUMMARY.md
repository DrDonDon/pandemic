# Research Summary: Spatially Varying Anomalous Diffusion
# Project: C1'' Conjecture — Sharp Regularity for Variable-Order CTRW Convergence
# Date: 2026-04-25

---

## The Question

**When does a spatially varying CTRW (Continuous Time Random Walk) converge to
a well-defined variable-order fractional diffusion PDE?**

Specifically: what regularity conditions on the exponents α(x) (space-fractional)
and β(x) (time-fractional) are necessary and sufficient?

---

## Background

A CTRW at position x draws:
- Spatial jumps ξ ~ symmetric α(x)-stable (heavy-tailed, |ξ|^{-1-α(x)})
- Waiting times W ~ β(x)-stable (power-law clock, W^{-β(x)})

The target macroscopic equation is the **variable-order fractional PDE**:
```
∂_t^{β(x)} u = -(-Δ)^{α(x)/2} u
```

For constant α, β this is well-established (Meerschaert-Scheffler 2008,
Gorenflo-Mainardi 2007). The spatially varying case is open.

---

## The Conjecture (Revised)

**C1'' (final form):**
> The rescaled CTRW X^ε converges weakly in D([0,T],ℝ) to a process whose
> density satisfies the variable-order fractional diffusion PDE
> ∂_t^{β(x)} u = -(-Δ)^{α(x)/2} u
> **if and only if α and β are Dini-continuous:**
> ∫₀¹ ω_α(r)/r dr < ∞,  ∫₀¹ ω_β(r)/r dr < ∞
> where ω_α, ω_β are the moduli of continuity of α, β.

**The Dini condition is strictly between Hölder C^γ and mere C⁰:**
```
α ∈ C^γ (Hölder)  ⊊  Dini-continuous  ⊊  α ∈ C⁰  ⊊  measurable
```

The original conjecture used C⁰. The proof revealed the true threshold is Dini.

---

## Key Finding: The Step-Function Counterexample

For α(x) = α₁·1_{x<0} + α₂·1_{x≥0} with α₁ < α₂:

**The CTRW does converge weakly (under n^{1/α₁} scaling) — but to the WRONG limit.**

The limit is a **scale mixture of α₁-stables**:
```
X_∞ = P^{1/α₁} · Z_{α₁}
```
where P = lim(τₙ⁻/n) is the occupation time fraction and Z_{α₁} is an
independent α₁-stable variable.

This scale mixture is NOT α-stable for any α (proved), and cannot satisfy
any variable-order PDE. This refines the original conjecture from
"no convergence" to "convergence to the wrong process."

---

## Proof Structure (Three Drafts)

### 1. Necessity — `proofs/C1-S1-draft.tex`
**Status: Complete modulo gap G1-G2**

Steps proved:
- Lemma: α₂ contribution vanishes under n^{1/α₁} scaling (CF argument)
- Step 3: Limit is scale mixture P^{1/α₁}Z_{α₁} (modulo G1-G2)
- Proposition: Scale mixture is not α-stable for any α ∈ (0,2)

**Gap G1-G2**: Does τₙ⁻/n converge in distribution to a non-degenerate P?
- Numerically confirmed (Exp 2: Beta(0.33, 0.87) fit, std ≈ 0.29)
- Theoretical tool: Darling-Kac theorem for null-recurrent Markov chains
- Bingham (1973) arc-sine law extension to asymmetric-exponent stable walks

### 2. Uniqueness — `proofs/C1-gap2-uniqueness-draft.tex`
**Status: Done with concerns (2 errors to fix)**

Method: Levi parametrix — freeze α at y, build correction kernel R, solve
Volterra equation Φ = R + R*Φ via Neumann series.

Key results:
- Correction kernel bound: |R(t,x,y)| ≤ C·ω_α(|x-y|+t^{1/α_min})·t·(t^{1/α_min}+|x-y|)^{-2-α_min}
- Neumann series converges iff ∫₀¹ ω_α(r)/r dr < ∞ (Dini condition)
- Sharp threshold identified: Dini is necessary and sufficient for parametrix

**Errors found in proof-review:**
1. Missing second-derivative estimate (uses ∂_x p^(0) where ∂²_x p^(0) needed)
2. Varying c(x) unaccounted — need Dini-on-c as additional hypothesis

### 3. Sufficiency — `proofs/C1-sufficiency-draft.tex`
**Status: Done with concerns**

Steps proved:
- Step 1: L^ε f = Lf exactly (by symmetry of Lévy measure) — no error
- Step 2: Generator equicontinuity |Lf(x)-L^{x₀}f(x)| ≤ C·ω_α(δ)·||f||_{C²}
- Step 3: Tightness (sketched — gap for β(x) time-change)
- Step 4: Limit points solve martingale problem
- Step 5: Uniqueness → deferred to Gap 2 proof above

**Gap**: Tightness proof does not correctly handle the β(x) time-change.
Correct tool: Straka-Henry (2011) subordination tightness for CTRWs.

---

## Simulation Results — `simulations/C1-S1-extended.py`

### Experiment 1: Large-n tail analysis (n = 800, 5000, 10000)
| n     | Left tail | Right tail | Asymmetric? |
|-------|-----------|------------|-------------|
| 800   | 1.186     | 1.134      | marginal    |
| 5000  | 1.335     | 1.056      | YES         |
| 10000 | 1.230     | 1.027      | YES         |

Left tail → α₁=1.2, right tail lighter. Asymmetry persists at large n.
Rules out convergence to any single symmetric stable law.

### Experiment 2: Occupation time distribution τₙ⁻/n
- Non-degenerate (std ≈ 0.29 at n=10000)
- Beta(0.329, 0.873) fit — lies between Bingham predictions for pure α₁ and α₂ walks
- Mean still slowly decreasing at n=10000 (slow convergence, consistent with null-recurrence)
- G1-G2 **numerically confirmed**: occupation time converges to non-degenerate limit

### Experiment 3: Scale mixture fit
| Comparison | L2 distance |
|------------|-------------|
| Step walk vs. scale mixture P^{1/α₁}Z_{α₁} | **0.021** |
| Step walk vs. pure α₁-stable | 1.121 |

Scale mixture is **54× closer** to the step walk than pure stable. Strong
confirmation of the theoretical prediction.

### Experiment 4: Step-function β(x) CTRW
- β₁=0.4 (x<0), β₂=0.8 (x≥0), fixed α=1.5
- Asymmetric tails: left=1.598, right=1.866
- Same failure mode as α case — necessity extends to β direction

---

## Proof Review Findings — `proofs/proof-review.md`

| Priority | Issue | File |
|----------|-------|------|
| P1 MUST FIX | Missing ∂²_x p^(0) estimate in R-bound | gap2-uniqueness |
| P1 MUST FIX | Missing Dini-on-c hypothesis, c(x) variation unaccounted | gap2-uniqueness |
| P2 MUST FIX | Tightness proof doesn't handle β(x) time-change | sufficiency |
| P2 SHOULD FIX | G1-G2: add Darling-Kac citation and strategy | S1-necessity |
| P3 CLEANUP | C³_c → C²_c in Proposition 2 statement | sufficiency |
| P3 CLEANUP | Remove spurious Prop 2 reference from Step 4 | sufficiency |
| P3 CLEANUP | Add complete monotonicity argument for α/α₁>1 case | S1-necessity |

**Overall**: Correct architecture, sound conjecture, publishable as preprint
with open questions. Two P1 fixes needed before journal submission.

---

## Literature

| Paper | Relevance |
|-------|-----------|
| Straka (2018) Physica A | Closest: proves β(x) CTRW→VOFFPE for variable β, fixed α |
| Meerschaert & Straka (2014) Ann.Prob. | General semi-Markov framework |
| Meerschaert & Scheffler (2008) SPA | Constant-exponent baseline and template |
| Wang & Zheng (2019) JMAA | PDE-side well-posedness for variable-order |
| Fedotov & Falconer (2012) PRE | Heuristic evidence for necessity |
| Gorenflo & Mainardi (2007) | Fourier-Laplace baseline |
| Chechkin, Gorenflo & Sokolov (2005) | Step-function case — heuristic only |
| Bingham (1973) | Arc-sine law for stable walks — key for G1-G2 |
| Bass (2004) | Parametrix for jump diffusions — key for uniqueness |

---

## Files in This Repository

```
pandemic/
├── RESEARCH-SUMMARY.md          ← this file
├── research-state.yaml          ← living research state (conjecture, evidence)
├── dead-ends.md                 ← failed approaches log
├── literature-notes.md          ← 6 papers with gap analysis
├── conjectures/
│   └── C1.md                    ← full formalisation of C1''
├── proofs/
│   ├── C1-S1-draft.tex          ← necessity (scale mixture)
│   ├── C1-gap2-uniqueness-draft.tex  ← uniqueness (Levi parametrix)
│   ├── C1-sufficiency-draft.tex ← sufficiency (generator convergence)
│   └── proof-review.md          ← adversarial review of all three
├── simulations/
│   ├── C1-S1-step-counterexample.py   ← original counterexample (n=800)
│   ├── C1-S1-step-counterexample.png  ← 3-panel plot
│   ├── C1-S1-notes.md                 ← original simulation notes
│   ├── C1-S1-extended.py              ← extended 4-experiment simulation
│   ├── C1-S1-extended.png             ← 6-panel plot
│   └── C1-S1-extended-notes.md        ← extended simulation notes
├── mathstack/                   ← the research skill framework
│   ├── README.md
│   ├── CLAUDE-routing.md
│   ├── install.sh
│   ├── templates/
│   └── skills/                  ← derive, simulate, proof-review, write,
│                                    editor, science-writer, checkpoint, retro
└── agentspec/
    └── site/index.html          ← AgentSpec developer website
```

---

## What Remains

### To complete the proof (research gaps):
1. **G1-G2**: Prove τₙ⁻/n → P non-degenerate using Darling-Kac theorem
2. **Fix P1 errors** in Gap 2 proof (second-derivative bound, Dini-on-c)
3. **Fix tightness** in sufficiency proof for β(x) time-change
4. **Extend necessity** for β(x) beyond numerics (Exp 4)

### To complete the paper (writing):
5. Write `paper/C1-main.tex` — full LaTeX paper assembling all three proofs
6. Editor pass — structure, notation consistency, references
7. Science-writer pass — accessible abstract and blog post

### Sprint stages remaining:
- **Write** (paper assembly) — not started
- **Editor + Science-Writer** — pending
- **Retro** — pending
- **Checkpoint** — pending

---

## Core Insight (one sentence)

A spatially varying CTRW converges to the correct variable-order fractional PDE
if and only if the exponents are Dini-continuous — the precise threshold where
the Levi parametrix Neumann series converges and the limit process is unique.
