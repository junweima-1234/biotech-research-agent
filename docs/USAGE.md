# Usage Guide

## Installation

```bash
# Clone repository
git clone https://github.com/junweima-1234/biotech-research-agent.git
cd biotech-research-agent

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

### 1. Copy environment template
```bash
cp .env.example .env
```

### 2. Add API keys to `.env`
```bash
# Get Gemini API key from: https://aistudio.google.com/apikey
GEMINI_API_KEY=your_gemini_key_here

# Get Tavily API key from: https://tavily.com
TAVILY_API_KEY=your_tavily_key_here
```

### 3. Verify configuration
```bash
python -m biotech_agent config
```

You should see:
```
✅ GEMINI_API_KEY: Set
✅ TAVILY_API_KEY: Set
```

## Usage

### Command Line Interface

#### Basic Analysis
```bash
python -m biotech_agent analyze --ticker AMGN --company "Amgen"
```

#### Save to JSON
```bash
python -m biotech_agent analyze --ticker NVAX --company "Novavax" --format json --output report.json
```

#### Save to Markdown
```bash
python -m biotech_agent analyze --ticker BNTX --company "BioNTech" --output report.md
```

#### Verbose Mode (see logs)
```bash
python -m biotech_agent analyze --ticker MRNA --company "Moderna" --verbose
```

#### Show Version
```bash
python -m biotech_agent version
```

### Python Script

```python
import asyncio
from src.orchestrator import BiotechResearchOrchestrator

async def main():
    orchestrator = BiotechResearchOrchestrator()
    report = await orchestrator.analyze("AMGN", "Amgen Inc.")
    
    # Access results
    print(f"Disease: {report.disease_analysis.target_disease}")
    print(f"Pipeline: {report.clinical_data.pipeline_stage}")
    print(f"Recommendation: {report.investment_thesis.recommendation}")
    
    # Format as markdown
    md_report = orchestrator.format_report_markdown(report)
    print(md_report)

if __name__ == "__main__":
    asyncio.run(main())
```

### Jupyter Notebook

```python
from src.orchestrator import BiotechResearchOrchestrator
import asyncio

# Initialize orchestrator
orchestrator = BiotechResearchOrchestrator()

# Run analysis
report = await orchestrator.analyze("AMGN", "Amgen")

# Display results
display_markdown(orchestrator.format_report_markdown(report))
```

## Output Formats

### Markdown Format (default)
- Human-readable report with sections
- Includes all analysis from 5 workers
- Good for presentations and documents

### JSON Format
- Machine-readable structured data
- Contains all metadata and source references
- Good for further processing or storage

### Example Output Structure

```json
{
  "ticker": "AMGN",
  "company_name": "Amgen Inc.",
  "report_date": "2024-01-15T10:30:00",
  "disease_analysis": {
    "target_disease": "Oncology",
    "mechanism_of_action": "Bispecific antibody",
    ...
  },
  "clinical_data": {
    "pipeline_stage": "Phase 3",
    "indications": ["Lung Cancer", "Colorectal Cancer"],
    ...
  },
  ...
}
```

## Click CLI Options

### `analyze` Command

```
Options:
  --ticker TEXT              Stock ticker symbol (required) [default: None]
  --company TEXT             Company name (required) [default: None]
  --format [json|markdown]   Output format [default: markdown]
  --output TEXT              Output file path (optional) [default: None]
  --verbose                  Enable verbose logging [default: False]
  --help                     Show help message
```

### `config` Command

```
$ python -m biotech_agent config

Shows configuration status for all required API keys.
```

### `version` Command

```
$ python -m biotech_agent version

Displays the current version of the agent.
```

## Examples

### Example 1: Quick Analysis
```bash
python -m biotech_agent analyze --ticker AMGN --company "Amgen"
```

### Example 2: Batch Analysis with Python
```python
import asyncio
from src.orchestrator import BiotechResearchOrchestrator

async def analyze_multiple():
    orchestrator = BiotechResearchOrchestrator()
    
    companies = [
        ("AMGN", "Amgen"),
        ("NVAX", "Novavax"),
        ("BNTX", "BioNTech")
    ]
    
    for ticker, company in companies:
        print(f"\nAnalyzing {company}...")
        report = await orchestrator.analyze(ticker, company)
        print(f"Recommendation: {report.investment_thesis.recommendation}")

asyncio.run(analyze_multiple())
```

### Example 3: Save Reports
```bash
# Create reports directory
mkdir -p reports

# Analyze multiple companies
python -m biotech_agent analyze --ticker AMGN --company "Amgen" --output reports/AMGN.md
python -m biotech_agent analyze --ticker NVAX --company "Novavax" --format json --output reports/NVAX.json
```

## Troubleshooting

### Error: "Missing required environment variables"
**Solution**: Run `cp .env.example .env` and add your API keys

### Error: "Failed to initialize Gemini"
**Solution**: Check your GEMINI_API_KEY is valid (get from https://aistudio.google.com/apikey)

### Error: "Tavily API error"
**Solution**: Check your TAVILY_API_KEY is valid (get from https://tavily.com)

### Analysis takes very long
**Normal**: First run may take 10-15 minutes due to API latency
**Optimization**: Cache search results for subsequent analyses

### Missing data in report
**Expected**: Some data may be unavailable for smaller companies
**Behavior**: Report will contain "N/A" for unavailable fields

## Performance Tips

1. **Use verbose mode sparingly**: `--verbose` adds log output overhead
2. **Batch analyses offline**: Run multiple analyses during off-peak hours
3. **Cache results**: Store JSON reports for repeated analysis
4. **Monitor API quotas**: Check Tavily and Gemini usage limits

## Next Steps

- Review generated reports in `reports/` directory
- Customize worker prompts in `src/workers/` for specific analysis
- Add additional data sources by extending WebSearchTool
- Integrate with your workflow management system
