"""Command-line interface for Biotech Research Agent"""

import click
import asyncio
import json
import logging
import sys
from pathlib import Path
from datetime import datetime

from src.orchestrator import BiotechResearchOrchestrator
from src.tools.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)

logger = logging.getLogger(__name__)


@click.group()
def cli():
    """Autonomous Biotech Fundamental Research Agent"""
    pass


@cli.command()
@click.option(
    '--ticker',
    required=True,
    help='Stock ticker symbol (e.g., AMGN)',
    type=str
)
@click.option(
    '--company',
    required=True,
    help='Company name (e.g., "Amgen Inc.")',
    type=str
)
@click.option(
    '--format',
    default='markdown',
    type=click.Choice(['json', 'markdown']),
    help='Output format'
)
@click.option(
    '--output',
    default=None,
    type=str,
    help='Output file path (optional)'
)
@click.option(
    '--verbose',
    is_flag=True,
    help='Enable verbose logging'
)
def analyze(ticker: str, company: str, format: str, output: str, verbose: bool):
    """
    Analyze a biotech company and generate comprehensive research report
    
    Examples:
    
        python -m biotech_agent analyze --ticker AMGN --company "Amgen"
        
        python -m biotech_agent analyze --ticker NVAX --company "Novavax" --format json
        
        python -m biotech_agent analyze --ticker BNTX --company "BioNTech" --verbose
        
        python -m biotech_agent analyze --ticker MRNA --company "Moderna" --output report.json
    """
    
    # Set logging level
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        click.secho(f"❌ Configuration Error: {e}", fg='red')
        sys.exit(1)
    
    click.secho(f"🚀 Starting analysis for {company} ({ticker})", fg='cyan', bold=True)
    click.echo()
    
    try:
        # Run async analysis
        report = asyncio.run(_run_analysis(ticker, company))
        
        # Format output
        if format == 'json':
            output_data = report.dict()
            output_text = json.dumps(output_data, indent=2, default=str)
        else:  # markdown
            orchestrator = BiotechResearchOrchestrator()
            output_text = orchestrator.format_report_markdown(report)
        
        # Save or print
        if output:
            output_path = Path(output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(output_text)
            click.secho(f"✅ Report saved to: {output_path.absolute()}", fg='green')
        else:
            click.echo()
            click.echo(output_text)
        
        click.echo()
        click.secho(f"✅ Analysis complete!", fg='green', bold=True)
        
    except Exception as e:
        click.secho(f"❌ Analysis failed: {e}", fg='red')
        logger.exception("Detailed error:")
        sys.exit(1)


async def _run_analysis(ticker: str, company: str):
    """Internal async function to run analysis"""
    orchestrator = BiotechResearchOrchestrator()
    report = await orchestrator.analyze(ticker, company)
    return report


@cli.command()
def config():
    """Check configuration status"""
    click.secho("🔧 Configuration Status", fg='cyan', bold=True)
    click.echo()
    
    checks = {
        "GEMINI_API_KEY": Config.GEMINI_API_KEY,
        "TAVILY_API_KEY": Config.TAVILY_API_KEY,
    }
    
    all_good = True
    for key, value in checks.items():
        status = "✅" if value else "❌"
        click.echo(f"{status} {key}: {'Set' if value else 'Not set'}")
        if not value:
            all_good = False
    
    click.echo()
    if all_good:
        click.secho("✅ All required configurations are set!", fg='green')
    else:
        click.secho("⚠️  Some configurations are missing. Please set them in .env file.", fg='yellow')
        click.echo()
        click.echo("Run: cp .env.example .env")
        click.echo("Then edit .env and add your API keys")


@cli.command()
def version():
    """Show version information"""
    from biotech_agent import __version__
    click.echo(f"Biotech Research Agent v{__version__}")


if __name__ == '__main__':
    cli()
