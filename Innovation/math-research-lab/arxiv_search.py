"""
ArXiv search and paper retrieval.
"""
import arxiv
from rich.console import Console
from rich.table import Table

console = Console()


def search(query: str, max_results: int = 10, sort_by="relevance") -> list:
    """
    Search ArXiv. Returns list of result dicts.
    sort_by: "relevance" | "lastUpdatedDate" | "submittedDate"
    """
    sort_map = {
        "relevance": arxiv.SortCriterion.Relevance,
        "lastUpdatedDate": arxiv.SortCriterion.LastUpdatedDate,
        "submittedDate": arxiv.SortCriterion.SubmittedDate,
    }
    client = arxiv.Client()
    search_obj = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=sort_map.get(sort_by, arxiv.SortCriterion.Relevance),
    )
    results = []
    for r in client.results(search_obj):
        results.append({
            "title": r.title,
            "authors": [a.name for a in r.authors],
            "abstract": r.summary,
            "url": r.entry_id,
            "pdf_url": r.pdf_url,
            "published": str(r.published.date()),
            "categories": r.categories,
        })
    return results


def print_results(results: list, show_abstract: bool = False):
    """Pretty-print search results."""
    table = Table(title=f"ArXiv Results ({len(results)} papers)", show_lines=True)
    table.add_column("#", width=3)
    table.add_column("Title", min_width=30)
    table.add_column("Authors", max_width=25)
    table.add_column("Date", width=12)
    table.add_column("URL", max_width=40)

    for i, r in enumerate(results, 1):
        authors = ", ".join(r["authors"][:3])
        if len(r["authors"]) > 3:
            authors += " et al."
        table.add_row(str(i), r["title"], authors, r["published"], r["url"])

    console.print(table)

    if show_abstract:
        for i, r in enumerate(results, 1):
            console.print(f"\n[bold]{i}. {r['title']}[/bold]")
            console.print(r["abstract"][:600] + "..." if len(r["abstract"]) > 600
                         else r["abstract"])


def search_for_topic(topic: str, areas: list = None) -> list:
    """
    Build a targeted ArXiv query for a math research topic.
    areas: e.g. ["math.DS", "math.PR", "math.OC", "cs.LG"]
    """
    query = topic
    if areas:
        cat_filter = " OR ".join(f"cat:{a}" for a in areas)
        query = f"({topic}) AND ({cat_filter})"
    return search(query, max_results=15)
