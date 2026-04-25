"""
Probability & stochastic processes toolkit.
Monte Carlo, SDEs, Markov chains, empirical distributions.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def sde_euler_maruyama(drift, diffusion, y0, t_span, dt=1e-3, n_paths=1):
    """
    Simulate SDE:  dX = drift(t, X) dt + diffusion(t, X) dW

    Returns (t, paths) where paths.shape = (n_paths, len(t), dim)
    """
    t = np.arange(t_span[0], t_span[1], dt)
    dim = len(y0) if hasattr(y0, "__len__") else 1
    y0 = np.atleast_1d(y0)

    paths = np.zeros((n_paths, len(t), dim))
    paths[:, 0, :] = y0

    for i in range(1, len(t)):
        X = paths[:, i - 1, :]          # (n_paths, dim)
        dW = np.random.randn(n_paths, dim) * np.sqrt(dt)
        mu = np.array([drift(t[i - 1], X[k]) for k in range(n_paths)])
        sigma = np.array([diffusion(t[i - 1], X[k]) for k in range(n_paths)])
        paths[:, i, :] = X + mu * dt + sigma * dW

    return t, paths


def plot_sde_paths(t, paths, title="SDE Paths", dim=0, n_show=None, show_mean=True):
    """Plot sample paths + mean for one dimension."""
    fig, ax = plt.subplots(figsize=(10, 5))
    n_show = n_show or min(50, paths.shape[0])
    for k in range(n_show):
        ax.plot(t, paths[k, :, dim], alpha=0.2, linewidth=0.6, color="steelblue")
    if show_mean:
        ax.plot(t, paths[:, :, dim].mean(axis=0), "r-", linewidth=2, label="Mean")
        ax.legend()
    ax.set_title(title)
    ax.set_xlabel("t")
    plt.tight_layout()
    return fig


def monte_carlo(f, n_samples=100_000, seed=None):
    """
    Generic Monte Carlo integrator.
    f(samples) where samples ~ U[0,1]^d
    Returns (estimate, std_error)
    """
    rng = np.random.default_rng(seed)
    samples = rng.random(n_samples)
    vals = f(samples)
    return vals.mean(), vals.std() / np.sqrt(n_samples)


def markov_chain(transition_matrix, n_steps, start_state=0):
    """Simulate a discrete Markov chain. Returns state sequence."""
    P = np.array(transition_matrix)
    n_states = P.shape[0]
    states = [start_state]
    for _ in range(n_steps - 1):
        states.append(np.random.choice(n_states, p=P[states[-1]]))
    return np.array(states)


def stationary_distribution(transition_matrix):
    """Compute stationary distribution via left eigenvector."""
    P = np.array(transition_matrix, dtype=float)
    vals, vecs = np.linalg.eig(P.T)
    idx = np.argmin(np.abs(vals - 1.0))
    pi = np.real(vecs[:, idx])
    return pi / pi.sum()


def empirical_density(samples, bins=50, fit_dist=None):
    """Plot histogram + optional distribution fit."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(samples, bins=bins, density=True, alpha=0.6, color="steelblue", label="Empirical")
    if fit_dist is not None:
        params = fit_dist.fit(samples)
        x = np.linspace(samples.min(), samples.max(), 300)
        ax.plot(x, fit_dist.pdf(x, *params), "r-", linewidth=2,
                label=f"Fit: {fit_dist.name}")
        ax.legend()
    ax.set_title("Empirical Density")
    plt.tight_layout()
    return fig


def mixing_time_estimate(transition_matrix, eps=0.01):
    """Estimate mixing time via spectral gap."""
    P = np.array(transition_matrix, dtype=float)
    vals = sorted(np.abs(np.linalg.eigvals(P)), reverse=True)
    spectral_gap = 1 - vals[1]
    if spectral_gap <= 0:
        return float("inf")
    return int(np.ceil(np.log(1 / eps) / spectral_gap))


# --- Common SDEs ---

def brownian_motion(t_span=(0, 1), dt=1e-3, n_paths=10):
    return sde_euler_maruyama(
        drift=lambda t, x: np.zeros_like(x),
        diffusion=lambda t, x: np.ones_like(x),
        y0=[0.0], t_span=t_span, dt=dt, n_paths=n_paths
    )


def ornstein_uhlenbeck(theta=1.0, mu=0.0, sigma=0.3, x0=1.0, t_span=(0, 10),
                       dt=1e-3, n_paths=20):
    """OU process: dX = theta*(mu - X)dt + sigma*dW"""
    return sde_euler_maruyama(
        drift=lambda t, x: theta * (mu - x),
        diffusion=lambda t, x: np.full_like(x, sigma),
        y0=[x0], t_span=t_span, dt=dt, n_paths=n_paths
    )
