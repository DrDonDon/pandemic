#!/usr/bin/env bash
# Usage: ./new-project.sh <project-name>
set -euo pipefail

NAME="${1:-}"
if [[ -z "$NAME" ]]; then
  echo "Usage: $0 <project-name>" >&2
  exit 1
fi

DIR="$(dirname "$0")/$NAME"
if [[ -d "$DIR" ]]; then
  echo "Error: $DIR already exists" >&2
  exit 1
fi

mkdir -p "$DIR"

cat > "$DIR/requirements.txt" <<'EOF'
-r ../base-requirements.txt
# Add project-specific packages below
EOF

cat > "$DIR/main.py" <<'EOF'
from rich.console import Console

console = Console()

def main():
    console.print("[bold green]Hello from your new prototype![/bold green]")

if __name__ == "__main__":
    main()
EOF

cat > "$DIR/test_browser.py" <<'EOF'
import os
from playwright.sync_api import sync_playwright

HEADED = os.getenv("HEADED", "0") == "1"

def run(url: str = "https://example.com"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not HEADED)
        page = browser.new_page()
        page.goto(url)
        title = page.title()
        print(f"Page title: {title}")
        page.screenshot(path="screenshot.png")
        print("Screenshot saved to screenshot.png")
        browser.close()

if __name__ == "__main__":
    run()
EOF

echo "Created $DIR"
echo ""
echo "Next steps:"
echo "  cd $NAME"
echo "  python -m venv .venv && source .venv/bin/activate"
echo "  pip install -r requirements.txt"
echo "  playwright install chromium"
echo "  python main.py"
