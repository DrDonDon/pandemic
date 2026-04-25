"""
Optimization toolkit.
Landscape visualization, gradient flows, convex optimization.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize, differential_evolution
from scipy.linalg import eigvalsh


def landscape_2d(f, xlim, ylim, resolution=200, log_scale=False, title="Loss Landscape"):
    """Plot a 2D function landscape as a contour + surface."""
    x = np.linspace(*xlim, resolution)
    y = np.linspace(*ylim, resolution)
    X, Y = np.meshgrid(x, y)
    Z = np.vectorize(lambda a, b: f([a, b]))(X, Y)
    if log_scale:
        Z = np.log1p(Z - Z.min())

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Contour
    axes[0].contourf(X, Y, Z, levels=40, cmap="viridis")
    axes[0].contour(X, Y, Z, levels=20, colors="white", alpha=0.3, linewidths=0.5)
    axes[0].set_title(f"{title} — Contour")
    axes[0].set_xlabel("x₁"); axes[0].set_ylabel("x₂")

    # 3D surface
    ax3d = fig.add_subplot(1, 2, 2, projection="3d", computed_zorder=False)
    ax3d.plot_surface(X, Y, Z, cmap="viridis", alpha=0.85, linewidth=0)
    ax3d.set_title(f"{title} — Surface")
    fig.delaxes(axes[1])
    plt.tight_layout()
    return fig


def gradient_flow(f, grad_f, x0, lr=0.01, n_steps=500, momentum=0.0):
    """
    Simulate gradient descent / gradient flow trajectory.
    Returns array of iterates shape (n_steps+1, dim).
    """
    x = np.array(x0, dtype=float)
    trajectory = [x.copy()]
    v = np.zeros_like(x)

    for _ in range(n_steps):
        g = np.array(grad_f(x))
        v = momentum * v - lr * g
        x = x + v
        trajectory.append(x.copy())

    return np.array(trajectory)


def plot_gradient_flow(f, trajectory, xlim, ylim, title="Gradient Flow"):
    """Overlay a gradient flow trajectory on the loss landscape."""
    x = np.linspace(*xlim, 200)
    y = np.linspace(*ylim, 200)
    X, Y = np.meshgrid(x, y)
    Z = np.vectorize(lambda a, b: f([a, b]))(X, Y)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.contourf(X, Y, Z, levels=40, cmap="viridis", alpha=0.7)
    ax.plot(trajectory[:, 0], trajectory[:, 1], "r.-", linewidth=1.5,
            markersize=3, label="GD path")
    ax.plot(*trajectory[0], "go", markersize=8, label="Start")
    ax.plot(*trajectory[-1], "r*", markersize=12, label="End")
    ax.set_xlim(xlim); ax.set_ylim(ylim)
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    return fig


def minimize_global(f, bounds, method="differential_evolution", **kwargs):
    """Global optimization over a box. Returns OptimizeResult."""
    if method == "differential_evolution":
        return differential_evolution(f, bounds, **kwargs)
    return minimize(f, x0=np.mean(bounds, axis=1), bounds=bounds, method="L-BFGS-B",
                    **kwargs)


def convex_solve(objective_fn, constraints=None, variables=None):
    """
    Thin wrapper hint — for convex programs use CVXPY directly:

    import cvxpy as cp
    x = cp.Variable(n)
    prob = cp.Problem(cp.Minimize(objective), constraints)
    prob.solve()
    """
    raise NotImplementedError(
        "Use CVXPY directly for convex programs.\n"
        "  import cvxpy as cp\n"
        "  x = cp.Variable(n)\n"
        "  prob = cp.Problem(cp.Minimize(0.5 * cp.sum_squares(x)), [x >= 0])\n"
        "  prob.solve()"
    )


def hessian_spectrum(f, x, eps=1e-5):
    """Numerical Hessian and its eigenvalues at point x."""
    n = len(x)
    H = np.zeros((n, n))
    fx = f(x)
    for i in range(n):
        for j in range(n):
            xpp = x.copy(); xpp[i] += eps; xpp[j] += eps
            xpm = x.copy(); xpm[i] += eps; xpm[j] -= eps
            xmp = x.copy(); xmp[i] -= eps; xmp[j] += eps
            xmm = x.copy(); xmm[i] -= eps; xmm[j] -= eps
            H[i, j] = (f(xpp) - f(xpm) - f(xmp) + f(xmm)) / (4 * eps**2)
    eigs = eigvalsh(H)
    return H, eigs


# --- Classic test functions ---

def rosenbrock(x, a=1, b=100):
    return (a - x[0])**2 + b * (x[1] - x[0]**2)**2

def rastrigin(x):
    n = len(x)
    return 10 * n + sum(xi**2 - 10 * np.cos(2 * np.pi * xi) for xi in x)

def ackley(x):
    a, b, c = 20, 0.2, 2 * np.pi
    n = len(x)
    return (-a * np.exp(-b * np.sqrt(sum(xi**2 for xi in x) / n))
            - np.exp(sum(np.cos(c * xi) for xi in x) / n) + a + np.e)
