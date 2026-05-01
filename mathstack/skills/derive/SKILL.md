# /derive

Step-by-step derivation. Each step is explicit. Each assumption is named when first used.
Outputs LaTeX.

Run after `/counterexample` has found no violation.

---

## Preamble

```bash
echo "=== Derive ==="
if [ -f research-state.yaml ]; then
  cat research-state.yaml
fi
CONJECTURE_ID="${1:-}"
if [ -n "$CONJECTURE_ID" ] && [ -f "conjectures/${CONJECTURE_ID}.md" ]; then
  cat "conjectures/${CONJECTURE_ID}.md"
fi
```

---

## Inputs

A conjecture ID or statement. Optionally: a suggested proof strategy from the researcher.

---

## Workflow

**1. Choose a strategy.**
Before writing a single step, state the proof strategy:
- Direct proof
- Contradiction
- Induction (on what? with what base case?)
- Construction
- Reduction to a known result (name the result)

If the conjecture has a stepping-stone hierarchy (from `/conjecture`), start with the weaker version.

**2. Write the proof structure.**
Outline the proof before filling in details:
```
1. Establish [preliminary lemma]
2. Apply [known result] to get [intermediate claim]
3. Take [limit / bound / estimate] to get the conclusion
```

If any step looks hard, flag it immediately. Don't defer hard steps to "details to fill in later" — that's where proofs break.

**3. Derive step by step.**
For each step:
- Write the mathematical claim
- Write the justification (which lemma, which inequality, which assumption)
- State explicitly which assumption from the conjecture statement is being used
- Flag if the step requires a new lemma (add it to a "Lemmas Needed" list)

Format each step as LaTeX, inside an `align` or `proof` environment.

**4. Handle the hard steps.**
For any step flagged as hard:
- Try a direct calculation first
- If that fails, try bounding/estimating
- If that fails, try a different strategy for that step specifically
- If stuck for more than 30 minutes of reasoning, flag it and suggest running `/simulate` to check whether the step is even true before going further

**5. Verify the proof closes.**
At the end, confirm:
- Every assumption in the conjecture statement was used
- No assumption was used that isn't in the statement (if one was, the statement needs updating)
- The conclusion follows from the last step
- All lemmas listed as "Needed" are either proved inline or cited

---

## Output

Write the derivation to `proofs/[CONJECTURE_ID]-draft.tex`:

```latex
\begin{theorem}[Conjecture CN]
  [Formal statement]
\end{theorem}

\begin{proof}
  [Step-by-step proof in LaTeX]
\end{proof}
```

If lemmas were needed, write them before the main theorem with their own proofs.

Update the conjecture entry in research-state.yaml:
- If proof is complete: move to `proved`, set `proof_file`
- If proof has gaps: leave in `open_conjectures`, add gaps to `evidence_against` with step numbers
- If a new assumption was required: update the conjecture statement and flag for researcher review

---

## Voice

Show your work. A derivation with gaps filled by "it can be shown that" is not a derivation — it's a sketch. Write every step. If a step is standard and tedious (e.g. swapping a limit and an integral), cite the theorem that justifies it rather than just doing it without comment.

When stuck, say so precisely: "Step 3 requires bounding [expression] — standard approaches give [weaker bound] which is insufficient. Possible approaches: [list]."

---

## Completion

- **DONE** — complete proof written to proofs/CN-draft.tex, research-state.yaml updated
- **DONE_WITH_CONCERNS** — proof is complete but uses an assumption not in the original statement; updated conjecture statement needs researcher review
- **BLOCKED** — specific step identified where every attempted approach fails; describe the obstruction precisely and recommend /simulate or /research-director
