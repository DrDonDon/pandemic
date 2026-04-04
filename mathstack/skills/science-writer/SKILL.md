# /science-writer

Writes an accessible version of the result. Also forces the core insight to be stated clearly.
If the core insight can't be stated in one sentence, that's a signal — the result may not be ready to write about, or the research director needs to run again.

---

## Preamble

```bash
echo "=== Science Writer ==="
PAPER="${1:-paper/main.tex}"
FORMAT="${2:-blog}"     # blog | abstract | thread | lay-summary
if [ -f "$PAPER" ]; then
  cat "$PAPER"
fi
if [ -f research-state.yaml ]; then
  cat research-state.yaml
fi
if [ -f dead-ends.md ]; then
  echo "--- Dead Ends (often the best story) ---"
  cat dead-ends.md
fi
```

---

## Core Insight First

Before writing anything, extract the core insight:

**One sentence.** Complete it:
> "We proved that [X], which means [consequence in plain terms], because [the key idea]."

If this sentence requires more than one clause of mathematics, the result either:
- Has multiple results that should be separated, or
- Is not yet understood well enough to be written about

Do not proceed until this sentence is clear. Show it to the researcher before writing the full piece.

---

## Formats

### Blog post (1000–1500 words)
Structure:
1. **Hook** — a concrete situation where this matters. Not "in mathematics, we often study...". A real scenario.
2. **The question** — state the problem in plain terms. Use an analogy if necessary. Name what was unknown.
3. **The obstacle** — what made this hard? What did people try before? (The dead-ends log is useful here)
4. **The insight** — the one idea that unlocked the proof. Not the proof itself.
5. **The result** — what was proved, and what it implies
6. **What's next** — one open problem, stated plainly

Use one analogy. Use it consistently. Don't mix analogies.

### Talk abstract (250 words)
Structure:
1. Context sentence (what field, what type of problem)
2. The specific question (one sentence, technical but accessible)
3. Main result (what was proved)
4. Key technique (one sentence on the approach)
5. Significance (what this opens up)

### Twitter/social thread (12–15 tweets)
- Tweet 1: the hook or surprising result
- Tweets 2–4: the setup and question
- Tweets 5–8: the key idea (no equations — use analogies)
- Tweet 9–10: the result
- Tweet 11–12: what it means and what's next
- Final tweet: link to paper

### Lay summary (for grant applications, 150–200 words)
- Sentence 1: why this area matters (real-world connection)
- Sentence 2–3: the specific question
- Sentence 4–5: what was found
- Sentence 6: what it enables

---

## Accuracy constraint

Never sacrifice accuracy for accessibility. Where there is tension:
1. Use a correct analogy instead of a wrong simplification
2. Say "roughly speaking" or "informally" before a simplification
3. Flag the passage for the researcher: "This simplification loses [X] — is that acceptable for this audience?"

Technical terms can be kept if briefly explained on first use. They don't need to be eliminated.

---

## Dead ends as story

The best science writing often centres on what failed. The dead-ends log contains this material.
"We first tried X, which seemed natural — but here is why it fails" is more compelling than
a linear account of the successful proof. Ask the researcher whether any dead end is interesting
enough to feature.

---

## Output

Write to `writing/[format]-[date].md`.

Also extract the core insight sentence and add it to `research-state.yaml` under a new field:
```yaml
core_insight: "We proved that [X], which means [Y], because [Z]."
```

If the core insight sentence could not be produced, write:
```yaml
core_insight: "UNCLEAR — run /research-director"
```

---

## Voice

Plain. Concrete. Active verbs. Short sentences. No passive constructions ("it was shown that").
No jargon without explanation. No hedging that obscures the result ("results suggest that
under certain conditions...").

The reader should finish knowing one thing they didn't know before.

---

## Completion

- **DONE** — core insight stated, accessible piece written, research-state.yaml updated
- **NEEDS_CONTEXT** — core insight cannot be extracted from the paper as written; state what's missing and recommend /research-director
- **DONE_WITH_CONCERNS** — piece written but one passage required a simplification that loses important precision; flagged for researcher review
