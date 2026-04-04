# AgentSpec — Developer Overview

> **Status:** Early prototype. Schema and validator are working. Deployers generate
> runnable Python output for LangChain and CrewAI. Enterprise platform deployers
> (Sierra, Cognigy, Google Agent Studio) are the next milestone.

---

## The Problem

Large enterprises — telcos, banks, insurers — run customer-facing AI agents on
multiple platforms simultaneously. A single agent (e.g. "billing dispute") might
live on Sierra for voice, Google Agent Studio for complex web flows, and Cognigy
for chat. When you need to update that agent, you need three teams, three separate
builds, three rounds of testing. A major update costs hundreds of hours. The
platform versions drift from each other over time, adding complexity and TCO.

There is no tool that lets you define an agent once and deploy it everywhere.

---

## The Idea

AgentSpec is to AI agents what Terraform is to cloud infrastructure.

You define an agent once in a YAML file. A deployer reads that file and generates
platform-native config or code for each target platform. Change the agent in one
place. Every platform gets updated.

```
billing-dispute.yaml
        │
        ├── → Sierra journey config
        ├── → Google Agent Studio (Dialogflow CX) agent ZIP
        ├── → Cognigy flow via REST API
        ├── → LangChain AgentExecutor (Python)
        └── → CrewAI Crew (Python)
```

---

## Core Design Principle

**The schema is capability-centric, not topology-centric.**

This is the hard part. The three enterprise platforms have completely different
structural models:

| Platform | Model | Structure |
|---|---|---|
| Sierra | Monolithic | One agent, multiple journeys inside |
| Google Agent Studio | Microservices | Many specialised agents that hand off |
| Cognigy | Hybrid | Flows within flows, configurable depth |

A schema shaped like Sierra's topology fails on Agent Studio. A schema shaped like
Cognigy's node model fails on Sierra. So the schema describes *what* the agent does —
intents, entities, flows, escalations — and each deployer handles the structural
translation.

The same insight Terraform had: HCL describes a database. The AWS provider makes
an RDS instance. The Azure provider makes an Azure SQL Database. Same spec, different
output.

---

## What's in the Repo

```
agentspec/
├── schema/
│   └── agentspec.schema.json       # JSON Schema (draft-2020-12) — the contract
├── examples/
│   ├── billing-dispute.yaml        # Full telco billing dispute agent
│   └── account-inquiry.yaml        # Read-only account inquiry agent
├── validator/
│   └── validate.py                 # CLI validator (JSON Schema + semantic checks)
├── deployers/
│   ├── render.py                   # Entry point: render --platform <name> <spec>
│   ├── langchain_deployer.py       # → LangChain AgentExecutor Python file
│   └── crewai_deployer.py          # → CrewAI Crew Python file
└── out/                            # Generated output (gitignored in production)
    ├── billing_dispute_langchain.py
    └── billing_dispute_crewai.py
```

**Dependencies:** Python 3.11+, `pyyaml`, `jsonschema`

---

## The Schema

A spec file has six sections:

### `entities`
The data the agent works with. No platform assumptions — no "slots" vs "parameters".
Supports types: `string`, `number`, `boolean`, `enum`, `date`, `phone`, `email`,
`account-number`.

```yaml
entities:
  dispute_type:
    type: enum
    description: Category of the billing dispute
    values:
      - value: incorrect-charge
        synonyms:
          - wrong charge
          - charge I don't recognise
          - unexpected charge
      - value: duplicate-charge
        synonyms:
          - charged twice
          - billed twice

  account_number:
    type: account-number
    redact: true          # masked in platform logs — maps to CX parameter.redact,
                          # Cognigy data privacy settings, etc.
    validation:
      pattern: "^\\d{10}$"
```

Key flags:
- `redact: true` — PII masking in logs. Compliance-critical for telco/finance.
- `isList: true` — collect multiple values.
- `synonyms` on enum values — map natural language variants to canonical values.
  This is what actually drives NLU quality.

### `intents`
What users can say, with training examples. Routes to a flow.

```yaml
intents:
  dispute-bill:
    description: Customer wants to dispute a charge on their bill
    triggers_flow: identify-customer
    examples:
      - "I want to dispute a charge"
      - "There's something wrong on my bill"
      - "I've been charged incorrectly"
      - "I don't recognise this charge"
```

### `integrations`
Named backend systems. URLs are always env-var references — never hardcoded.

```yaml
integrations:
  billing-api:
    type: rest-api
    base_url_env: BILLING_API_BASE_URL
    auth: oauth2
    operations:
      verify-account:
        description: Verify account number and DOB, return account status
        input: [account_number, verification_dob]
        output: [account_status, previous_dispute_count]
      create-dispute:
        input: [account_number, dispute_type, dispute_amount, billing_period]
        output: [dispute_reference]
```

### `flows`
Conversational sequences as typed steps. No platform topology — no Pages, no Nodes,
no Journeys.

Step types: `collect`, `confirm`, `call-integration`, `branch`, `handoff-flow`,
`escalate`, `message`, `end`.

```yaml
flows:
  dispute-intake:
    entry: false
    collects: [dispute_type, dispute_amount, billing_period]
    steps:
      - id: check-dispute-history
        type: branch
        condition: "previous_dispute_count >= 3"
        then: escalate-repeat-disputer
        else: collect-dispute-type

      - id: collect-dispute-type
        type: collect
        entity: dispute_type
        prompt: "What type of billing issue are you experiencing?"

      - id: create-dispute-record
        type: call-integration
        integration: billing-api
        operation: create-dispute

      - id: route-by-amount
        type: branch
        condition: "dispute_amount <= 150"
        then: auto-resolve
        else: escalate-high-value
```

### `fallback`
Global recovery behaviour.

```yaml
fallback:
  unrecognized_input: repeat-prompt
  max_retries: 3
  final_action: escalate
  escalation_queue: billing-specialists
```

### `overrides`
Platform-specific config that doesn't belong in the canonical spec.
Additive only — never changes the shared definition.

```yaml
overrides:
  sierra:
    agent_name: "Billing Dispute Agent"
    voice_channel: true
  google-agent-studio:
    location: "australia-southeast1"
    default_language_code: "en-AU"
  cognigy:
    flow_id: "billing_dispute_v1"
    nlu_connector: "cognigy-nlu"
  langchain:
    model: "claude-3-5-sonnet-20241022"
    provider: anthropic
    temperature: 0
  crewai:
    model: "claude-3-5-sonnet-20241022"
    process: sequential
```

---

## The Validator

Runs two passes:

**Pass 1 — JSON Schema:** Catches type errors, missing required fields, invalid enums.

**Pass 2 — Semantic checks:**
- All flow references in `then`/`else`/`triggers_flow` resolve to defined flows or step IDs
- All entity names in `collect` steps and `handoff_entities` exist in `entities`
- All `integration + operation` pairs resolve
- Exactly one flow has `entry: true`
- `fallback.escalation_queue` set when `final_action: escalate`
- Enum entities have ≥ 2 values
- PII-type entities warn if `redact` not set
- Escalation steps warn if `account_number` not in `handoff_entities`

```bash
$ python agentspec/validator/validate.py examples/billing-dispute.yaml

✓ examples/billing-dispute.yaml — valid
```

---

## The Deployers (current)

### LangChain

```bash
python agentspec/deployers/render.py --platform langchain examples/billing-dispute.yaml
```

Generates `out/billing_dispute_langchain.py` containing:
- **Pydantic input schemas** for every integration operation, with Literal types for
  enums, ge/le bounds from validation, and proper typing for isList entities
- **`@tool` functions** for every operation — typed signatures, auth headers from env
  vars, POST to `{base_url_env}/{operation-id}`
- **System prompt** assembled from flow descriptions, intent descriptions, fallback
  rules, and a privacy section listing all `redact: true` entities
- **`AgentExecutor`** with sliding window memory, configurable via `overrides.langchain`

The generated file runs as-is once you `pip install langchain-anthropic` and set
`BILLING_API_BASE_URL` and `BILLING_API_ACCESS_TOKEN`.

### CrewAI

```bash
python agentspec/deployers/render.py --platform crewai examples/billing-dispute.yaml
```

Generates `out/billing_dispute_crewai.py` containing:
- **`@tool` functions** (same as LangChain)
- **Agents** with role/goal/backstory, derived from flow structure:
  - Entry flow → Customer Intake Specialist
  - Flows with escalate steps → Escalation Coordinator
  - Flows with API calls → Resolution Specialist
- **Tasks** (one per flow), with descriptions and expected outputs derived from steps,
  chained sequentially so each task receives prior context
- **`Crew`** ready to `kickoff(inputs={"input": user_input})`

---

## What's Not Built Yet

These are the next milestones, roughly in priority order:

| Deployer | Status | Blocker |
|---|---|---|
| Cognigy | Not started | Need REST API credentials + existing agent export to validate translation |
| Google Agent Studio | Not started | Need GCP project + service account; Page grouping logic for consecutive collects needs validation |
| Sierra | Not started | API docs not public — needs account team access |

The validator also doesn't yet support:
- Training phrase entity annotation (annotating which spans are entities)
- Cognigy Lexicon vs. Question Node type split (handled by deployer, not schema)

---

## Known Design Gaps (from SDK research)

Discovered by comparing the schema against Dialogflow CX and Cognigy public API docs:

1. **CX Page grouping is implicit** — our sequential step model maps naturally to Cognigy's node execution model, but CX uses a state machine (Pages). The CX deployer will need to group consecutive `collect` steps into a single Page form. This is a deployer convention, not something expressed in the schema.

2. **CX webhook tag dispatch** — CX identifies which webhook handler to call via `FulfillmentInfo.tag`. The CX deployer will auto-generate tags as `{integration-name}-{operation-name}` and register them. Not expressed in the schema.

3. **Training phrase annotation** — both platforms support annotating which spans in training phrases correspond to which entities. Our `examples` are plain strings. Deferred to v1.1.

---

## Running It

```bash
# Install deps
pip install pyyaml jsonschema

# Validate a spec
python agentspec/validator/validate.py agentspec/examples/billing-dispute.yaml

# Generate LangChain code
python agentspec/deployers/render.py --platform langchain agentspec/examples/billing-dispute.yaml

# Generate CrewAI code
python agentspec/deployers/render.py --platform crewai agentspec/examples/billing-dispute.yaml
```

---

## Feedback We're Looking For

1. **Schema completeness** — does the agentspec format capture everything you'd need
   to describe a real agent on your platform? What's missing?

2. **Deployer fidelity** — if you ran the LangChain or CrewAI output against a real
   backend, what would break?

3. **The topology gap** — our sequential step model works well for Cognigy and LangChain/CrewAI.
   For CX's state machine model, the deployer has to make assumptions about Page groupings.
   Is there a better way to express this in the schema without making it platform-specific?

4. **Enterprise platform deployers** — if you have access to Cognigy, Agent Studio, or Sierra:
   what does the native config format look like for a simple 3-step agent? That's the
   fixture we need to write the deployer.
