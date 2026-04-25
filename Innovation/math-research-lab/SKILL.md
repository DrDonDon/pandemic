---
name: math-lab
version: 1.0.0
description: |
  AI-powered mathematical research lab for dynamical systems, probability,
  optimization, and AI theory. Run numerical experiments, analyze conjectures,
  search ArXiv, visualize dynamics, and chat with an AI math collaborator.
  Use when asked to "explore a conjecture", "simulate a system", "search
  arxiv", "plot a phase portrait", "analyze stability", "run an experiment",
  or "math lab". (math-lab)
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - AskUserQuestion
triggers:
  - math lab
  - explore conjecture
  - phase portrait
  - simulate system
  - search arxiv
  - analyze stability
  - run experiment
  - plot dynamics
---

# /math-lab — AI Mathematical Research Lab

Rapid prototyping for dynamical systems, probability, optimization, and AI theory.

## Preamble (run first)

```bash
_SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || echo "$HOME/.claude/skills/math-lab")"
_LAB_DIR="${MATH_LAB_DIR:-$HOME/pandemic/Innovation/math-research-lab}"
# Fallback: search common locations
if [ ! -d "$_LAB_DIR" ]; then
  for _candidate in \
    "$HOME/pandemic/Innovation/math-research-lab" \
    "$(git rev-parse --show-toplevel 2>/dev/null)/Innovation/math-research-lab" \
    "$HOME/Innovation/math-research-lab"; do
    [ -d "$_candidate" ] && _LAB_DIR="$_candidate" && break
  done
fi
echo "LAB_DIR: $_LAB_DIR"
echo "LAB_EXISTS: $([ -d "$_LAB_DIR" ] && echo yes || echo no)"

# Check Python
_PY=$(command -v python3 2>/dev/null || echo "")
echo "PYTHON: ${_PY:-missing}"

# Check venv
_VENV="$_LAB_DIR/.venv"
echo "VENV: $([ -d "$_VENV" ] && echo ready || echo missing)"

# Check ANTHROPIC_API_KEY
echo "API_KEY: $([ -n "$ANTHROPIC_API_KEY" ] && echo set || echo missing)"

# Check gstack browse binary for ArXiv browsing
_B=""
[ -x "$HOME/.claude/skills/gstack/browse/dist/browse" ] && _B="$HOME/.claude/skills/gstack/browse/dist/browse"
[ -z "$_B" ] && _ROOT=$(git rev-parse --show-toplevel 2>/dev/null) && \
  [ -x "$_ROOT/.claude/skills/gstack/browse/dist/browse" ] && \
  _B="$_ROOT/.claude/skills/gstack/browse/dist/browse"
echo "BROWSE: ${_B:-missing}"

# Session log
mkdir -p ~/.math-lab/sessions
_SESSION_ID="$$-$(date +%s)"
_SESSION_LOG=~/.math-lab/sessions/"$_SESSION_ID".jsonl
echo '{"event":"start","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' >> "$_SESSION_LOG"
echo "SESSION: $_SESSION_ID"
echo "SESSION_LOG: $_SESSION_LOG"
```

**If `LAB_EXISTS` is `no`:** Tell the user the lab directory wasn't found. Ask them to set `MATH_LAB_DIR` to the path of their `math-research-lab` folder, or run `install.sh`.

**If `VENV` is `missing`:** Run:
```bash
cd "$_LAB_DIR" && python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt
echo "VENV_SETUP: done"
```
Tell the user "Setting up Python environment (first run, ~60 seconds)..."

**If `API_KEY` is `missing`:** Warn the user: "Set `ANTHROPIC_API_KEY` in your environment to enable the AI brain. Numerical tools still work without it."

Set `$B` from the BROWSE output for use in ArXiv browsing steps below.

---

## Step 1 — Choose Mode

```bash
echo "Ready."
```

Use AskUserQuestion:

> What do you want to explore?

Options:
- A) **Conjecture** — analyze a mathematical statement, find proof direction or counterexample
- B) **Numerical Experiment** — simulate a dynamical system, SDE, or optimization landscape
- C) **ArXiv Search** — find papers on a topic, browse abstracts and PDFs
- D) **Free Chat** — talk to the AI math collaborator about anything

---

## Mode A — Conjecture Analysis

Ask the user: "State your conjecture." (free text input)

Then ask: "Any numerical evidence or context to include?" (optional)

Run:
```bash
cd "$_LAB_DIR" && source .venv/bin/activate
python3 - <<'PYEOF'
import os, sys
sys.path.insert(0, '.')
from brain import analyze_conjecture
conjecture = os.environ.get('_CONJECTURE', '')
evidence = os.environ.get('_EVIDENCE', '')
print(analyze_conjecture(conjecture, evidence))
PYEOF
```

Set `_CONJECTURE` and `_EVIDENCE` as env vars from the user's answers before running.

After showing the AI analysis, ask:
> What next?
- A) Sketch a proof — go to Proof Sketch sub-mode
- B) Hunt for a counterexample — go to Counterexample sub-mode
- C) Search ArXiv for related work — go to Mode C
- D) Run a numerical test — go to Mode B
- E) Done

**Proof Sketch sub-mode:**
Ask "Any approach in mind?" then run:
```bash
cd "$_LAB_DIR" && source .venv/bin/activate
python3 -c "
import os, sys; sys.path.insert(0,'.')
from brain import proof_sketch
print(proof_sketch(os.environ['_STATEMENT'], os.environ.get('_APPROACH','')))
"
```

**Counterexample sub-mode:**
```bash
cd "$_LAB_DIR" && source .venv/bin/activate
python3 -c "
import os, sys; sys.path.insert(0,'.')
from brain import find_counterexample
print(find_counterexample(os.environ['_STATEMENT']))
"
```

---

## Mode B — Numerical Experiment

Use AskUserQuestion:

> Which type of experiment?

Options:
- A) **Dynamical system** — phase portrait, trajectory, Lyapunov exponent, bifurcation
- B) **Stochastic process** — SDE simulation, Markov chain, empirical distribution
- C) **Optimization landscape** — plot loss surface, run gradient flow, find minima

### B-A: Dynamical System

Ask: "Describe your system (e.g. Lorenz, van der Pol, or give the equations as f([x,y]) → [dx,dy])."

Generate and run a Python script in `~/.math-lab/sessions/` based on their description. Example scaffold:

```python
# scaffold — adapt to user's system
import sys
sys.path.insert(0, '_LAB_DIR_')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dynamics import phase_portrait, simulate, lyapunov_exponent, lorenz

# --- USER SYSTEM HERE ---
f = lorenz()  # replace with user's system

fig = phase_portrait(
    lambda t, y: [f(t,y)[0], f(t,y)[1]],
    xlim=(-20, 20), ylim=(-25, 25),
    title="Phase Portrait",
    trajectories=[([-5, 5], (0, 20))]
)
fig.savefig('/tmp/phase_portrait.png', dpi=150)
print("Saved: /tmp/phase_portrait.png")

le = lyapunov_exponent(f, [1.0, 1.0, 1.0], t_max=200)
print(f"Largest Lyapunov exponent (per dim): {le}")
```

Replace `_LAB_DIR_` with the actual `$_LAB_DIR` path.
Write the script to `$_SESSION_LOG`-companion `.py`, run it, show output.
Then read `/tmp/phase_portrait.png` with the Read tool so the user can see it.

After showing results, ask: "Want me to analyze these dynamics with the AI brain?" If yes, pass the Lyapunov output to `brain.ask()`.

### B-B: Stochastic Process

Ask: "What process? (e.g. Ornstein-Uhlenbeck, geometric Brownian motion, or describe drift/diffusion)"

Generate and run:
```python
import sys
sys.path.insert(0, '_LAB_DIR_')
import matplotlib
matplotlib.use('Agg')
from probability import ornstein_uhlenbeck, plot_sde_paths

t, paths = ornstein_uhlenbeck(theta=1.0, mu=0.0, sigma=0.3, n_paths=50)
fig = plot_sde_paths(t, paths, title="Ornstein-Uhlenbeck Paths")
fig.savefig('/tmp/sde_paths.png', dpi=150)
print("Saved: /tmp/sde_paths.png")
print(f"Mean at T: {paths[:,-1,0].mean():.4f}  Std: {paths[:,-1,0].std():.4f}")
```

Read `/tmp/sde_paths.png` to show the user.

### B-C: Optimization Landscape

Ask: "Describe the function to optimize (e.g. Rosenbrock, or give f([x,y]) → scalar)."

Generate and run:
```python
import sys
sys.path.insert(0, '_LAB_DIR_')
import matplotlib
matplotlib.use('Agg')
import numpy as np
from optimize import landscape_2d, gradient_flow, plot_gradient_flow, rosenbrock

f = rosenbrock  # replace with user's function
grad_f = lambda x: np.array([
    -2*(1-x[0]) - 400*x[0]*(x[1]-x[0]**2),
     200*(x[1]-x[0]**2)
])

fig = landscape_2d(f, xlim=(-2,2), ylim=(-1,3), title="Loss Landscape")
fig.savefig('/tmp/landscape.png', dpi=150)

traj = gradient_flow(f, grad_f, x0=[-1.5, 1.0], lr=0.002, n_steps=2000)
fig2 = plot_gradient_flow(f, traj, xlim=(-2,2), ylim=(-1,3))
fig2.savefig('/tmp/gradient_flow.png', dpi=150)
print(f"Saved: /tmp/landscape.png, /tmp/gradient_flow.png")
print(f"Final point: {traj[-1]}  f(final): {f(traj[-1]):.6f}")
```

Read both PNGs to show the user.

---

## Mode C — ArXiv Search

Ask: "What topic are you searching for?"

Run:
```bash
cd "$_LAB_DIR" && source .venv/bin/activate
python3 - <<'PYEOF'
import os, sys
sys.path.insert(0, '.')
from arxiv_search import search_for_topic, print_results
topic = os.environ['_TOPIC']
areas = ["math.DS", "math.PR", "math.OC", "cs.LG", "math.AP"]
results = search_for_topic(topic, areas)
print_results(results, show_abstract=False)
# Print URLs for browsing
for i, r in enumerate(results, 1):
    print(f"[{i}] {r['url']}")
PYEOF
```

Show the results table. Then ask:

> Want to open any paper?
- A) Yes — open in browser with gstack
- B) Search the AI brain for related theorems instead
- C) Done

**If A and `$B` is available:**
Ask "Which paper number?" then:
```bash
$B goto "<paper_url>"
$B snapshot -i
$B screenshot /tmp/arxiv_paper.png
```
Read `/tmp/arxiv_paper.png` to show the paper. Then `$B text` to extract the abstract for AI analysis.

**If A and `$B` is missing:** Print the URL and tell the user to open it manually.

**If B:** Pass the topic and top 3 paper titles to `brain.literature_hint()`.

---

## Mode D — Free Chat

```bash
cd "$_LAB_DIR" && source .venv/bin/activate
python3 -c "
import sys; sys.path.insert(0,'.')
from brain import chat
chat()
"
```

This opens a multi-turn interactive session with the AI math collaborator.

---

## Research Log

After any mode completes, ask:

> Save results to your research log?
- A) Yes — save to `~/.math-lab/log.md`
- B) No

If A, append a timestamped entry to `~/.math-lab/log.md`:
```markdown
## <date> — <mode>: <one-line summary>

<key results, figures generated, AI analysis excerpt>

---
```

---

## Completion

```bash
_TEL_END=$(date +%s)
echo '{"event":"end","ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","session":"'"$_SESSION_ID"'"}' >> "$_SESSION_LOG"
```

Report **DONE** with a one-line summary of what was computed/explored.

Suggest next steps:
- Run another experiment: `/math-lab`
- Search literature: `/math-lab` → Mode C
- Ship findings to a notebook: open JupyterLab with `cd <lab-dir> && .venv/bin/jupyter lab`
