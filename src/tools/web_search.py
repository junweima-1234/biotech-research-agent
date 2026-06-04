"""Web search tool using Tavily API"""

import asyncio
import logging
from typing import List, Dict, Any
from tavily import TavilyClient

from src.tools.config import Config

logger = logging.getLogger(__name__)


class WebSearchTool:
    """Web search tool using Tavily API"""
    
    def __init__(self):
        """Initialize Tavily client"""
        self.client = TavilyClient(api_key=Config.TAVILY_API_KEY)
    
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Perform a web search using Tavily
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with URLs and content
        """
        try:
            logger.info(f"🔍 Searching: {query}")
            
            response = self.client.search(
                query=query,
                max_results=max_results,
                include_answer=True,
                topic="general"
            )
            
            results = []
            if "results" in response:
                for result in response["results"][:max_results]:
                    results.append({
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "content": result.get("content", ""),
                        "source": result.get("source", ""),
                    })
            
            logger.info(f"✅ Found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"❌ Search error: {e}")
            return []
    
    async def search_async(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Async version of search
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            List of search results
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, self.search, query, max_results
        )
    
    async def search_multiple(self, queries: List[str], max_results: int = 5) -> Dict[str, List[Dict[str, Any]]]:
        """
        Search multiple queries in parallel
        
        Args:
            queries: List of search queries
            max_results: Maximum results per query
            
        Returns:
            Dictionary mapping queries to results
        """
        logger.info(f"🔍 Searching {len(queries)} queries in parallel...")
        
        tasks = [
            self.search_async(query, max_results) 
            for query in queries
        ]
        
        results = await asyncio.gather(*tasks)
        
        return {
            query: result 
            for query, result in zip(queries, results)
        }
