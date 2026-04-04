# mathstack skill routing rules
# Add this section to your project's CLAUDE.md

## Skill routing (mathstack)

When the user's request matches one of these, ALWAYS invoke the skill using the Skill
tool as your FIRST action. Do not answer directly. Do not use other tools first.

Key routing rules:
- Direction, priorities, "what should we work on", stuck for weeks → invoke research-director
- Literature, related work, prior results, papers → invoke literature-scout
- Formalise a conjecture, write it precisely, sharpen an idea → invoke conjecture
- Try to disprove, find a counterexample, test cheaply → invoke counterexample
- Derive, prove, step through the proof → invoke derive
- Simulate, numerical experiment, parameter sweep, plot → invoke simulate
- Review the proof, check correctness, find gaps → invoke proof-review
- Edit the paper, review writing, structure, notation → invoke editor
- Write a blog post, talk abstract, accessible version → invoke science-writer
- Write the paper, assemble LaTeX → invoke write
- Weekly retro, what did we do, what's open → invoke retro
- Save progress, checkpoint, resume later → invoke checkpoint
