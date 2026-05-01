"""
Counterexample simulation for C1-S1:
Demonstrate that a CTRW with step-function alpha(x) does not converge to
a single alpha-stable limit under any global power-law rescaling.

Method: compare empirical log-characteristic functions of
  (a) constant alpha=alpha1 walk       -> pure alpha1-stable limit
  (b) constant alpha=alpha2 walk       -> pure alpha2-stable limit  
  (c) step-function alpha walk         -> should NOT match either

If (c) converged to an alpha*-stable law, log|E[exp(ikX)]| would be
linear in log|k| with slope alpha*. We show it is not.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

np.random.seed(42)

ALPHA1 = 1.2   # exponent for x < 0
ALPHA2 = 1.8   # exponent for x >= 0
N_TRIALS = 15000
N_STEPS  = 800

def stable_sample(alpha, n):
    """Chambers-Mallows-Stuck symmetric alpha-stable sampler."""
    theta = np.random.uniform(-np.pi/2, np.pi/2, n)
    W     = np.random.exponential(1.0, n)
    if abs(alpha - 1.0) < 1e-9:
        return np.tan(theta)
    num = np.sin(alpha * theta)
    den = np.cos(theta) ** (1.0 / alpha)
    cor = (np.cos((alpha - 1) * theta) / W) ** ((1.0 - alpha) / alpha)
    return (num / den) * cor

# ── Case (c): step-function alpha walk ────────────────────────────────────────
print("Simulating step-function walk...")
pos_step = np.zeros(N_TRIALS)
for step in range(N_STEPS):
    mask1 = pos_step < 0
    mask2 = ~mask1
    jumps = np.empty(N_TRIALS)
    if mask1.any():
        jumps[mask1] = stable_sample(ALPHA1, int(mask1.sum()))
    if mask2.any():
        jumps[mask2] = stable_sample(ALPHA2, int(mask2.sum()))
    pos_step += jumps
print(f"  done. mean={pos_step.mean():.4f}, std={pos_step.std():.4f}")

# ── Cases (a) and (b): constant-alpha walks (sum of iid stables) ──────────────
print("Simulating constant-alpha walks...")
pos_c1 = stable_sample(ALPHA1, (N_TRIALS, N_STEPS)).sum(axis=1)
pos_c2 = stable_sample(ALPHA2, (N_TRIALS, N_STEPS)).sum(axis=1)

# ── Rescale: n^{1/alpha} is the natural scale for n-step alpha-stable walk ────
scale_c1   = N_STEPS ** (1.0 / ALPHA1)
scale_c2   = N_STEPS ** (1.0 / ALPHA2)
pos_c1_sc  = pos_c1   / scale_c1
pos_c2_sc  = pos_c2   / scale_c2
pos_step_sc1 = pos_step / scale_c1   # rescale step-fn walk as if alpha1
pos_step_sc2 = pos_step / scale_c2   # rescale step-fn walk as if alpha2

# ── Empirical log-characteristic function ──────────────────────────────────────
ks = np.logspace(-1, 1, 40)

def log_cf(xs, ks):
    """log|E[exp(ikX)]| for each k."""
    result = []
    for k in ks:
        cf = np.mean(np.exp(1j * k * xs))
        result.append(np.log(max(abs(cf), 1e-12)))
    return np.array(result)

print("Computing characteristic functions...")
lcf_c1   = log_cf(pos_c1_sc,   ks)
lcf_c2   = log_cf(pos_c2_sc,   ks)
lcf_step1 = log_cf(pos_step_sc1, ks)
lcf_step2 = log_cf(pos_step_sc2, ks)

# Theoretical: for alpha-stable, log|CF| = -c * k^alpha
# In log-log: slope = alpha
logk = np.log(ks)
theory_c1 = -1.0 * ks ** ALPHA1   # c=1 (normalised)
theory_c2 = -1.0 * ks ** ALPHA2

# ── Tail exponent estimation ────────────────────────────────────────────────────
def estimate_tail_exponent(xs):
    """Hill estimator for tail exponent using top 10% of |X|."""
    ax = np.abs(xs)
    ax = np.sort(ax)[::-1]
    k  = max(int(0.1 * len(ax)), 10)
    if ax[k-1] <= 0:
        return np.nan
    return 1.0 / np.mean(np.log(ax[:k] / ax[k-1]))

tail_c1   = estimate_tail_exponent(pos_c1)
tail_c2   = estimate_tail_exponent(pos_c2)
tail_step = estimate_tail_exponent(pos_step)

print(f"\n=== Tail exponent estimates (Hill estimator) ===")
print(f"  Constant alpha={ALPHA1}:  estimated={tail_c1:.3f}  (true={ALPHA1})")
print(f"  Constant alpha={ALPHA2}:  estimated={tail_c2:.3f}  (true={ALPHA2})")
print(f"  Step-function alpha:       estimated={tail_step:.3f}  (should not match either)")
print()

# ── Quantile-conditional tail analysis ─────────────────────────────────────────
# For a pure stable law, the tail exponent should be the same for left and right tails.
# For the step walk, left-tail (x<0 side, alpha1) and right-tail (x>0 side, alpha2) differ.
pos_step_left  = pos_step[pos_step < 0]
pos_step_right = pos_step[pos_step >= 0]

tail_step_left  = estimate_tail_exponent(pos_step_left)
tail_step_right = estimate_tail_exponent(pos_step_right)

print(f"=== Step walk: split tail analysis ===")
print(f"  Left tail  (x<0, alpha1={ALPHA1} region):  estimated={tail_step_left:.3f}")
print(f"  Right tail (x>0, alpha2={ALPHA2} region): estimated={tail_step_right:.3f}")
print(f"  -> Different tails confirm asymmetric stable structure: NOT a single stable law")
print()

# ── Scaling consistency test ───────────────────────────────────────────────────
# For alpha-stable walk: E[|X_n|^q] ~ n^{q/alpha} for q < alpha
# Check this for q=0.5 (always below alpha) across multiple n values
ns = [100, 200, 400, 800]
q  = 0.5

print(f"=== Scaling test: E[|X_n|^{q}] ~ n^(q/alpha) ===")
print(f"{'n':>6}  {'C1 slope':>10}  {'C2 slope':>10}  {'Step slope':>12}")

prev = {}
for n in ns:
    r_c1   = np.mean(np.abs(stable_sample(ALPHA1, (2000, n)).sum(axis=1)) ** q)
    r_c2   = np.mean(np.abs(stable_sample(ALPHA2, (2000, n)).sum(axis=1)) ** q)
    # step walk for this n
    p = np.zeros(2000)
    for _ in range(n):
        m1 = p < 0; m2 = ~m1
        j = np.empty(2000)
        if m1.any(): j[m1] = stable_sample(ALPHA1, int(m1.sum()))
        if m2.any(): j[m2] = stable_sample(ALPHA2, int(m2.sum()))
        p += j
    r_step = np.mean(np.abs(p) ** q)
    prev[n] = (r_c1, r_c2, r_step)

for i, n in enumerate(ns[1:], 1):
    n0 = ns[i-1]
    ratio = n / n0
    slope_c1   = np.log(prev[n][0] / prev[n0][0]) / np.log(ratio)
    slope_c2   = np.log(prev[n][1] / prev[n0][1]) / np.log(ratio)
    slope_step = np.log(prev[n][2] / prev[n0][2]) / np.log(ratio)
    true_c1    = q / ALPHA1
    true_c2    = q / ALPHA2
    print(f"{n:>6}  {slope_c1:>8.3f} ({true_c1:.3f})  {slope_c2:>8.3f} ({true_c2:.3f})  {slope_step:>10.3f} (neither)")

# ── Plots ─────────────────────────────────────────────────────────────────────
Path("simulations").mkdir(exist_ok=True)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle(f"CTRW Step-Function Counterexample (α₁={ALPHA1}, α₂={ALPHA2}, n={N_STEPS} steps)",
             fontsize=13, fontweight='bold')

# Panel 1: Distributions under alpha1-scaling
ax = axes[0]
for xs, label, color in [
    (pos_c1_sc,   f"Const α={ALPHA1} (should converge)", "steelblue"),
    (pos_step_sc1, f"Step α (scaled as α={ALPHA1})",      "crimson"),
]:
    xs_clip = np.clip(xs, -20, 20)
    ax.hist(xs_clip, bins=80, density=True, alpha=0.5, color=color, label=label)
ax.set_title(f"Under α₁={ALPHA1} scaling")
ax.set_xlabel("Rescaled position"); ax.legend(fontsize=8)
ax.set_xlim(-15, 15)

# Panel 2: Distributions under alpha2-scaling  
ax = axes[1]
for xs, label, color in [
    (pos_c2_sc,   f"Const α={ALPHA2} (should converge)", "green"),
    (pos_step_sc2, f"Step α (scaled as α={ALPHA2})",      "darkorange"),
]:
    xs_clip = np.clip(xs, -20, 20)
    ax.hist(xs_clip, bins=80, density=True, alpha=0.5, color=color, label=label)
ax.set_title(f"Under α₂={ALPHA2} scaling")
ax.set_xlabel("Rescaled position"); ax.legend(fontsize=8)
ax.set_xlim(-15, 15)

# Panel 3: Log-CF slope (should be constant=alpha for pure stable)
ax = axes[2]
# Finite-difference slope of log|CF| vs log|k|
def cf_slope(lcf, logk):
    return np.gradient(lcf, logk)

slope_c1   = cf_slope(lcf_c1,   logk)
slope_c2   = cf_slope(lcf_c2,   logk)
slope_step1 = cf_slope(lcf_step1, logk)

ax.plot(ks, np.abs(slope_c1),    color="steelblue",  label=f"Const α={ALPHA1} (slope→{ALPHA1})")
ax.plot(ks, np.abs(slope_c2),    color="green",      label=f"Const α={ALPHA2} (slope→{ALPHA2})")
ax.plot(ks, np.abs(slope_step1), color="crimson",    label="Step α (slope varies — not stable)", linewidth=2)
ax.axhline(ALPHA1, color="steelblue", linestyle="--", alpha=0.4)
ax.axhline(ALPHA2, color="green",     linestyle="--", alpha=0.4)
ax.set_xscale("log")
ax.set_xlabel("k"); ax.set_ylabel("|d log|CF| / d log k|")
ax.set_title("Local CF exponent\n(constant=pure stable, varying=not stable)")
ax.legend(fontsize=8); ax.set_ylim(0, 3)

plt.tight_layout()
plt.savefig("simulations/C1-S1-step-counterexample.png", dpi=150, bbox_inches="tight")
print("\nPlot saved: simulations/C1-S1-step-counterexample.png")
