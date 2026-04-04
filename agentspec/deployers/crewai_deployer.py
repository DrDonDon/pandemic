"""
agentspec → CrewAI deployer

Reads an agentspec YAML and generates a self-contained Python file with:
  - @tool decorated functions for every integration operation
  - One CrewAI Agent per logical role (derived from flow groupings)
  - One Task per flow
  - A Crew wiring it all together

Role assignment logic:
  - entry flow → "Customer Intake Specialist"
  - flows with escalate steps → "Escalation Specialist"
  - flows with call-integration steps → "Resolution Specialist"
  - remaining flows → "Support Specialist"

Output is a Python file — no API calls made during rendering.

Usage:
    python deployers/crewai_deployer.py examples/billing-dispute.yaml
    python deployers/crewai_deployer.py examples/billing-dispute.yaml --output out/billing_dispute_crew.py
"""

import sys
import re
import argparse
from pathlib import Path
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)


# ── Helpers ───────────────────────────────────────────────────────────────────

def snake(s: str) -> str:
    return re.sub(r"[-\s]+", "_", s).lower()


def title(s: str) -> str:
    return " ".join(w.title() for w in re.split(r"[-_\s]+", s))


def entity_to_pydantic_type(entity: dict) -> str:
    if entity.get("type") == "enum":
        values = []
        for v in entity.get("values", []):
            values.append(v if isinstance(v, str) else v["value"])
        if values:
            return "Literal[" + ", ".join(f'"{v}"' for v in values) + "]"
    return {
        "string": "str", "number": "float", "boolean": "bool",
        "date": "str", "phone": "str", "email": "str", "account-number": "str",
    }.get(entity.get("type", "string"), "str")


def classify_flow(flow_id: str, flow: dict) -> str:
    """Assign a role category to a flow based on its steps."""
    if flow.get("entry"):
        return "intake"
    step_types = {s.get("type") for s in flow.get("steps", [])}
    if "escalate" in step_types and "call-integration" not in step_types:
        return "escalation"
    if "call-integration" in step_types:
        return "resolution"
    return "support"


ROLE_PROFILES = {
    "intake": {
        "role": "Customer Intake Specialist",
        "goal": "Verify customer identity and understand the nature of their request before passing to specialist agents.",
        "backstory": (
            "You are the first point of contact for every customer interaction. "
            "You are thorough, calm, and efficient. You never proceed without verifying identity. "
            "You gather all required information before handing off to the next agent."
        ),
    },
    "resolution": {
        "role": "Resolution Specialist",
        "goal": "Process customer requests by calling the appropriate backend systems and delivering outcomes.",
        "backstory": (
            "You handle the core transaction logic. You call APIs, interpret results, "
            "and determine whether a request can be resolved automatically or needs escalation. "
            "You are precise about thresholds and business rules."
        ),
    },
    "escalation": {
        "role": "Escalation Coordinator",
        "goal": "Route complex or sensitive cases to the right human queue with complete context.",
        "backstory": (
            "You handle cases that cannot be resolved automatically. "
            "You ensure specialists have every piece of information they need "
            "before the handoff — no customer should have to repeat themselves."
        ),
    },
    "support": {
        "role": "Support Specialist",
        "goal": "Handle supplementary customer requests that don't require account changes or escalation.",
        "backstory": (
            "You answer customer questions and provide account information. "
            "You are efficient and accurate, and you know when to involve other agents."
        ),
    },
}


def flow_to_task_description(flow_id: str, flow: dict, entities: dict) -> str:
    """Build a Task description from a flow's steps."""
    desc = flow.get("description", "").strip().split("\n")[0]
    collects = flow.get("collects", [])
    lines = [desc] if desc else []

    if collects:
        entity_descs = [
            entities.get(e, {}).get("description", e) for e in collects
        ]
        lines.append(f"Collect from the customer: {', '.join(entity_descs)}.")

    for step in flow.get("steps", []):
        stype = step.get("type")
        if stype == "branch":
            lines.append(f"Evaluate: {step.get('condition', 'condition')}.")
        elif stype == "call-integration":
            lines.append(
                f"Call {step.get('integration')}.{step.get('operation')} "
                f"with collected data."
            )
        elif stype == "escalate":
            lines.append(
                f"Escalate to the '{step.get('queue', 'support')}' queue "
                f"(priority: {step.get('priority', 'normal')}) with all collected entities."
            )

    return " ".join(lines) if lines else f"Handle the {title(flow_id)} flow."


def flow_to_expected_output(flow_id: str, flow: dict) -> str:
    step_types = {s.get("type") for s in flow.get("steps", [])}
    if "escalate" in step_types:
        return "Confirmation that the case has been escalated with full context provided to the specialist queue."
    if "call-integration" in step_types:
        return "Outcome of the backend operation (success confirmation or error details) communicated to the customer."
    if flow.get("collects"):
        return f"All required information collected and verified: {', '.join(flow.get('collects', []))}."
    return f"Successful completion of the {title(flow_id)} flow with outcome communicated to customer."


# ── Code generation ───────────────────────────────────────────────────────────

def render(spec: dict) -> str:
    meta = spec.get("metadata", {})
    overrides = spec.get("overrides", {}).get("crewai", {})
    integrations = spec.get("integrations", {})
    entities = spec.get("entities", {})
    flows = spec.get("flows", {})

    provider = overrides.get("provider", "anthropic")
    model = overrides.get("model", "claude-3-5-sonnet-20241022")
    process_type = overrides.get("process", "sequential")
    verbose = overrides.get("verbose", False)
    memory = overrides.get("memory", False)

    llm_import, llm_class = {
        "anthropic": ("from langchain_anthropic import ChatAnthropic", "ChatAnthropic"),
        "openai":    ("from langchain_openai import ChatOpenAI", "ChatOpenAI"),
        "google":    ("from langchain_google_genai import ChatGoogleGenerativeAI", "ChatGoogleGenerativeAI"),
        "bedrock":   ("from langchain_aws import ChatBedrock", "ChatBedrock"),
    }.get(provider, ("from langchain_anthropic import ChatAnthropic", "ChatAnthropic"))

    # ── Tools (one per integration operation) ─────────────────────────────────
    tool_blocks: list[str] = []
    all_tool_names: list[str] = []

    for int_id, integration in integrations.items():
        base_url_env = integration.get("base_url_env", f"{snake(int_id).upper()}_BASE_URL")
        auth = integration.get("auth", "none")

        for op_id, op in integration.get("operations", {}).items():
            fn_name = snake(f"{int_id}_{op_id}")
            all_tool_names.append(fn_name)

            params = ", ".join(
                f"{snake(eid)}: {entity_to_pydantic_type(entities.get(eid, {'type': 'string'}))}"
                for eid in op.get("input", [])
            )
            body_dict = "{" + ", ".join(f'"{eid}": {snake(eid)}' for eid in op.get("input", [])) + "}"

            if auth in ("api-key",):
                auth_lines = (
                    f'    api_key = os.environ.get("{snake(int_id).upper()}_API_KEY")\n'
                    f'    headers = {{"Authorization": f"Bearer {{api_key}}"}}\n'
                )
            elif auth == "oauth2":
                auth_lines = (
                    f'    token = os.environ.get("{snake(int_id).upper()}_ACCESS_TOKEN")\n'
                    f'    headers = {{"Authorization": f"Bearer {{token}}"}}\n'
                )
            else:
                auth_lines = "    headers = {}\n"

            outputs = op.get("output", [])
            return_note = f"Returns: {', '.join(outputs)}." if outputs else ""

            tool_blocks.append(f'''
@tool
def {fn_name}({params}) -> dict:
    """{op.get("description", op_id)}. {return_note}"""
    import requests
    base_url = os.environ["{base_url_env}"]
{auth_lines}    response = requests.post(
        f"{{base_url}}/{op_id}",
        json={body_dict},
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
''')

    # ── Agents (one per role category, deduped) ───────────────────────────────
    role_to_flows: dict[str, list[str]] = {}
    for flow_id, flow in flows.items():
        cat = classify_flow(flow_id, flow)
        role_to_flows.setdefault(cat, []).append(flow_id)

    # Which tools does each role need?
    def tools_for_role(category: str) -> list[str]:
        """Return tool names used by flows in this role category."""
        needed = []
        for flow_id in role_to_flows.get(category, []):
            for step in flows[flow_id].get("steps", []):
                if step.get("type") == "call-integration":
                    t = snake(f"{step['integration']}_{step['operation']}")
                    if t not in needed:
                        needed.append(t)
        return needed or all_tool_names  # fallback: give all tools

    agent_var_names: dict[str, str] = {}
    agent_blocks: list[str] = []

    for cat, profile in ROLE_PROFILES.items():
        if cat not in role_to_flows:
            continue
        var_name = f"agent_{cat}"
        agent_var_names[cat] = var_name
        tools_list = "[" + ", ".join(tools_for_role(cat)) + "]"

        agent_blocks.append(f'''
{var_name} = Agent(
    role={repr(profile["role"])},
    goal={repr(profile["goal"])},
    backstory={repr(profile["backstory"])},
    tools={tools_list},
    llm=_LLM,
    verbose={verbose},
)
''')

    # ── Tasks (one per flow, assigned to the agent for that role) ─────────────
    task_var_names: list[str] = []
    task_blocks: list[str] = []
    # context chain: each task depends on the previous one
    prev_task_var: str | None = None

    for flow_id, flow in flows.items():
        cat = classify_flow(flow_id, flow)
        agent_var = agent_var_names.get(cat, list(agent_var_names.values())[0])
        task_var = f"task_{snake(flow_id)}"
        task_var_names.append(task_var)

        description = flow_to_task_description(flow_id, flow, entities)
        expected_output = flow_to_expected_output(flow_id, flow)

        context_line = ""
        if prev_task_var and process_type == "sequential":
            context_line = f"    context=[{prev_task_var}],\n"

        task_blocks.append(f'''
{task_var} = Task(
    description={repr(description)},
    expected_output={repr(expected_output)},
    agent={agent_var},
{context_line})
''')
        prev_task_var = task_var

    agents_list = "[" + ", ".join(agent_var_names.values()) + "]"
    tasks_list = "[" + ", ".join(task_var_names) + "]"
    process_val = f"Process.{process_type}"

    has_enums = any(e.get("type") == "enum" for e in entities.values())
    typing_imports = ["Any"]
    if has_enums:
        typing_imports.append("Literal")
    typing_line = "from typing import " + ", ".join(typing_imports)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = [
        '"""',
        "Auto-generated by agentspec — do not edit directly.",
        f"Source: {meta.get('name', 'agent')} v{meta.get('version', '1.0.0')}",
        f"Platform: crewai / {provider}",
        f"Generated: {now}",
        '"""',
        "",
        "import os",
        typing_line,
        "",
        "from crewai import Agent, Task, Crew, Process",
        "from crewai.tools import tool",
        llm_import,
        "",
        "",
        f"_LLM = {llm_class}(model={repr(model)})",
        "",
        "",
        "# ── Tools " + "─" * 67,
    ]

    lines += tool_blocks

    lines += [
        "",
        "# ── Agents " + "─" * 66,
    ]
    lines += agent_blocks

    lines += [
        "",
        "# ── Tasks " + "─" * 67,
    ]
    lines += task_blocks

    lines += [
        "",
        "# ── Crew " + "─" * 68,
        "",
        "crew = Crew(",
        f"    agents={agents_list},",
        f"    tasks={tasks_list},",
        f"    process={process_val},",
        f"    memory={memory},",
        f"    verbose={verbose},",
        ")",
        "",
        "",
        'if __name__ == "__main__":',
        f'    print("Crew: {meta.get("name")} v{meta.get("version", "1.0.0")}")',
        '    user_input = input("Describe your request: ").strip()',
        '    result = crew.kickoff(inputs={"input": user_input})',
        '    print("\\nResult:", result)',
    ]

    return "\n".join(lines) + "\n"


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Render agentspec YAML to CrewAI Python")
    parser.add_argument("spec", help="Path to agentspec YAML file")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    path = Path(args.spec)
    if not path.exists():
        print(f"ERROR: {args.spec} not found")
        sys.exit(1)

    with open(path) as f:
        spec = yaml.safe_load(f)

    code = render(spec)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(code)
        print(f"✓ Written to {out}")
    else:
        print(code)


if __name__ == "__main__":
    main()
