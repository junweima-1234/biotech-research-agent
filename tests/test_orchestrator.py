"""Tests for orchestrator"""

import pytest
from src.orchestrator import BiotechResearchOrchestrator


def test_orchestrator_initialization():
    """Test that orchestrator initializes correctly"""
    orchestrator = BiotechResearchOrchestrator()
    assert orchestrator.disease_worker is not None
    assert orchestrator.clinical_worker is not None
    assert orchestrator.commercial_worker is not None
    assert orchestrator.valuation_worker is not None
    assert orchestrator.synthesis_worker is not None


@pytest.mark.asyncio
async def test_orchestrator_analyze():
    """Test orchestrator analyze method - requires API keys"""
    pytest.skip("Requires valid API keys")
    
    orchestrator = BiotechResearchOrchestrator()
    report = await orchestrator.analyze("AMGN", "Amgen")
    
    assert report is not None
    assert report.ticker == "AMGN"
    assert report.company_name == "Amgen"
