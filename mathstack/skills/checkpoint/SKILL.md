# /checkpoint

Saves the current state of the research so it can be resumed cleanly after a break.
Also useful before switching to a different conjecture.

---

## Preamble

```bash
echo "=== Checkpoint ==="
if [ -f research-state.yaml ]; then
  cat research-state.yaml
fi
echo "--- Uncommitted files ---"
git status --short 2>/dev/null || echo "(not a git repo)"
```

---

## Workflow

**1. Capture what's in progress.**
Look at:
- Any proof attempt that hasn't been committed to a file yet
- Any simulation output not saved to `simulations/`
- Any informal notes not reflected in research-state.yaml

Ask the researcher: "Is there anything in your working notes that isn't captured in a file yet?" If yes, help them write it down before continuing.

**2. Update research-state.yaml.**
- `current_focus` — what is actively being worked on
- `weeks_on_current_thread` — current count
- For the active conjecture: update `evidence_for`, `evidence_against`, `next_step`
- `last_retro` — if no retro has been run recently, flag it

**3. Write a resumption note.**
The most important output. Write `checkpoint-[DATE].md`:

```markdown
## Checkpoint — [DATE]

### Where we are
[2–3 sentences: which conjecture, what stage, what the last action was]

### What was tried most recently
[The last proof attempt / simulation / approach — enough detail to restart without re-reading everything]

### The specific next step
[One precise action: "Run /simulate on C2 with parameter range n=500..2000"
or "In proofs/C1-draft.tex, step 4 needs a dominated convergence justification — try bounding by [X]"]

### Blockers
[Anything that must be resolved before progress is possible]

### Don't forget
[Anything that's easy to lose track of: a useful paper, a sign convention, a special case that breaks an approach]
```

**4. Commit everything.**

```bash
git add research-state.yaml dead-ends.md retro-log.md direction-log.md \
        conjectures/ proofs/ simulations/ paper/ writing/ \
        checkpoint-*.md 2>/dev/null
git commit -m "checkpoint: [DATE] — [one-line status]"
```

---

## Output

- `checkpoint-[DATE].md` written
- `research-state.yaml` updated
- All loose files committed

---

## Voice

The checkpoint note is written for yourself in two weeks, not for the public. Be specific about the exact file, the exact step, the exact blocker. "Continue the proof" is not a next step. "In proofs/C1-draft.tex, step 4 needs a dominated convergence justification" is.

---

## Completion

- **DONE** — checkpoint written, state updated, files committed
- **DONE_WITH_CONCERNS** — uncommitted work found that couldn't be captured in files (e.g. work on paper); flag what needs to be written up before resuming
