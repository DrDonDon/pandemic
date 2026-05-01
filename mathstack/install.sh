#!/usr/bin/env bash
# Install mathstack skills to ~/.claude/skills/
# After running: invoke skills with /research-director, /conjecture, etc.

set -e

SKILLS_DIR="$HOME/.claude/skills"
MATHSTACK_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/skills"

echo "Installing mathstack skills to $SKILLS_DIR..."
mkdir -p "$SKILLS_DIR"

for skill_dir in "$MATHSTACK_SRC"/*/; do
    skill_name=$(basename "$skill_dir")
    target="$SKILLS_DIR/$skill_name"
    mkdir -p "$target"
    cp "$skill_dir/SKILL.md" "$target/SKILL.md"
    echo "  ✓ $skill_name"
done

echo ""
echo "Done. Skills installed:"
ls "$MATHSTACK_SRC"
echo ""
echo "Next: add the routing rules from mathstack/CLAUDE-routing.md to your CLAUDE.md"
