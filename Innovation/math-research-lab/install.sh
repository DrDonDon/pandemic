#!/usr/bin/env bash
# Install the math-lab skill to ~/.claude/skills/math-lab/
set -euo pipefail

SKILL_NAME="math-lab"
LAB_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_DIR="$HOME/.claude/skills/$SKILL_NAME"

echo "Installing $SKILL_NAME skill..."
echo "  Lab dir : $LAB_DIR"
echo "  Skill   : $INSTALL_DIR"

# Create skill directory and symlink SKILL.md
mkdir -p "$INSTALL_DIR"
ln -sf "$LAB_DIR/SKILL.md" "$INSTALL_DIR/SKILL.md"
echo "  Linked  : $INSTALL_DIR/SKILL.md -> $LAB_DIR/SKILL.md"

# Set MATH_LAB_DIR so the skill can find the Python modules
PROFILE_LINE="export MATH_LAB_DIR=\"$LAB_DIR\""
for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
  if [ -f "$rc" ] && ! grep -q "MATH_LAB_DIR" "$rc" 2>/dev/null; then
    echo "$PROFILE_LINE" >> "$rc"
    echo "  Added MATH_LAB_DIR to $rc"
  fi
done
export MATH_LAB_DIR="$LAB_DIR"

# Set up Python venv
if [ ! -d "$LAB_DIR/.venv" ]; then
  echo "  Setting up Python environment..."
  python3 -m venv "$LAB_DIR/.venv"
  "$LAB_DIR/.venv/bin/pip" install -q --upgrade pip
  "$LAB_DIR/.venv/bin/pip" install -q -r "$LAB_DIR/requirements.txt"
  echo "  Python env ready."
else
  echo "  Python env already exists — skipping."
fi

echo ""
echo "Done! The /math-lab skill is now available in Claude Code."
echo ""
echo "Usage: type /math-lab in Claude Code to start a research session."
echo ""
echo "To enable the AI brain:"
echo "  export ANTHROPIC_API_KEY=sk-ant-..."
echo ""
echo "Optional — set your API key permanently:"
echo "  echo 'export ANTHROPIC_API_KEY=sk-ant-...' >> ~/.bashrc"
