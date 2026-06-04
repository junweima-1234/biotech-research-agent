"""Example script for analyzing a biotech company"""

import asyncio
import json
from pathlib import Path

from src.orchestrator import BiotechResearchOrchestrator


async def main():
    """Run example analysis"""
    
    orchestrator = BiotechResearchOrchestrator()
    
    ticker = "AMGN"
    company_name = "Amgen Inc."
    
    print(f"\n{'='*60}")
    print(f"Analyzing: {company_name} ({ticker})")
    print(f"{'='*60}\n")
    
    report = await orchestrator.analyze(ticker, company_name)
    
    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)
    
    report_json_path = output_dir / f"{ticker}_report.json"
    with open(report_json_path, "w") as f:
        json.dump(report.dict(), f, indent=2, default=str)
    
    print(f"\n✅ JSON Report saved to: {report_json_path}")
    
    report_md = orchestrator.format_report_markdown(report)
    report_md_path = output_dir / f"{ticker}_report.md"
    with open(report_md_path, "w") as f:
        f.write(report_md)
    
    print(f"✅ Markdown Report saved to: {report_md_path}")
    
    print(f"\n{'='*60}")
    print("Report Summary")
    print(f"{'='*60}\n")
    
    if report.investment_thesis:
        print(f"Recommendation: {report.investment_thesis.recommendation}")
        print(f"\nVariant Perception:\n{report.investment_thesis.variant_perception}\n")


if __name__ == "__main__":
    asyncio.run(main())
