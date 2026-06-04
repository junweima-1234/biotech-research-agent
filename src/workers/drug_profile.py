"""Drug Profile Worker - Worker 2"""

import logging
import json
from typing import Dict, Any

from src.tools.web_search import WebSearchTool
from src.tools.llm_interface import LLMInterface
from src.schemas.models import ClinicalData

logger = logging.getLogger(__name__)


class DrugProfileWorker:
    """Worker 2: Drug Profile & Clinical Data"""
    
    def __init__(self):
        """Initialize the drug profile worker"""
        self.search_tool = WebSearchTool()
        self.llm = LLMInterface()
        self.worker_name = "Drug Profile"
    
    async def execute(self, input_data: Dict[str, Any]) -> ClinicalData:
        """
        Execute drug profile and clinical data analysis
        
        Args:
            input_data: Dict with 'ticker' and 'company_name'
            
        Returns:
            ClinicalData object
        """
        company_name = input_data.get("company_name", "")
        ticker = input_data.get("ticker", "")
        
        logger.info(f"💊 {self.worker_name} Worker: Analyzing {company_name} ({ticker})")
        
        try:
            # Step 1: Web search for clinical trial data
            search_queries = [
                f"{company_name} clinical trial results ORR PFS OS",
                f"{company_name} {ticker} pipeline stage FDA approval",
                f"{company_name} adverse events safety profile grade 3",
            ]
            
            logger.info(f"📡 Performing clinical data searches...")
            search_results = await self.search_tool.search_multiple(search_queries, max_results=5)
            
            # Step 2: Prepare context for LLM
            search_context = json.dumps(search_results, indent=2, default=str)
            
            prompt = f"""
你是一名资深临床数据分析专家。

公司：{company_name} ({ticker})

请基于以下网络搜索结果分析该公司的药物开发管线：

搜索结果：
{search_context}

请提供结构化分析，包括以下内容（返回JSON格式）：
1. pipeline_stage: 当前研发阶段（临床前、第1期、第2期、第3期、已批准等）
2. indications: 适应症列表
3. trial_design: 试验设计描述
4. patient_populations: 患者人群
5. safety_profile: 安全性概览
6. summary: 执行总结（200字以内）

返回有效的JSON格式。
"""
            
            logger.info(f"🧠 Invoking LLM for clinical analysis...")
            llm_response = await self.llm.ainvoke(prompt)
            
            # Step 3: Parse LLM response
            try:
                response_json = json.loads(llm_response)
            except json.JSONDecodeError:
                logger.warning(f"Failed to parse JSON response, using raw text")
                response_json = {
                    "pipeline_stage": "Unknown",
                    "indications": [],
                    "summary": llm_response[:500]
                }
            
            # Step 4: Create ClinicalData object
            clinical_data = ClinicalData(
                pipeline_stage=response_json.get("pipeline_stage", "Unknown"),
                indications=response_json.get("indications", []),
                trial_design=response_json.get("trial_design", ""),
                patient_populations=response_json.get("patient_populations", []),
                safety_profile=response_json.get("safety_profile", ""),
                summary=response_json.get("summary", "")
            )
            
            logger.info(f"✅ {self.worker_name} Worker: Complete")
            return clinical_data
            
        except Exception as e:
            logger.error(f"❌ {self.worker_name} Worker Error: {e}")
            return ClinicalData(
                pipeline_stage="Error",
                summary=f"Error during analysis: {str(e)}"
            )
