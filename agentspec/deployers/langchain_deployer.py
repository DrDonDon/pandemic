"""
agentspec → LangChain deployer

Reads an agentspec YAML and generates a self-contained Python file with:
  - Pydantic input schemas for every integration operation
  - @tool decorated functions for every operation
  - A system prompt assembled from flows, intents, and fallback rules
  - A LangChain AgentExecutor wired up and ready to run

Output is a Python file — no API calls are made during rendering.
The generated file requires credentials at runtime (env vars).

Usage:
    python deployers/langchain_deployer.py examples/billing-dispute.yaml
    python deployers/langchain_deployer.py examples/billing-dispute.yaml --output out/billing_dispute_langchain.py
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
    """kebab-case or any-string → snake_case"""
    return re.sub(r"[-\s]+", "_", s).lower()


def entity_to_pydantic_type(entity: dict) -> str:
    type_map = {
        "string": "str",
        "number": "float",
        "boolean": "bool",
        "date": "str",
        "phone": "str",
        "email": "str",
        "account-number": "str",
        "enum": "str",
    }
    return type_map.get(entity.get("type", "string"), "str")


def entity_to_field(entity_id: str, entity: dict) -> str:
    """Generate a Pydantic Field(...) definition for an entity."""
    py_type = entity_to_pydantic_type(entity)
    parts = [f'description="{entity.get("description", entity_id)}"']

    # Enum literal type
    if entity.get("type") == "enum":
        values = []
        for v in entity.get("values", []):
            values.append(v if isinstance(v, str) else v["value"])
        if values:
            quoted = ", ".join(f'"{v}"' for v in values)
            py_type = f"Literal[{quoted}]"

    # Validation
    val = entity.get("validation", {})
    if "min" in val:
        parts.append(f'ge={val["min"]}')
    if "max" in val:
        parts.append(f'le={val["max"]}')

    field_args = ", ".join(parts)
    optional = "" if not entity.get("isList") else "List"
    if entity.get("isList"):
        return f"    {snake(entity_id)}: List[{py_type}] = Field(..., {field_args})"
    return f"    {snake(entity_id)}: {py_type} = Field(..., {field_args})"


def build_system_prompt(spec: dict) -> str:
    """Assemble a system prompt from flows, intents, and fallback."""
    meta = spec.get("metadata", {})
    lines = [
        f"You are {meta.get('name', 'an AI agent')}.",
        meta.get("description", ""),
        "",
        "## Your capabilities",
    ]

    for intent_id, intent in spec.get("intents", {}).items():
        lines.append(f"- {intent.get('description', intent_id)}")

    lines += ["", "## Rules you must follow"]

    # Extract rules from flow descriptions and escalation steps
    for flow_id, flow in spec.get("flows", {}).items():
        desc = flow.get("description", "").strip()
        if desc:
            # One-line summary per flow
            first_line = desc.split("\n")[0].strip()
            lines.append(f"- {first_line}")

        for step in flow.get("steps", []):
            if step.get("type") == "escalate":
                queue = step.get("queue", "human agents")
                priority = step.get("priority", "normal")
                lines.append(
                    f"- When escalating to {queue}, pass all collected entity values "
                    f"and set priority to {priority}."
                )

    # Fallback rules
    fallback = spec.get("fallback", {})
    max_retries = fallback.get("max_retries", 3)
    final_action = fallback.get("final_action", "escalate")
    lines += [
        "",
        f"## Fallback behaviour",
        f"- If you cannot understand the user after {max_retries} attempts, {final_action}.",
    ]
    if final_action == "escalate":
        q = fallback.get("escalation_queue", "the support queue")
        lines.append(f"- Escalate to: {q}")

    # Redact reminder
    redacted = [
        eid for eid, e in spec.get("entities", {}).items() if e.get("redact")
    ]
    if redacted:
        lines += [
            "",
            "## Privacy",
            f"- Never repeat or log these values: {', '.join(redacted)}.",
        ]

    return "\n".join(lines)


# ── Code generation ───────────────────────────────────────────────────────────

def render(spec: dict) -> str:
    meta = spec.get("metadata", {})
    overrides = spec.get("overrides", {}).get("langchain", {})
    integrations = spec.get("integrations", {})
    entities = spec.get("entities", {})

    provider = overrides.get("provider", "anthropic")
    model = overrides.get("model", "claude-3-5-sonnet-20241022")
    temperature = overrides.get("temperature", 0)
    max_iterations = overrides.get("max_iterations", 10)
    memory_window = overrides.get("memory_window", 10)

    llm_import, llm_class = {
        "anthropic": ("from langchain_anthropic import ChatAnthropic", "ChatAnthropic"),
        "openai":    ("from langchain_openai import ChatOpenAI", "ChatOpenAI"),
        "google":    ("from langchain_google_genai import ChatGoogleGenerativeAI", "ChatGoogleGenerativeAI"),
        "bedrock":   ("from langchain_aws import ChatBedrock", "ChatBedrock"),
    }.get(provider, ("from langchain_anthropic import ChatAnthropic", "ChatAnthropic"))

    # Collect which entities appear as inputs to operations (for schema classes)
    op_schemas: list[dict] = []
    tool_functions: list[str] = []
    tool_names: list[str] = []

    for int_id, integration in integrations.items():
        base_url_env = integration.get("base_url_env", f"{snake(int_id).upper()}_BASE_URL")
        auth = integration.get("auth", "none")

        for op_id, op in integration.get("operations", {}).items():
            class_name = "".join(w.title() for w in re.split(r"[-_]", f"{int_id}_{op_id}")) + "Input"
            fn_name = snake(f"{int_id}_{op_id}")
            tool_names.append(fn_name)

            # Pydantic schema for inputs
            input_fields = []
            for entity_id in op.get("input", []):
                entity = entities.get(entity_id, {"type": "string", "description": entity_id})
                input_fields.append(entity_to_field(entity_id, entity))

            schema_lines = [f"class {class_name}(BaseModel):"]
            if input_fields:
                schema_lines += input_fields
            else:
                schema_lines.append("    pass")
            op_schemas.append("\n".join(schema_lines))

            # Auth header snippet
            auth_snippet = ""
            if auth == "api-key":
                auth_snippet = (
                    f'    api_key = os.environ.get("{snake(int_id).upper()}_API_KEY")\n'
                    f'    headers = {{"Authorization": f"Bearer {{api_key}}"}}\n'
                )
            elif auth == "oauth2":
                auth_snippet = (
                    f'    token = os.environ.get("{snake(int_id).upper()}_ACCESS_TOKEN")\n'
                    f'    headers = {{"Authorization": f"Bearer {{token}}"}}\n'
                )
            else:
                auth_snippet = "    headers = {}\n"

            # Input params for function signature
            params = ", ".join(
                f"{snake(eid)}: {entity_to_pydantic_type(entities.get(eid, {'type': 'string'}))}"
                for eid in op.get("input", [])
            )
            body_dict = "{" + ", ".join(f'"{eid}": {snake(eid)}' for eid in op.get("input", [])) + "}"
            outputs = op.get("output", [])
            return_note = f"Returns: {', '.join(outputs)}." if outputs else "Returns: operation result."

            fn = f'''
@tool("{fn_name}", args_schema={class_name})
def {fn_name}({params}) -> dict:
    """{op.get("description", op_id)}. {return_note}"""
    import requests
    base_url = os.environ["{base_url_env}"]
{auth_snippet}    response = requests.post(
        f"{{base_url}}/{op_id}",
        json={body_dict},
        headers=headers,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
'''
            tool_functions.append(fn)

    system_prompt = build_system_prompt(spec)
    tool_list = "[" + ", ".join(tool_names) + "]"

    # Need Literal import only if any enum entities are used
    has_enums = any(e.get("type") == "enum" for e in entities.values())
    has_lists = any(e.get("isList") for e in entities.values())

    typing_imports = ["Any"]
    if has_enums:
        typing_imports.append("Literal")
    if has_lists:
        typing_imports.append("List")
    typing_line = "from typing import " + ", ".join(typing_imports)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = [
        f'"""',
        f"Auto-generated by agentspec — do not edit directly.",
        f"Source: {meta.get('name', 'agent')} v{meta.get('version', '1.0.0')}",
        f"Platform: langchain / {provider}",
        f"Generated: {now}",
        f'"""',
        "",
        "import os",
        typing_line,
        "",
        "from pydantic import BaseModel, Field",
        "from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder",
        "from langchain_core.tools import tool",
        "from langchain.agents import AgentExecutor, create_tool_calling_agent",
        "from langchain.memory import ConversationBufferWindowMemory",
        llm_import,
        "",
        "",
        "# ── Entity input schemas " + "─" * 54,
        "",
    ]

    for schema in op_schemas:
        lines.append(schema)
        lines.append("")

    lines += [
        "",
        "# ── Tools " + "─" * 67,
    ]
    lines += tool_functions

    lines += [
        "",
        "# ── Agent " + "─" * 66,
        "",
        f"_SYSTEM_PROMPT = {repr(system_prompt)}",
        "",
        "_PROMPT = ChatPromptTemplate.from_messages([",
        '    ("system", _SYSTEM_PROMPT),',
        '    MessagesPlaceholder("chat_history"),',
        '    ("human", "{input}"),',
        '    MessagesPlaceholder("agent_scratchpad"),',
        "])",
        "",
        f"_LLM = {llm_class}(model={repr(model)}, temperature={temperature})",
        "",
        f"_TOOLS = {tool_list}",
        "",
        "_MEMORY = ConversationBufferWindowMemory(",
        f"    k={memory_window},",
        '    memory_key="chat_history",',
        "    return_messages=True,",
        ")",
        "",
        "_AGENT = create_tool_calling_agent(_LLM, _TOOLS, _PROMPT)",
        "",
        "agent_executor = AgentExecutor(",
        "    agent=_AGENT,",
        "    tools=_TOOLS,",
        "    memory=_MEMORY,",
        f"    max_iterations={max_iterations},",
        "    verbose=True,",
        "    handle_parsing_errors=True,",
        ")",
        "",
        "",
        'if __name__ == "__main__":',
        f'    print("Agent: {meta.get("name")} v{meta.get("version", "1.0.0")}")',
        '    print("Type your message. Ctrl+C to exit.\\n")',
        "    history: list = []",
        "    while True:",
        "        try:",
        '            user_input = input("You: ").strip()',
        "            if not user_input:",
        "                continue",
        '            result = agent_executor.invoke({"input": user_input})',
        '            print(f\'Agent: {result["output"]}\\n\')',
        "        except KeyboardInterrupt:",
        "            break",
    ]

    return "\n".join(lines) + "\n"


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Render agentspec YAML to LangChain Python")
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
