"""Run GPT Researcher on a query and save the markdown report to research/."""
import argparse
import asyncio
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_QUERY = (
    "Healthify (formerly HealthifyMe), the Bengaluru AI nutrition and weight-loss company: "
    "business model, products (AI coach Ria, GLP-1 programme), financials FY22-FY25, funding, "
    "Novo Nordisk partnership, the 2026 merger with US-based Berry Street, competitors, and key risks"
)


async def run(query: str, report_type: str) -> str:
    from gpt_researcher import GPTResearcher

    researcher = GPTResearcher(query=query, report_type=report_type)
    await researcher.conduct_research()
    report = await researcher.write_report()
    sources = researcher.get_source_urls()
    if sources:
        report += "\n\n## Retrieved source URLs\n" + "\n".join(f"- {u}" for u in sources)
    return report


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default=DEFAULT_QUERY)
    parser.add_argument("--report-type", default="research_report",
                        help="research_report | detailed_report | resource_report | outline_report")
    parser.add_argument("--out", help="output path (default: research/<slug>-gptr.md)")
    args = parser.parse_args()

    if not (os.getenv("OPENAI_API_KEY") or os.getenv("FAST_LLM")):
        sys.exit("OPENAI_API_KEY is not set (or configure FAST_LLM/SMART_LLM for another provider). See .env.example.")

    report = asyncio.run(run(args.query, args.report_type))
    slug = re.sub(r"[^a-z0-9]+", "-", args.query.lower().split(",")[0].split("(")[0]).strip("-")[:40]
    out = Path(args.out or f"research/{slug}-gptr.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report)
    print(f"Report written to {out}")


if __name__ == "__main__":
    main()
