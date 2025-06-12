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


@tool("Memvid Search")
def memvid_search_tool(query: str, top_k: int = 8) -> str:
    """
    Search through content using memvid semantic search.
    
    This tool searches through content that has been encoded into video format
    using memvid for efficient semantic search.
    
    Args:
        query: The search query to find relevant content
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
            return f"No relevant content found for query: '{query}'"
        
        # Debug: Log the structure of results to understand format
        if results and len(results) > 0:
            first_result = results[0]
            print(f"DEBUG: Results type: {type(results)}, length: {len(results)}")
            print(f"DEBUG: First result type: {type(first_result)}")
            print(f"DEBUG: First result content: {str(first_result)[:200]}...")
            if isinstance(first_result, tuple):
                print(f"DEBUG: Tuple length: {len(first_result)}")
                for idx, item in enumerate(first_result):
                    print(f"DEBUG: Tuple item {idx}: type={type(item)}, content={str(item)[:100]}...")
        
        # Format results with robust error handling
        formatted_results = []
        formatted_results.append(f"# Content Search Results for: '{query}'\n")
        
        for i, result in enumerate(results, 1):
            try:
                # Handle different result formats
                if isinstance(result, tuple):
                    if len(result) == 2:
                        chunk, score = result
                        # Ensure score is a number
                        if isinstance(score, (int, float)):
                            formatted_results.append(f"## Result {i} (Relevance: {score:.3f})")
                        else:
                            formatted_results.append(f"## Result {i} (Score: {score})")
                        formatted_results.append(f"{chunk}\n")
                    elif len(result) > 2:
                        # If more than 2 values, take first as chunk and second as score
                        chunk, score = result[0], result[1]
                        if isinstance(score, (int, float)):
                            formatted_results.append(f"## Result {i} (Relevance: {score:.3f})")
                        else:
                            formatted_results.append(f"## Result {i} (Score: {score})")
                        formatted_results.append(f"{chunk}\n")
                    elif len(result) == 1:
                        # Single item tuple
                        chunk = result[0]
                        formatted_results.append(f"## Result {i}")
                        formatted_results.append(f"{chunk}\n")
                    else:
                        # Empty tuple
                        formatted_results.append(f"## Result {i}")
                        formatted_results.append("No content available\n")
                elif isinstance(result, dict):
                    # Handle dictionary result
                    chunk = result.get('text', result.get('content', str(result)))
                    score = result.get('score', result.get('similarity', 'N/A'))
                    if isinstance(score, (int, float)):
                        formatted_results.append(f"## Result {i} (Relevance: {score:.3f})")
                    else:
                        formatted_results.append(f"## Result {i} (Score: {score})")
                    formatted_results.append(f"{chunk}\n")
                else:
                    # If not a tuple or dict, treat as just text
                    formatted_results.append(f"## Result {i}")
                    formatted_results.append(f"{result}\n")
                    
            except Exception as result_error:
                # If individual result processing fails, log and continue
                formatted_results.append(f"## Result {i} (Error processing)")
                formatted_results.append(f"Error: {str(result_error)}\n")
                print(f"DEBUG: Error processing result {i}: {result_error}")
        
        return "\n".join(formatted_results)
        
    except Exception as e:
        error_msg = f"Error searching content: {str(e)}"
        print(f"DEBUG: Search error: {error_msg}")
        return error_msg


# For backwards compatibility, create a class-like interface
class MemvidSearchTool:
    """Wrapper class for the memvid search tool."""
    
    def __init__(self, video_path: str, index_path: str):
        initialize_memvid_retriever(video_path, index_path)
        self.tool = memvid_search_tool 