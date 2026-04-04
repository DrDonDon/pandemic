"""
agentspec render CLI

Renders an agentspec YAML to a platform-native output file.

Usage:
    python deployers/render.py --platform langchain examples/billing-dispute.yaml
    python deployers/render.py --platform crewai examples/billing-dispute.yaml
    python deployers/render.py --platform langchain examples/billing-dispute.yaml --output out/agent.py

Supported platforms:
    langchain   — generates a Python file with LangChain AgentExecutor
    crewai      — generates a Python file with CrewAI Crew

File-output only. No API calls are made. The generated file is the artifact.
"""

import sys
import argparse
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)

# Import deployers relative to this file
sys.path.insert(0, str(Path(__file__).parent))
from langchain_deployer import render as render_langchain
from crewai_deployer import render as render_crewai

PLATFORMS = {
    "langchain": render_langchain,
    "crewai": render_crewai,
}


def main():
    parser = argparse.ArgumentParser(
        description="Render an agentspec YAML to a platform-native output.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("spec", help="Path to agentspec YAML file")
    parser.add_argument(
        "--platform", "-p",
        required=True,
        choices=list(PLATFORMS.keys()),
        help="Target platform",
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path. Default: <spec-name>_<platform>.py",
    )
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"ERROR: {args.spec} not found")
        sys.exit(1)

    with open(spec_path) as f:
        spec = yaml.safe_load(f)

    render_fn = PLATFORMS[args.platform]
    code = render_fn(spec)

    if args.output:
        out_path = Path(args.output)
    else:
        stem = spec_path.stem.replace("-", "_")
        out_path = spec_path.parent.parent / "out" / f"{stem}_{args.platform}.py"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(code)
    print(f"✓ {args.platform}: {out_path}")


if __name__ == "__main__":
    main()
