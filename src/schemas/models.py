"""Data models for biotech research analysis"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class SourceReference(BaseModel):
    """Source reference with URL and retrieval date"""
    url: str
    title: Optional[str] = None
    retrieval_date: datetime = Field(default_factory=datetime.now)
    confidence: Optional[float] = None  # 0-1 scale


class DiseaseAnalysis(BaseModel):
    """Disease biology analysis results"""
    target_disease: str
    mechanism_of_action: str
    epidemiology: str
    unmet_medical_needs: str
    standard_of_care: str
    competitive_moas: List[str] = []
    sources: List[SourceReference] = []
    summary: Optional[str] = None


class ClinicalDataPoint(BaseModel):
    """Individual clinical trial data point"""
    metric_name: str  # e.g., "ORR", "PFS", "OS"
    value: str
    patient_population: Optional[str] = None
    trial_phase: str  # Phase 1, 2, 3
    grade_3_plus_ae: Optional[str] = None


class ClinicalData(BaseModel):
    """Drug profile and clinical trial data"""
    pipeline_stage: str  # Preclinical, Phase 1, 2, 3, Approved
    indications: List[str] = []
    clinical_data_points: List[ClinicalDataPoint] = []
    trial_design: Optional[str] = None
    patient_populations: List[str] = []
    safety_profile: Optional[str] = None
    sources: List[SourceReference] = []
    summary: Optional[str] = None


class CompetitorInfo(BaseModel):
    """Competitor pipeline information"""
    company_name: str
    drug_name: Optional[str] = None
    stage: str
    moa: Optional[str] = None
    estimated_timeline: Optional[str] = None


class CompetitiveLandscape(BaseModel):
    """Commercialization and competitive landscape"""
    addressable_market_size: Optional[str] = None
    market_growth_rate: Optional[str] = None
    standard_of_care_shifts: List[str] = []
    pricing_benchmarks: Dict[str, str] = {}
    reimbursement_status: Optional[str] = None
    competitors: List[CompetitorInfo] = []
    patent_cliffs: List[str] = []
    sources: List[SourceReference] = []
    summary: Optional[str] = None


class ValuationAssumption(BaseModel):
    """Valuation assumption"""
    name: str
    value: str
    rationale: Optional[str] = None


class ValuationFramework(BaseModel):
    """Risk-adjusted valuation analysis"""
    peak_sales_estimate: Optional[str] = None
    probability_of_success: Dict[str, float] = {}  # {stage: probability}
    risk_adjusted_npv: Optional[str] = None
    discount_rate: Optional[float] = None
    assumptions: List[ValuationAssumption] = []
    sensitivities: Dict[str, str] = {}
    sources: List[SourceReference] = []
    summary: Optional[str] = None


class Catalyst(BaseModel):
    """Upcoming catalyst"""
    event: str
    estimated_timing: str
    potential_impact: str


class InvestmentThesis(BaseModel):
    """Investment thesis and synthesis"""
    variant_perception: str  # Non-consensus view
    key_investment_highlights: List[str] = []
    key_risks: List[str] = []
    upcoming_catalysts: List[Catalyst] = []
    valuation_verdict: Optional[str] = None
    price_targets: Dict[str, str] = {}
    recommendation: Optional[str] = None


class ResearchReport(BaseModel):
    """Complete research report"""
    ticker: str
    company_name: str
    report_date: datetime = Field(default_factory=datetime.now)
    
    disease_analysis: Optional[DiseaseAnalysis] = None
    clinical_data: Optional[ClinicalData] = None
    competitive_landscape: Optional[CompetitiveLandscape] = None
    valuation_framework: Optional[ValuationFramework] = None
    investment_thesis: Optional[InvestmentThesis] = None
    
    executive_summary: Optional[str] = None
    overall_score: Optional[float] = None  # 0-10
    
    class Config:
        json_schema_extra = {
            "example": {
                "ticker": "AMGN",
                "company_name": "Amgen Inc.",
                "report_date": "2024-01-15T10:30:00",
                "disease_analysis": {
                    "target_disease": "Oncology",
                    "mechanism_of_action": "mAb targeting EGFR",
                    "epidemiology": "~500k patients annually",
                    "unmet_medical_needs": "High progression rate",
                    "standard_of_care": "Chemotherapy + mAbs",
                    "sources": []
                }
            }
        }
