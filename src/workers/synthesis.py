"""Synthesis Worker - Worker 5"""

import logging
import json
from typing import Dict, Any

from src.tools.llm_interface import LLMInterface
from src.schemas.models import (
    InvestmentThesis,
    ResearchReport,
    DiseaseAnalysis,
    ClinicalData,
    CompetitiveLandscape,
    ValuationFramework
)

logger = logging.getLogger(__name__)


class SynthesisWorker:
    """Worker 5: Investment Thesis Synthesis"""
    
    def __init__(self):
        """Initialize the synthesis worker"""
        self.llm = LLMInterface()
        self.worker_name = "Synthesis"
    
    async def execute(self, input_data: Dict[str, Any]) -> ResearchReport:
        """
        Execute synthesis and create final investment report
        
        Args:
            input_data: Dict with all worker outputs and company info
            
        Returns:
            ResearchReport object
        """
        company_name = input_data.get("company_name", "")
        ticker = input_data.get("ticker", "")
        
        logger.info(f"📊 {self.worker_name} Worker: Synthesizing report for {company_name} ({ticker})")
        
        try:
            # Extract worker outputs
            disease = input_data.get("disease", DiseaseAnalysis(target_disease=""))
            clinical = input_data.get("clinical", ClinicalData())
            commercial = input_data.get("commercial", CompetitiveLandscape())
            valuation = input_data.get("valuation", ValuationFramework())
            
            # Prepare comprehensive context
            context = {
                "disease": disease.dict() if hasattr(disease, 'dict') else disease,
                "clinical": clinical.dict() if hasattr(clinical, 'dict') else clinical,
                "commercial": commercial.dict() if hasattr(commercial, 'dict') else commercial,
                "valuation": valuation.dict() if hasattr(valuation, 'dict') else valuation,
            }
            context_str = json.dumps(context, indent=2, default=str)
            
            prompt = f"""
你是一名资深的买方研究分析师。

公司：{company_name} ({ticker})

请基于以下完整的研究分析结果，合成一份机构级的投资研究报告：

分析结果：
{context_str}

请生成结构化的投资论文，包括以下内容（返回JSON格式）：
1. variant_perception: 非共识观点（你对该公司的独特见解，200字）
2. key_investment_highlights: 关键投资亮点（列表，3-5个要点）
3. key_risks: 关键风险（列表，3-5个风险）
4. upcoming_catalysts: 即将到来的催化剂（列表）
   格式：[{{"event": "Phase 3 readout", "estimated_timing": "Q3 2024", "potential_impact": "Critical for value"}}]
5. valuation_verdict: 估值判断（高估/合理/低估及原因）
6. price_targets: 目标价格（字典，12个月/24个月）
   格式：{{"12_months": "$XX", "24_months": "$XX"}}
7. recommendation: 推荐（买入/持有/卖出）
8. executive_summary: 执行总结（300字）

返回有效的JSON格式。
"""
            
            logger.info(f"🧠 Invoking LLM for synthesis...")
            llm_response = await self.llm.ainvoke(prompt)
            
            # Parse LLM response
            try:
                response_json = json.loads(llm_response)
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse JSON response, using raw text")
                response_json = {
                    "variant_perception": llm_response[:300],
                    "key_investment_highlights": [],
                    "key_risks": [],
                    "recommendation": "Hold",
                    "executive_summary": llm_response[:500]
                }
            
            # Create InvestmentThesis
            investment_thesis = InvestmentThesis(
                variant_perception=response_json.get("variant_perception", ""),
                key_investment_highlights=response_json.get("key_investment_highlights", []),
                key_risks=response_json.get("key_risks", []),
                valuation_verdict=response_json.get("valuation_verdict", ""),
                price_targets=response_json.get("price_targets", {}),
                recommendation=response_json.get("recommendation", "Hold")
            )
            
            # Create final ResearchReport
            report = ResearchReport(
                ticker=ticker,
                company_name=company_name,
                disease_analysis=disease,
                clinical_data=clinical,
                competitive_landscape=commercial,
                valuation_framework=valuation,
                investment_thesis=investment_thesis,
                executive_summary=response_json.get("executive_summary", ""),
                overall_score=None
            )
            
            logger.info(f"✅ {self.worker_name} Worker: Complete")
            return report
            
        except Exception as e:
            logger.error(f"❌ {self.worker_name} Worker Error: {e}")
            return ResearchReport(
                ticker=ticker,
                company_name=company_name,
                executive_summary=f"Error during synthesis: {str(e)}"
            )
