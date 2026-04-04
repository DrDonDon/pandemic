#!/usr/bin/env python3
"""
agentspec validator — checks a YAML agent spec against the agentspec schema
and runs semantic validation that JSON Schema can't catch.

Usage:
    python validate.py <spec.yaml> [<spec.yaml> ...]
    python validate.py examples/billing-dispute.yaml
"""

import json
import sys
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml jsonschema")
    sys.exit(1)

try:
    import jsonschema
except ImportError:
    print("ERROR: jsonschema not installed. Run: pip install pyyaml jsonschema")
    sys.exit(1)


SCHEMA_PATH = Path(__file__).parent.parent / "schema" / "agentspec.schema.json"
ERRORS = []
WARNINGS = []


def error(msg: str):
    ERRORS.append(f"  ✗ ERROR: {msg}")


def warn(msg: str):
    WARNINGS.append(f"  ⚠ WARN:  {msg}")


def validate_file(spec_path: str) -> bool:
    ERRORS.clear()
    WARNINGS.clear()
    path = Path(spec_path)

    if not path.exists():
        print(f"✗ File not found: {spec_path}")
        return False

    # Load YAML
    try:
        with open(path) as f:
            spec = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(f"✗ YAML parse error in {spec_path}:\n  {e}")
        return False

    # JSON Schema validation
    try:
        with open(SCHEMA_PATH) as f:
            schema = json.load(f)
    except FileNotFoundError:
        print(f"✗ Schema not found at {SCHEMA_PATH}")
        return False

    validator = jsonschema.Draft202012Validator(schema)
    schema_errors = sorted(validator.iter_errors(spec), key=lambda e: e.path)
    for e in schema_errors:
        path_str = " → ".join(str(p) for p in e.absolute_path) or "(root)"
        error(f"[{path_str}] {e.message}")

    if schema_errors:
        _print_results(spec_path)
        return False

    # Semantic validation — things JSON Schema can't enforce
    _check_flow_references(spec)
    _check_intent_flow_references(spec)
    _check_entity_references(spec)
    _check_integration_references(spec)
    _check_entry_flow(spec)
    _check_fallback_escalation_queue(spec)
    _check_enum_entity_values(spec)
    _check_branch_targets(spec)
    _check_handoff_entities(spec)

    _print_results(spec_path)
    return len(ERRORS) == 0


def _check_flow_references(spec):
    """Every flow referenced by a step must exist."""
    defined_flows = set(spec.get("flows", {}).keys())
    for flow_id, flow in spec.get("flows", {}).items():
        for step in flow.get("steps", []):
            if step.get("type") == "handoff-flow":
                target = step.get("flow")
                if target and target not in defined_flows:
                    error(f"flows.{flow_id}.steps.{step['id']}: handoff-flow target '{target}' is not defined in flows")
            for field in ("then", "else"):
                target = step.get(field)
                if target and target not in defined_flows:
                    # Could be a step ID within the same flow — check both
                    step_ids = {s["id"] for s in flow.get("steps", [])}
                    if target not in step_ids:
                        error(f"flows.{flow_id}.steps.{step['id']}: branch target '{target}' is not a defined flow or step ID")


def _check_intent_flow_references(spec):
    """Every intent's triggers_flow must reference a defined flow."""
    defined_flows = set(spec.get("flows", {}).keys())
    for intent_id, intent in spec.get("intents", {}).items():
        target = intent.get("triggers_flow")
        if target and target not in defined_flows:
            error(f"intents.{intent_id}: triggers_flow '{target}' is not defined in flows")


def _check_entity_references(spec):
    """Entity names used in flow steps and collects must exist in entities."""
    defined_entities = set(spec.get("entities", {}).keys())
    for flow_id, flow in spec.get("flows", {}).items():
        for entity_ref in flow.get("collects", []):
            if entity_ref not in defined_entities:
                error(f"flows.{flow_id}.collects: '{entity_ref}' is not defined in entities")
        for step in flow.get("steps", []):
            entity_ref = step.get("entity")
            if entity_ref and entity_ref not in defined_entities:
                error(f"flows.{flow_id}.steps.{step['id']}: entity '{entity_ref}' is not defined in entities")
            for ref in step.get("handoff_entities", []):
                if ref not in defined_entities:
                    error(f"flows.{flow_id}.steps.{step['id']}: handoff_entities '{ref}' is not defined in entities")


def _check_integration_references(spec):
    """Integration and operation names referenced in steps must exist."""
    defined_integrations = spec.get("integrations", {})
    for flow_id, flow in spec.get("flows", {}).items():
        for step in flow.get("steps", []):
            if step.get("type") == "call-integration":
                integration_name = step.get("integration")
                operation_name = step.get("operation")
                if integration_name not in defined_integrations:
                    error(f"flows.{flow_id}.steps.{step['id']}: integration '{integration_name}' is not defined in integrations")
                elif operation_name:
                    ops = defined_integrations[integration_name].get("operations", {})
                    if operation_name not in ops:
                        error(f"flows.{flow_id}.steps.{step['id']}: operation '{operation_name}' is not defined in integrations.{integration_name}.operations")


def _check_entry_flow(spec):
    """Exactly one flow must be marked entry: true."""
    entry_flows = [fid for fid, f in spec.get("flows", {}).items() if f.get("entry")]
    if len(entry_flows) == 0:
        warn("No flow has 'entry: true'. Deployers will not know where to start.")
    elif len(entry_flows) > 1:
        error(f"Multiple entry flows defined: {entry_flows}. Exactly one flow should be the entry point.")


def _check_fallback_escalation_queue(spec):
    """If fallback.final_action is 'escalate', escalation_queue must be set."""
    fallback = spec.get("fallback", {})
    if fallback.get("final_action") == "escalate" and not fallback.get("escalation_queue"):
        error("fallback.final_action is 'escalate' but fallback.escalation_queue is not set")


def _check_enum_entity_values(spec):
    """Entities with type 'enum' must have at least 2 values."""
    for entity_id, entity in spec.get("entities", {}).items():
        if entity.get("type") == "enum":
            values = entity.get("values", [])
            if len(values) < 2:
                error(f"entities.{entity_id}: type is 'enum' but fewer than 2 values defined")


def _check_branch_targets(spec):
    """Branch steps must have both 'then' and 'else' defined."""
    for flow_id, flow in spec.get("flows", {}).items():
        for step in flow.get("steps", []):
            if step.get("type") == "branch":
                if not step.get("then"):
                    error(f"flows.{flow_id}.steps.{step['id']}: branch step missing 'then'")
                if not step.get("else"):
                    error(f"flows.{flow_id}.steps.{step['id']}: branch step missing 'else'")
                if not step.get("condition"):
                    error(f"flows.{flow_id}.steps.{step['id']}: branch step missing 'condition'")


def _check_handoff_entities(spec):
    """Warn if escalation steps don't include account_number — hard to work a ticket without it."""
    defined_entities = set(spec.get("entities", {}).keys())
    for flow_id, flow in spec.get("flows", {}).items():
        for step in flow.get("steps", []):
            if step.get("type") == "escalate":
                handoff = step.get("handoff_entities", [])
                if "account_number" in defined_entities and "account_number" not in handoff:
                    warn(f"flows.{flow_id}.steps.{step['id']}: escalate step doesn't include 'account_number' in handoff_entities — specialists will need to re-verify")


def _print_results(spec_path: str):
    total = len(ERRORS) + len(WARNINGS)
    if total == 0:
        print(f"✓ {spec_path} — valid")
        return

    print(f"\n{spec_path}")
    for msg in ERRORS:
        print(msg)
    for msg in WARNINGS:
        print(msg)
    print(f"\n  {len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    files = sys.argv[1:]
    results = [validate_file(f) for f in files]

    failed = results.count(False)
    if len(files) > 1:
        print(f"\n{'─' * 40}")
        print(f"{len(files) - failed}/{len(files)} specs valid")

    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
