# /retro

Weekly retrospective. Tracks what's open, what was proved, what died, and what to focus on next.
Run every Friday (or at the end of a focused sprint).

---

## Preamble

```bash
echo "=== Retro ==="
if [ -f research-state.yaml ]; then
  cat research-state.yaml
fi
if [ -f dead-ends.md ]; then
  cat dead-ends.md
fi
if [ -f direction-log.md ]; then
  tail -50 direction-log.md
fi
echo "--- Recent simulation files ---"
ls -lt simulations/ 2>/dev/null | head -10 || echo "(none)"
echo "--- Recent proof files ---"
ls -lt proofs/ 2>/dev/null | head -10 || echo "(none)"
```

---

## Retro Structure

### 1. What happened this week

List concretely:
- Conjectures formalised (new entries in open_conjectures)
- Conjectures disproved (moved to disproved + dead-ends)
- Conjectures proved (moved to proved + proof file written)
- Simulations run
- Proof attempts started or completed
- Literature found

Do not editorialize. Just list.

### 2. What's the current state of each open conjecture

For each entry in `open_conjectures`:
- How many weeks has it been active?
- What's the latest evidence for/against?
- What is blocking progress?
- Is it still worth pursuing, or should it be handed to `/research-director`?

Flag any conjecture with `weeks_active >= 2` and no new evidence this week. That's a stall.

### 3. What are the three most promising open directions right now

Not the three most active — the three most likely to yield a result in the next 2 weeks.
State why for each. This is a judgment call, not just a list.

### 4. What should be abandoned

Name any conjecture or approach that should be moved to dead-ends. State the reason:
- Disproved (counterexample exists)
- Not worth the effort given current evidence
- Superseded by a better-stated version
- Blocked by an obstacle that isn't going to resolve

Abandoning is not failure. It is information.

### 5. One thing to do differently

One specific change to the research process. Not "work harder" — a specific change.
Examples: "run `/counterexample` before any new proof attempt", "commit research-state.yaml daily", "run `/research-director` after 10 days without a result".

---

## Output

Update `research-state.yaml`:
- Set `last_retro` to today's date
- Update `weeks_active` on all open conjectures
- Move any abandoned conjectures to `disproved` or add to `dead_ends`
- Update `current_focus` if it changed

Append a retro entry to `retro-log.md`:

```markdown
## Retro — [DATE]

### What happened
- [list]

### Open conjecture status
| ID | Weeks active | Status | Blocker |
|----|-------------|--------|---------|
| C1 | 2 | active | step 3 unjustified |
| C2 | 0 | new | — |

### Top 3 directions
1. [conjecture + reason]
2. ...
3. ...

### Abandoned this week
- [list with reasons]

### One change
[specific process change]
```

---

## Voice

Honest about stalls. "C1 has been active for 3 weeks with no new evidence" is a problem that should be named, not softened. The retro is the mechanism for catching rabbit holes before they become months.

---

## Completion

- **DONE** — retro-log.md updated, research-state.yaml updated
- **DONE_WITH_CONCERNS** — one or more conjectures have been active >2 weeks with no progress; recommend running /research-director before next sprint
