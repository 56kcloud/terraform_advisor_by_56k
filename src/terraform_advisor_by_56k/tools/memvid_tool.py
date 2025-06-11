"""
Custom memvid tool for CrewAI to search through AWS documentation stored in video format.
"""

import os
from typing import Type, Any, Optional
from pydantic import BaseModel, Field
from crewai.tools import tool
from memvid import MemvidRetriever


class MemvidSearchSchema(BaseModel):
    """Input schema for Memvid search."""
    query: str = Field(..., description="The search query to find relevant AWS documentation")
    top_k: int = Field(default=5, description="Number of top results to return")


# Initialize global retriever - this will be initialized when the tool is created
_global_retriever = None


def initialize_memvid_retriever(video_path: str, index_path: str):
    """Initialize the global memvid retriever."""
    global _global_retriever
    
    # Validate files exist
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"Index file not found: {index_path}")
    
    _global_retriever = MemvidRetriever(video_path, index_path)


@tool("AWS Documentation Search")
def memvid_search_tool(query: str, top_k: int = 8) -> str:
    """
    Search through AWS Well-Architected Framework documentation using memvid.
    
    This tool searches through AWS documentation that has been encoded into video format
    using memvid for efficient semantic search.
    
    Args:
        query: The search query to find relevant AWS documentation
        top_k: Number of top results to return (default: 8)
        
    Returns:
        Formatted search results as a string
    """
    global _global_retriever
    
    if _global_retriever is None:
        return "Error: Memvid retriever not initialized."
    
    try:
        # Perform semantic search
        results = _global_retriever.search(query, top_k=top_k)
        
        if not results:
            return f"No relevant AWS documentation found for query: '{query}'"
        
        # Format results
        formatted_results = []
        formatted_results.append(f"# AWS Documentation Search Results for: '{query}'\n")
        
        for i, (chunk, score) in enumerate(results, 1):
            formatted_results.append(f"## Result {i} (Relevance: {score:.3f})")
            formatted_results.append(f"{chunk}\n")
        
        return "\n".join(formatted_results)
        
    except Exception as e:
        return f"Error searching AWS documentation: {str(e)}"


# For backwards compatibility, create a class-like interface
class MemvidSearchTool:
    """Wrapper class for the memvid search tool."""
    
    def __init__(self, video_path: str, index_path: str):
        initialize_memvid_retriever(video_path, index_path)
        self.tool = memvid_search_tool 