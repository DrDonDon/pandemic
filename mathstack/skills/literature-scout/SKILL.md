# /literature-scout

Finds related work. Summarises what's known, what was tried, and where the gaps are.
Outputs to `research-state.yaml` under `adjacent_results`.

---

## Preamble

```bash
echo "=== Literature Scout ==="
if [ -f research-state.yaml ]; then
  cat research-state.yaml
  echo "STATE: loaded"
else
  echo "STATE: missing — run /checkpoint first or create research-state.yaml"
fi
```

---

## Inputs

Read:
- `research-state.yaml` — especially `question`, `motivation`, and any existing `adjacent_results`
- Any conjecture IDs passed as arguments

The user may also provide keywords or paper titles as a starting point.

---

## Workflow

**1. Construct search terms.**
From the `question` field, extract 3–5 search queries. Vary them — use both technical terminology and applied-domain language. The same result appears under different names in different communities.

**2. Search.**
Use WebSearch to run each query against:
- arXiv (search.arxiv.org) — preprints, most current
- Google Scholar — breadth, including textbooks and older results
- Semantic Scholar — citation graph, finds highly-cited foundational papers

For each promising result, fetch the abstract. For the 3–5 most relevant, skim the introduction and theorem statements.

**3. Summarise each relevant paper.**
For each paper worth noting:
- What did they prove? (One precise sentence — use their notation if possible)
- What assumptions did they need?
- What did they leave open?
- How does it relate to the current question? (extends / contradicts / analogous / prerequisite)

**4. Identify gaps.**
Across all papers found: what is the natural next step that no one has taken? Where do the results stop? Are there obvious generalisations that appear unaddressed?

**5. Flag conflicts.**
If any adjacent result directly implies the current conjecture (already proved) or directly contradicts it (already disproved), flag this immediately and prominently before anything else.

---

## Output

Update `adjacent_results` in `research-state.yaml` with structured entries:

```yaml
adjacent_results:
  - citation: "Author et al. (Year), Journal/arXiv:XXXX.XXXXX"
    what_they_proved: "Precise one-sentence summary"
    assumptions: "Key conditions required"
    how_it_relates: "extends / contradicts / analogous / prerequisite"
    gap: "What they didn't do"
```

Also write a prose summary to `literature-notes.md`:
- What the field currently knows about this problem
- The 2–3 most important prior results and why they matter
- The clearest identified gap (this should match or inform `current_focus` in research-state.yaml)

---

## Voice

Precise about what is proved vs. conjectured in the literature. Don't say "they showed that X tends to hold" — say "they proved X under conditions Y and Z" or "they conjectured X but gave no proof". This distinction matters.

---

## Completion

- **DONE** — adjacent_results updated, literature-notes.md written, gaps identified
- **DONE_WITH_CONCERNS** — a prior result may already answer the question; flag explicitly for researcher review
- **NEEDS_CONTEXT** — question field too vague to construct useful search terms
