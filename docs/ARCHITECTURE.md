# Architecture Overview

## System Design

The Biotech Research Agent follows a **Worker/Orchestrator** pattern with clear modular separation of concerns.

```
                    INPUT
                      |
                      v
            [Orchestrator Agent]
                      |
        ______________|______________
        |      |      |      |      |
        v      v      v      v      v
      W1     W2     W3     W4     W5
    (Disease)(Drug)(Comm)(Value)(Synth)
        |      |      |      |      |
        |______|______|______|______|
                      |
                      v
                   OUTPUT
              (Research Report)
```

## Components

### 1. Orchestrator (`src/orchestrator.py`)

- **Role**: Central coordinator
- **Responsibilities**:
  - Receives company ticker and name as input
  - Delegates to 5 workers in parallel (Workers 1-4)
  - Waits for all workers to complete
  - Passes aggregated results to synthesis worker (Worker 5)
  - Returns final ResearchReport

### 2. Workers (5 Independent Agents)

#### Worker 1: Disease Biology (`src/workers/disease_biology.py`)
- **Input**: Company name, ticker
- **Process**:
  1. Web search for disease mechanisms, epidemiology
  2. Query Gemini 1.5 Pro for analysis
  3. Extract MoA, patient population, unmet needs
- **Output**: DiseaseAnalysis
- **Key Metrics**: target disease, epidemiology, SoC

#### Worker 2: Drug Profile (`src/workers/drug_profile.py`)
- **Input**: Company name, ticker
- **Process**:
  1. Search for clinical trial data (ClinicalTrials.gov)
  2. Extract ORR, PFS, OS, Grade 3+ AE
  3. Assess pipeline stage
- **Output**: ClinicalData
- **Key Metrics**: pipeline stage, efficacy/safety data

#### Worker 3: Commercialization (`src/workers/commercialization.py`)
- **Input**: Company name, ticker
- **Process**:
  1. Search competitor pipelines, market size
  2. Analyze pricing/reimbursement landscape
  3. Assess standard of care shifts
- **Output**: CompetitiveLandscape
- **Key Metrics**: TAM, competitors, pricing

#### Worker 4: Valuation (`src/workers/valuation.py`)
- **Input**: Company name, ticker
- **Process**:
  1. Search financial forecasts, analyst reports
  2. Calculate probability of success by stage
  3. Estimate peak sales, rNPV
- **Output**: ValuationFramework
- **Key Metrics**: peak sales, PoS, NPV

#### Worker 5: Synthesis (`src/workers/synthesis.py`)
- **Input**: All 4 worker outputs
- **Process**:
  1. Consolidate findings into cohesive narrative
  2. Identify variant perception (non-consensus views)
  3. Extract upcoming catalysts, risks
  4. Generate investment recommendation
- **Output**: ResearchReport (complete)

### 3. Tools

#### Web Search Tool (`src/tools/web_search.py`)
- **Provider**: Tavily API
- **Capabilities**:
  - Real-time web search with source tracking
  - Support for parallel searches
  - URL citations with retrieval dates

#### LLM Interface (`src/tools/llm_interface.py`)
- **Provider**: Google Gemini 1.5 Pro
- **Capabilities**:
  - Long context window (1M tokens)
  - Async/await support
  - Structured prompt handling

#### Configuration (`src/tools/config.py`)
- Environment variable management
- API key validation
- Default settings

### 4. Data Models (`src/schemas/models.py`)

All outputs are validated Pydantic models:

```
ResearchReport
├── DiseaseAnalysis
│   ├── target_disease: str
│   ├── mechanism_of_action: str
│   ├── epidemiology: str
│   ├── unmet_medical_needs: str
│   ├── standard_of_care: str
│   └── sources: List[SourceReference]
├── ClinicalData
│   ├── pipeline_stage: str
│   ├── indications: List[str]
│   ├── clinical_data_points: List[ClinicalDataPoint]
│   └── safety_profile: str
├── CompetitiveLandscape
│   ├── addressable_market_size: str
│   ├── competitors: List[CompetitorInfo]
│   ├── pricing_benchmarks: Dict
│   └── reimbursement_status: str
├── ValuationFramework
│   ├── peak_sales_estimate: str
│   ├── probability_of_success: Dict[str, float]
│   ├── risk_adjusted_npv: str
│   └── assumptions: List[ValuationAssumption]
└── InvestmentThesis
    ├── variant_perception: str
    ├── key_investment_highlights: List[str]
    ├── key_risks: List[str]
    ├── upcoming_catalysts: List[Catalyst]
    ├── valuation_verdict: str
    ├── price_targets: Dict
    └── recommendation: str
```

## Data Flow

1. **Input**: User provides ticker + company name
2. **Worker 1**: Analyzes disease biology → DiseaseAnalysis
3. **Worker 2**: Extracts clinical data → ClinicalData
4. **Worker 3**: Analyzes competitive landscape → CompetitiveLandscape
5. **Worker 4**: Calculates valuation → ValuationFramework
6. **Workers 1-4**: Execute in parallel for efficiency
7. **Worker 5**: Synthesizes all outputs → ResearchReport
8. **Output**: JSON or Markdown formatted report

## Parallelization

- **Workers 1-4**: Execute simultaneously using `asyncio.gather()`
- **Typical Duration**: 5-15 minutes per company
- **API Calls**: ~15-20 Tavily searches + 4 Gemini inferences

## Error Handling

- Each worker catches exceptions independently
- Partial errors don't block other workers
- Synthesis worker handles missing/incomplete data
- User receives report with available data + error logs

## Extensibility

To add a new worker:

1. Create `src/workers/new_worker.py`
2. Implement async `execute(input_data)` method
3. Return Pydantic model
4. Add to orchestrator's `__init__` and `analyze()` method
5. Update synthesis prompt to incorporate new data

## API Requirements

- **Gemini 1.5 Pro**: `google_api_key` parameter
- **Tavily**: `api_key` parameter
- Both set in `.env` file

## Performance Characteristics

| Metric | Value |
|--------|-------|
| Total Analysis Time | 5-15 min |
| Worker Runtime | 1-4 min each |
| API Calls per Analysis | ~20 |
| Output File Size | 50-200 KB |
| Memory Usage | 200-500 MB |
