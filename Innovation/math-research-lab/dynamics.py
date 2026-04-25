"""
Dynamical systems toolkit.
Phase portraits, trajectories, Lyapunov exponents, bifurcation diagrams.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve


def phase_portrait(f, xlim, ylim, title="Phase Portrait", density=1.5, trajectories=None):
    """
    Plot 2D vector field and optional trajectories.

    f(t, y) -> [dy1/dt, dy2/dt]
    trajectories: list of (y0, t_span) pairs
    """
    x = np.linspace(*xlim, 30)
    y = np.linspace(*ylim, 30)
    X, Y = np.meshgrid(x, y)

    U = np.zeros_like(X)
    V = np.zeros_like(Y)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            dxy = f(0, [X[i, j], Y[i, j]])
            U[i, j], V[i, j] = dxy[0], dxy[1]

    speed = np.sqrt(U**2 + V**2)
    speed[speed == 0] = 1

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.streamplot(X, Y, U, V, color=speed, cmap="plasma", density=density, linewidth=0.8)

    if trajectories:
        for y0, t_span in trajectories:
            sol = solve_ivp(f, t_span, y0, max_step=0.01, dense_output=True)
            ax.plot(sol.y[0], sol.y[1], "r-", linewidth=1.5, alpha=0.8)
            ax.plot(y0[0], y0[1], "ro", markersize=5)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_title(title)
    ax.set_xlabel("x₁")
    ax.set_ylabel("x₂")
    plt.tight_layout()
    return fig


def simulate(f, y0, t_span, t_eval=None, **kwargs):
    """Integrate an ODE. Returns scipy solution object."""
    if t_eval is None:
        t_eval = np.linspace(t_span[0], t_span[1], 2000)
    return solve_ivp(f, t_span, y0, t_eval=t_eval, max_step=1e-3, **kwargs)


def lyapunov_exponent(f, y0, t_max=500, dt=0.01, n_renorm=100):
    """
    Estimate the largest Lyapunov exponent via QR renormalization.
    Works for autonomous systems f(t, y).
    """
    n = len(y0)
    y = np.array(y0, dtype=float)
    Q = np.eye(n)
    log_sum = 0.0
    steps = int(t_max / dt)
    renorm_every = max(1, steps // n_renorm)

    def rk4_step(y, dt):
        k1 = np.array(f(0, y))
        k2 = np.array(f(0, y + 0.5 * dt * k1))
        k3 = np.array(f(0, y + 0.5 * dt * k2))
        k4 = np.array(f(0, y + dt * k3))
        return y + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

    def jacobian(y, eps=1e-6):
        J = np.zeros((n, n))
        fy = np.array(f(0, y))
        for i in range(n):
            yp = y.copy(); yp[i] += eps
            J[:, i] = (np.array(f(0, yp)) - fy) / eps
        return J

    for step in range(steps):
        J = jacobian(y)
        Q = Q + dt * (J @ Q)
        y = rk4_step(y, dt)

        if (step + 1) % renorm_every == 0:
            Q, R = np.linalg.qr(Q)
            log_sum += np.log(np.abs(np.diag(R)))

    return log_sum / t_max


def fixed_points(f, search_grid_x, search_grid_y, tol=1e-8):
    """Find fixed points of a 2D system on a search grid."""
    fps = []
    seen = []
    for x0 in search_grid_x:
        for y0 in search_grid_y:
            try:
                fp = fsolve(lambda y: f(0, y), [x0, y0], full_output=True)
                if fp[2] == 1:  # converged
                    pt = fp[0]
                    if not any(np.linalg.norm(pt - s) < tol for s in seen):
                        fps.append(pt)
                        seen.append(pt)
            except Exception:
                pass
    return fps


def bifurcation_diagram(f_param, y0, param_range, t_settle=200, t_record=50, dt=0.02):
    """
    1D bifurcation diagram.
    f_param(t, y, p) -> dy/dt  (y is scalar, p is parameter)
    """
    params = np.linspace(*param_range, 400)
    attractor_pts = []

    for p in params:
        f = lambda t, y: f_param(t, y, p)
        # settle
        sol = solve_ivp(f, [0, t_settle], y0, max_step=dt)
        y_end = sol.y[:, -1]
        # record
        sol2 = solve_ivp(f, [0, t_record], y_end, max_step=dt,
                         t_eval=np.arange(0, t_record, dt))
        for v in sol2.y[0]:
            attractor_pts.append((p, v))

    fig, ax = plt.subplots(figsize=(10, 5))
    ps, ys = zip(*attractor_pts)
    ax.plot(ps, ys, ",k", alpha=0.3, markersize=0.5)
    ax.set_xlabel("Parameter")
    ax.set_ylabel("Attractor")
    ax.set_title("Bifurcation Diagram")
    plt.tight_layout()
    return fig


def lorenz(sigma=10, rho=28, beta=8/3):
    """Classic Lorenz system factory."""
    def f(t, y):
        x, y_, z = y
        return [sigma * (y_ - x), x * (rho - z) - y_, x * y_ - beta * z]
    return f
