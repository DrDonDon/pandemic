# Proof Review — Adversarial Pass
# Date: 2026-04-10
# Reviewer role: hostile referee

Four rounds:
1. Logical/structural: does each step follow from the previous?
2. Technical: are the estimates correct?
3. Completeness: what is assumed vs proved?
4. Citation: are theorems invoked correctly?

---

## Draft 1: C1-S1-draft.tex (Necessity / Scale Mixture)

### PASS — overall sound for what it claims

**Scope is correct.** The draft proves a 1D marginal result for the rescaled
discrete-time walk at step n. It does NOT claim weak convergence in D([0,T],R),
which would require tightness + finite-dimensional convergence. The framing is
appropriate.

---

### Issue 1.1 — MINOR: CF convergence is conditional, unconditional step is implicit

The argument:
- Shows the *conditional* CF (given trajectory) converges to
  exp(−c₁(τₙ⁻/n)|k|^{α₁}) as n → ∞.
- Takes expectations and invokes bounded convergence.

**The gap**: the step "take expectations" requires that
  E[exp(−c₁(τₙ⁻/n)|k|^{α₁})] → E[exp(−c₁P|k|^{α₁})]
follows from τₙ⁻/n →ᵈ P. This uses:
  (a) g(p) = exp(−c₁p|k|^{α₁}) is bounded and continuous,
  (b) if τₙ⁻/n →ᵈ P then E[g(τₙ⁻/n)] → E[g(P)].

This is correct by the portmanteau theorem (or directly from weak convergence
of probability measures on [0,1]). **No error, but the step should be made
explicit in the write-up.**

---

### Issue 1.2 — MINOR: Proposition (not-stable) — α/α₁ > 1 case

The proof handles:
- α = α₁: requires L_P(s) = e^{−cs}, so P ~ Exp(c), contradicts P ∈ [0,1]. ✓
- α ≠ α₁: requires L_P to be the LT of an (α/α₁)-stable on (0,∞) with
  unbounded support, contradicts P ∈ [0,1]. ✓

**Imprecision for α/α₁ > 1**: e^{−cs^{α/α₁}} is NOT a valid Laplace transform
when α/α₁ > 1, because a Laplace transform must be completely monotone, and
e^{−cs^γ} is completely monotone iff γ ∈ (0,1]. So for α > α₁, the supposed
Laplace transform does not correspond to any distribution at all.

The proof should add: "For α > α₁, e^{−cs^{α/α₁}} is not a Laplace transform
(fails complete monotonicity for exponent > 1), so no such P exists." This
strengthens the argument.

**Fix needed**: split the case α/α₁ ∈ (0,1) (unbounded support) from
α/α₁ > 1 (not a valid LT). Both give the same conclusion but for different
reasons.

---

### Issue 1.3 — GENUINE GAP (correctly identified): G1-G2

The proof correctly flags G1 (does τₙ⁻/n converge?) and G2 (is the limit
non-degenerate?) as open. The simulation (Exp 2 in C1-S1-extended.py) gives
strong numerical evidence:
- Distribution stabilises in shape at n = 10000.
- KS fit: Beta(0.329, 0.873), lying between the two Bingham predictions.
- Non-degenerate: std ≈ 0.29.

**Proof strategy for G1-G2**: The occupation time for a random walk in a random
environment with position-dependent Lévy exponents can be handled via
fluctuation theory for Markov chains. The key tool is the Darling–Kac theorem
(Aaronson 1997, Theorem 2.4.2): for a null-recurrent Markov chain, the
occupation time fraction converges in distribution. Both the α₁ and α₂ regions
are null-recurrent (since α ∈ (1,2) for both), so the Darling–Kac theorem
should apply. The limit distribution is determined by the renewal sequence; for
the arc-sine case it gives Beta(1−1/α, 1/α).

**Recommended**: cite Darling–Kac (1957) and Bingham (1973) explicitly.
The asymmetric case likely gives a Beta(1−1/α₁, 1/α₁) × (some correction) or
a generalised arc-sine. This is the one remaining technical piece needed.

---

### Issue 1.4 — CONCERN: Step 5 (connection to PDE) is asserted, not proved

Point 3 in Section 4 says: "The CF is not of the form exp(−c|k|^{α(x)}) for
any function α(x) that is the characteristic exponent of the variable-order PDE."

This is stated but not derived. The argument would need to show that the
characteristic function of the scale-mixture process, as a *process* (not just
a 1D marginal), cannot satisfy any variable-order Kolmogorov equation. This
requires connecting the CF form to the PDE generator, which is a non-trivial
step.

**Assessment**: The draft correctly identifies this as contingent ("assuming
G1-G2, Proposition 1 establishes..."). For the paper, a sharper argument is
needed connecting the non-stable marginal distribution to failure of the PDE
characterisation (e.g., via the generator characterisation in Meerschaert-
Scheffler 2008).

---

## Draft 2: C1-gap2-uniqueness-draft.tex (Uniqueness via Levi parametrix)

### WARNING — two substantive technical errors

---

### Issue 2.1 — ERROR: Varying c(x) unaccounted in R-expand

Equation (R-expand) writes:
```
R(t,x,y) = c(x)∫(...)·|z|^{−1−α(x)} dz − c(y)∫(...)·|z|^{−1−α(y)} dz
```

The frozen operator L^(y) freezes BOTH c and α at y, so the second term
correctly uses c(y). The full operator uses c(x). The difference therefore has
TWO contributions:
1. The α-variation: c(y)[|z|^{−1−α(x)} − |z|^{−1−α(y)}]
2. The c-variation: [c(x)−c(y)]|z|^{−1−α(x)}

**The proof bounds only the α-variation term.** The c-variation term gives an
additional correction:
```
[c(x)−c(y)] ∫(f(x+z)−f(x)−f′(x)z·1_{|z|≤1}) |z|^{−1−α(x)} dz
= [c(x)−c(y)] · Lf(x)/c(x)
```

This term is bounded by |c(x)−c(y)| · C · ||f||_{C²}, which is small when c
is also Dini-continuous. **The proof implicitly requires c to also satisfy a
regularity condition (at minimum, Dini-continuity of c), which is not stated
in the theorem hypotheses.**

**Fix**: add hypothesis "c is Dini-continuous" (or Lipschitz, which implies
Dini), and add the c-variation bound to the R-bound proof. The conclusion is
the same (Dini on both α and c), but the hypothesis must be stated.

---

### Issue 2.2 — ERROR: Wrong derivative order in Taylor bound

Lemma R-bound proof (small jumps, |z| ≤ t^{1/α_min}):

> "Using |p^(0)(t,x+z,y)−p^(0)(t,x,y)−∂_x p^(0)·z| ≤ C|∂²_x p^(0)|·z²
> and (eq:grad)"

But **(eq:grad)** bounds |∂_x p^(0)| ≤ C·t·(t^{1/α} + |x−y|)^{−2−α₀}, which
is the *first* derivative. The Taylor remainder bound needs the *second*
derivative:
```
|∂²_x p^(0)(t,x,y)| ≤ C·t·(t^{1/α₀} + |x−y|)^{−3−α₀}
```
(standard estimate for α-stable densities, one extra power in the denominator).

**The bound as written cites eq:grad (first derivative) for a second-derivative
bound. The correct estimate has denominator exponent −3−α₀, not −2−α₀.**

Using the correct second-derivative bound, the small-jump integral becomes:
```
∫_{|z|≤t^{1/α_min}} z² · t · (t^{1/α_min}+|x−y|)^{−3−α_min} · ω_α(δ) · |log|z|| · |z|^{−1−α_min} dz
= t · (t^{1/α_min}+|x−y|)^{−3−α_min} · ω_α(δ) · ∫_0^{t^{1/α_min}} r^{1−α_min}|log r| dr
```

The z-integral evaluates to O(t^{(2−α_min)/α_min} · |log t|). Combined with
the prefactor t · (t^{1/α_min}+|x−y|)^{−3−α_min}:
- At |x−y| ~ t^{1/α_min}: O(ω_α · t^{1+(2−α_min)/α_min} · t^{−(3+α_min)/α_min}) = O(ω_α · t^{−1/α_min} · |log t|)

This differs from the claimed bound by the factor t^{−1/α_min} · |log t|.
**The R-bound in equation (R-bound) may have the wrong power law in t.**

**Consequence for Lemma Neumann**: The L1 bound of R (equation R-L1) is used
to establish Neumann series convergence. If the correct bound is:
```
∫_R |R(t,x,y)| dx ≤ C · ω_α(t^{1/α_min}) · t^{−1/α_min} · |log t|
```
then the Neumann series convergence condition becomes:
```
∫_0^T ω_α(t^{1/α_min}) t^{−1/α_min} dt < ∞
```
which after substitution u = t^{1/α_min} gives ∫_0^{T^{1/α_min}} ω_α(u) u^{α_min−2} du < ∞.
For α_min ∈ (1,2): this is ∫ ω_α(u) u^{α_min−2} du, which requires
ω_α(u) = o(u^{2−α_min}) — weaker than Dini but different from it.

**The Dini condition may still be sufficient** (since Dini implies ω_α(u) = o(u^ε)
for some ε > 0, and for α_min > 1 we need ε > 2−α_min > 0), but the
derivation as written does not correctly establish this. The intermediate
bound needs recomputation using the correct second-derivative estimate.

**Required action**: add the second-derivative estimate as a numbered equation
alongside (eq:upper) and (eq:grad), then redo the R-bound proof with it.

---

### Issue 2.3 — CONCERN: Neumann series induction (Lemma 4.2, proof)

The inductive bound:
```
I_n(t) = ∫_0^t ω_α(s^{1/α_min}) I_{n−1}(t−s) ds/s
```

The claim "Σ I_n(t) converges iff ∫_0^t ω_α(s^{1/α_min})/s ds < ∞" is
asserted but not proved. A complete proof would use the Gronwall inequality or
the Laplace-transform convolution method (standard in parametrix literature).

**Minor issue, but should be filled in for publication.**

---

### Issue 2.4 — CONCERN: Uniqueness proof (Theorem 5) too sketchy

The proof sketch omits:
1. Proof that ∫p(t,x,y)dy = 1 (mass conservation) — needs the parametrix
   kernel to integrate to 1 in y.
2. Proof of the semigroup property P_{t+s} = P_t P_s.
3. The step "any solution to the martingale problem has the same one-dimensional
   distributions" — needs a duality/test-function argument.

These are standard but non-trivial steps. The current proof is a sketch that
would need fleshing out for a complete paper. **Acceptable for a preprint with
"proof sketch" labelled; needs completion for journal submission.**

---

### Issue 2.5 — NOTE: Conjecture 6.1 (C⁰ insufficient) is evidence only

The conjecture that C⁰ alone is insufficient is supported by:
1. Divergence of the parametrix series for ω_α(r) = |log r|^{−1}.
2. Analogy with De Giorgi (1957) for elliptic PDEs.
3. Schilling–Wang (2012) examples.

**None of these directly proves that the martingale problem has non-unique
solutions.** Failure of the parametrix construction does not imply failure of
uniqueness — the parametrix is a sufficient condition tool, not necessary. The
conjecture remains open and correctly labelled as such.

---

## Draft 3: C1-sufficiency-draft.tex (Sufficiency Direction)

### PASS with two errors and two concerns

---

### Issue 3.1 — NOTATION ERROR: C³ vs C² in Proposition 2

Proposition 2 (Equicontinuity) states f ∈ C³_c(R) in the hypothesis but the
proof uses only ||f||_{C²}. The bound derived is:
```
|Lf(x) − L^{x₀}f(x)| ≤ C · ω_α(δ) · ||f||_{C²}
```

The C³_c hypothesis is not used and should be C²_c. **Fix: change C³_c to C²_c
in the proposition statement.**

---

### Issue 3.2 — CONCERN: Tightness (Step 3) does not handle β(x)

The tightness proof handles the spatial walk (position jumps only). The modulus
of continuity estimate:
```
P(|X^ε(t+δ) − X^ε(t)| > η) ≤ Cδ/η^{α_min}
```
is derived from "O(δ/ε) jumps of size O(ε^{1/α_min})". This argument treats the
number of jumps in a time interval as deterministic (O(δ/ε)), which is only
valid if the waiting times are deterministic (constant = ε).

**For the CTRW with β(x)-stable waiting times**: the number of jumps in [t,t+δ]
is random and heavy-tailed. The correct argument uses the fact that the process
is time-changed by an inverse β(x)-stable subordinator. Tightness of the
time-changed process follows from tightness of:
1. The spatial walk (already shown), AND
2. The time-change process (the inverse subordinator), which is tight because
   it is increasing and has locally finite variation.

The Straka–Henry (2011) framework (or Whitt 2002, Section 13.6) gives the
correct tool: if X^ε → X and T^ε → T and T is continuous, then X^ε∘T^ε → X∘T.
The inverse subordinator is continuous a.s., so the composition is tight.

**The current tightness proof is incorrect for the CTRW.** A separate argument
for the time-change is needed. This is a gap, not a minor issue.

---

### Issue 3.3 — CONCERN: Step 4 proof cites Proposition 2 unnecessarily

Lemma 1 shows L^ε f(x) = L f(x) **exactly** (the difference is 0 by symmetry).
Therefore in Step 4:
```
|∫_s^t L^ε f(X^ε(u)) − Lf(X^ε(u)) du| = 0
```
exactly, not approximately. No continuity bound (Proposition 2) is needed here.

The draft's Step 4 proof says "by Lemma 1 (equals 0) plus the continuity bound
from Proposition 2" — the second clause is superfluous. **Fix: remove the
reference to Proposition 2 from this step.** (Proposition 2 is used in the
tightness argument, not here.)

---

### Issue 3.4 — GAP (correctly identified): β(x) component

The time-fractional component is deferred to "the Straka (2018) bivariate
Langevin framework extended to the space-fractional case." This is the right
reference but the extension to space-fractional variable order is genuinely
non-trivial. The Straka (2018) paper handles variable β(x) but with FIXED α.
Allowing variable α(x) simultaneously is not in the literature.

**This is a genuine open piece.** The sufficiency proof as written is for the
spatial (α-only) component only. The full claim (α and β both varying) needs
the bivariate framework.

---

## Cross-draft issues

### Issue X.1 — Circular reference: Sufficiency uses Gap 2 uses Levi parametrix

The chain is:
- Sufficiency (Step 5) → Gap 2 (Theorem 5, uniqueness)
- Gap 2 (Theorem 5) → Levi parametrix → Neumann series convergence
- Neumann series convergence → R-bound (Issues 2.1, 2.2 above)

The errors in Issues 2.1–2.2 propagate through: if the R-bound is off, the
Dini condition in Gap 2 may not be the correct threshold, and the "sufficiency
under Dini" claim in the sufficiency proof inherits the uncertainty.

**The sufficiency and uniqueness proofs stand or fall together. Fixing Issues
2.1–2.2 is the highest priority.**

### Issue X.2 — Revised C1'' statement consistency

The revised conjecture C1'' says:
> "Converges to variable-order PDE solution **iff** α and β are Dini-continuous."

- Sufficiency: proved modulo Gap 2 concerns (Dini on α sufficient).
- Necessity: proved that step-function (discontinuous) α gives wrong limit.
- Sharp threshold: Dini identified as sharp via Gap 2.
- The "iff" for β is analogous but relies on Exp 4 (numerical only) plus
  the Gap 2 argument applied separately. No rigorous necessity for β is proved.

**C1'' as stated is supported for the α direction. The β direction of necessity
is currently numerical evidence only (Exp 4).**

---

## Priority list

| Priority | Action |
|----------|--------|
| P1 (MUST FIX) | Add second-derivative estimate to Gap 2 and redo R-bound |
| P1 (MUST FIX) | Add Dini-on-c hypothesis to Gap 2 and bound c-variation term |
| P2 (MUST FIX) | Fix tightness proof in Sufficiency to handle β(x) time-change |
| P2 (SHOULD FIX) | Add Darling–Kac citation and strategy for G1-G2 in S1 draft |
| P3 (CLEAN UP) | Change C³_c → C²_c in Sufficiency Proposition 2 |
| P3 (CLEAN UP) | Remove spurious Prop 2 reference from Step 4 of Sufficiency |
| P3 (CLEAN UP) | Add complete monotonicity argument for α/α₁ > 1 in S1 Prop 1 |
| P4 (PAPER) | Flesh out uniqueness sketch (Theorem 5, Gap 2) for submission |
| P4 (PAPER) | Extend necessity for β direction beyond Exp 4 numerics |

---

## Overall assessment

The three-draft proof system has **correct architecture**:
- Necessity (S1): scale mixture argument is sound modulo G1-G2.
- Uniqueness (Gap 2): Levi parametrix is the right tool; the Dini threshold is
  correctly identified; but the technical execution has two errors that need
  fixing before the proof is watertight.
- Sufficiency: generator convergence argument is correct; tightness has a
  genuine gap for the time-change component.

**The conjecture C1'' is well-supported and the proof strategy is sound.** The
main remaining work is (1) fixing the R-bound calculation in Gap 2, (2) closing
G1-G2 via Darling–Kac, and (3) the β(x) tightness argument.

These are research-level difficulties, not fatal flaws. The paper is publishable
in its current form as a "results with open questions" preprint. A complete
proof would take another sprint to close G1-G2 and fix P1 issues.
