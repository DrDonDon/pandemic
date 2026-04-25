"""
AI research assistant via Claude API.
Conjecture analysis, proof sketching, counterexample search, intuition building.
"""
import os
from anthropic import Anthropic

_client = None

SYSTEM_PROMPT = """You are a research collaborator working with a mathematician
specializing in dynamical systems, AI theory, probability, and optimization.

Your role:
- Analyze conjectures: assess plausibility, identify edge cases, suggest approaches
- Sketch proof strategies: outline key steps, flag where gaps likely are
- Search for counterexamples: reason about boundary cases and degenerate inputs
- Build intuition: give geometric or probabilistic explanations
- Connect to literature: cite relevant results, theorems, authors by name
- Generate LaTeX: produce clean mathematical notation on request

Be direct. If a conjecture is likely false, say so and give a counterexample sketch.
If a proof sketch is flawed, say where. Don't hedge excessively.
Use proper mathematical notation in your responses."""


def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "Set ANTHROPIC_API_KEY in your environment or .env file.\n"
                "  export ANTHROPIC_API_KEY=sk-ant-..."
            )
        _client = Anthropic(api_key=api_key)
    return _client


def ask(question: str, context: str = "", model: str = "claude-opus-4-7") -> str:
    """
    Ask the AI research assistant a free-form question.
    context: optional numerical results or prior computation to include.
    """
    client = _get_client()
    user_msg = question
    if context:
        user_msg = f"Context from computation:\n{context}\n\nQuestion: {question}"

    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}]
    )
    return response.content[0].text


def analyze_conjecture(conjecture: str, evidence: str = "") -> str:
    """Assess a mathematical conjecture."""
    prompt = f"Analyze this conjecture:\n\n{conjecture}"
    if evidence:
        prompt += f"\n\nNumerical evidence:\n{evidence}"
    prompt += "\n\nAssess: plausibility, known related results, proof sketch or counterexample direction."
    return ask(prompt)


def proof_sketch(statement: str, approach_hint: str = "") -> str:
    """Sketch a proof strategy for a mathematical statement."""
    prompt = f"Sketch a proof of:\n\n{statement}"
    if approach_hint:
        prompt += f"\n\nApproach hint: {approach_hint}"
    prompt += "\n\nOutline the key steps. Flag where the hard parts are."
    return ask(prompt)


def find_counterexample(statement: str) -> str:
    """Try to find or construct a counterexample."""
    prompt = (f"Try to find a counterexample to:\n\n{statement}\n\n"
              "If you find one, give it explicitly. "
              "If you think it's true, explain why counterexamples are hard to find.")
    return ask(prompt)


def explain_intuition(concept: str, level: str = "research") -> str:
    """Build geometric/probabilistic intuition for a concept."""
    prompt = (f"Give a deep intuitive explanation of: {concept}\n\n"
              f"Target: {level}-level mathematician. "
              "Use geometry, probability, or physical analogies. Avoid pure formalism.")
    return ask(prompt)


def to_latex(description: str) -> str:
    """Convert a mathematical description to clean LaTeX."""
    prompt = (f"Convert this to clean LaTeX (equations + surrounding text):\n\n{description}\n\n"
              "Output only the LaTeX, ready to paste into a paper.")
    return ask(prompt)


def literature_hint(topic: str) -> str:
    """Get key references and theorems for a topic."""
    prompt = (f"For the topic: {topic}\n\n"
              "List: key theorems (with names), seminal papers (author, year, title), "
              "and what to search on ArXiv. Be specific.")
    return ask(prompt)


def chat(history: list = None) -> list:
    """
    Multi-turn research chat. Pass history to continue a conversation.
    Returns updated history.

    Usage:
        h = chat()           # starts new conversation
        h = chat(h)          # continues
    """
    from rich.console import Console
    from rich.markdown import Markdown
    console = Console()

    if history is None:
        history = []
        console.print("[bold green]Math Research Assistant[/bold green] — type 'quit' to exit\n")

    client = _get_client()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.lower() in ("quit", "exit", "q"):
            break
        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=history
        )
        reply = response.content[0].text
        history.append({"role": "assistant", "content": reply})

        console.print("\n[bold blue]Assistant:[/bold blue]")
        console.print(Markdown(reply))
        console.print()

    return history
