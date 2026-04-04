# mathstack

A skill framework for applied math research. Inspired by [gstack](https://gstack.dev).

The unit of work is a **conjecture**, not a feature. "Disproved" is a valid outcome.

---

## Sprint Structure

Research runs in two modes that switch based on progress:

### Mode 1: Divergent (no fixed length)
```
Scout → Conjecture → Counterexample → Checkpoint
   ↑__________________________________|
```
Loop until 2–3 promising directions crystallise. Exit when Research Director approves a direction.

### Mode 2: Focused (1–2 week sprints)
```
Derive → Simulate → Proof-Review → Write ──┬──→ Editor ──────────→ Revise → Submit
                                            └──→ Science-Writer → Blog / Talk
```

---

## Skills

| Skill | Role | When to use |
|---|---|---|
| `/research-director` | PI — sets direction, rescues stuck threads | Start of project; when stuck >2 weeks |
| `/literature-scout` | Finds related work, surfaces gaps | Before committing to a direction |
| `/conjecture` | Formalises rough ideas into precise statements | When intuition needs sharpening |
| `/counterexample` | Adversarially tries to disprove a conjecture | Before investing in a proof |
| `/derive` | Step-by-step derivation with LaTeX output | Working phase |
| `/simulate` | Numerical experiments, parameter sweeps | Working phase, alongside derive |
| `/proof-review` | Correctness check — finds gaps, challenges steps | After a proof draft exists |
| `/editor` | Communication review — structure, clarity, notation | After a paper draft exists |
| `/science-writer` | Accessible version — blog, abstract, talk | After results are clear |
| `/write` | Assembles LaTeX paper | Writing phase |
| `/retro` | Weekly: what's open, proved, dead | Every Friday |
| `/checkpoint` | Saves research state for resuming | Before any break |

---

## State Files

All skills read and write from two shared files:

**`research-state.yaml`** — living document tracking the research
**`dead-ends.md`** — log of disproved conjectures and failed approaches (valuable)

Initialise them by copying the templates:
```bash
cp mathstack/templates/research-state.yaml ./research-state.yaml
cp mathstack/templates/dead-ends.md ./dead-ends.md
```

---

## Install

Copy skills to `~/.claude/skills/` so they're available in any Claude Code session:

```bash
bash mathstack/install.sh
```

Then add the routing rules from `mathstack/CLAUDE-routing.md` to your project's `CLAUDE.md`.

---

## Key differences from gstack

1. **Track dead ends.** `dead-ends.md` is a first-class artifact — not a bin.
2. **Counterexample before derive.** Falsify cheaply before investing in a proof.
3. **Research Director runs twice** — at the start and in rescue mode (no gstack equivalent).
4. **Science writer and editor are peers** — they run in parallel, not in sequence.
5. **Retro tracks open questions**, not velocity.
