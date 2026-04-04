# /write

Assembles the LaTeX paper from proofs, derivations, and research state.
Does not invent content — assembles what exists and flags what's missing.

---

## Preamble

```bash
echo "=== Write ==="
mkdir -p paper
if [ -f research-state.yaml ]; then
  cat research-state.yaml
fi
echo "--- Existing proof files ---"
ls proofs/ 2>/dev/null || echo "(none)"
echo "--- Existing literature notes ---"
ls literature-notes.md 2>/dev/null && cat literature-notes.md || echo "(none)"
```

---

## Inputs

All proved conjectures in `research-state.yaml`, their corresponding proof files in `proofs/`,
and the `adjacent_results` from literature scout.

---

## Paper Structure

```
1. Abstract
2. Introduction
   2.1 Problem statement
   2.2 Main results (theorem statements only — no proofs)
   2.3 Proof ideas (one paragraph per main result — the key insight, not the full proof)
   2.4 Organisation of the paper
3. Related work
4. Preliminaries (notation, background results)
5. Main results (one section per proved conjecture, with full proofs)
6. Discussion
   6.1 Consequences and extensions
   6.2 Open problems
7. References
```

---

## Workflow

**1. Check what exists.**
List all proved conjectures and their proof files. List any gaps (conjectures referenced as proved but with no proof file). Do not proceed if a proof file is missing — flag it.

**2. Write the introduction last.**
Start with the body. The introduction should describe what's actually in the paper, and that can only be written once the paper exists.

**3. Write preliminaries.**
Collect all notation used in the proofs. Define every object. If a background theorem is cited in a proof, state it here (not inline in the proof). Keep this section minimal — only what's actually needed.

**4. Assemble main results sections.**
For each proved conjecture:
- State the theorem (formal statement from `conjectures/CN.md`)
- Copy and clean the proof from `proofs/CN-draft.tex`
- Precede with any needed lemmas
- Follow with a remark if the theorem is tight or has a natural extension

**5. Write related work.**
From `literature-notes.md` and `adjacent_results` in research-state.yaml.
Be precise: "Theorem 2.1 of [X] proves Y under assumption Z. Our result removes assumption Z at the cost of [...]."

**6. Write the abstract and introduction.**
Abstract: statement of main results, key technique, significance. No undefined notation.
Introduction: motivation → problem → main results (stated informally) → proof ideas → organisation.

**7. Write open problems.**
Take any conjectures still in `open_conjectures` in research-state.yaml. State them precisely. These are the paper's contribution to future work.

---

## LaTeX Template

```latex
\documentclass{amsart}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{hyperref}

\newtheorem{theorem}{Theorem}[section]
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{remark}[theorem]{Remark}
\newtheorem{conjecture}[theorem]{Conjecture}

\title{[TITLE]}
\author{[AUTHOR]}
\date{\today}

\begin{document}
\maketitle

\begin{abstract}
[ABSTRACT]
\end{abstract}

\tableofcontents

\section{Introduction}
...

\section{Preliminaries}
...

\section{Main Results}
...

\section{Discussion}
...

\bibliographystyle{amsalpha}
\bibliography{refs}

\end{document}
```

---

## Output

Write to `paper/main.tex`. Write bibliography to `paper/refs.bib`.

Flag in the output:
- Any section that needs content not yet available (e.g. a proof that hasn't been written)
- Any theorem statement that doesn't match the proof (version drift)
- Any citation that needs a BibTeX entry

---

## Completion

- **DONE** — paper/main.tex written, all proved results included, bibliography seeded
- **DONE_WITH_CONCERNS** — one or more proof files missing; paper written with [PROOF NEEDED] placeholders; list them
- **NEEDS_CONTEXT** — no proved conjectures found; nothing to assemble
