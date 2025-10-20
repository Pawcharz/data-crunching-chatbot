import asyncio
import os
import json
from datetime import datetime
from typing import Optional, List, Dict, Any

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from openai import OpenAI

# ============================================================================
# CORE AI AGENT - Can be used independently for evaluation
# ============================================================================

class MongoDBAgent:
    """
    MongoDB AI Agent that uses OpenAI and MCP tools to query MongoDB.
    Can be used independently for evaluation with pydantic_evals.
    """
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        mongodb_connection_string: Optional[str] = None,
        database_name: Optional[str] = None,
        mcp_server_url: str = "http://localhost:3000/mcp",
        model: str = "gpt-4o",
        max_iterations: int = 5
    ):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.mongodb_connection_string = mongodb_connection_string or os.getenv("MDB_MCP_CONNECTION_STRING")
        self.database_name = database_name or os.getenv("MDB_MCP_DATABASE")
        self.mcp_server_url = mcp_server_url
        self.model = model
        self.max_iterations = max_iterations
        
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not provided")
        if not self.mongodb_connection_string:
            raise ValueError("MongoDB connection string not provided")
        if not self.database_name:
            raise ValueError("Database name not provided")
        
        self.openai_client = OpenAI(api_key=self.openai_api_key)
    
    @staticmethod
    def _convert_mcp_tools_to_openai_format(mcp_tools):
        """Convert MCP tool definitions to OpenAI function calling format."""
        openai_tools = []
        
        for tool in mcp_tools:
            function_def = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or f"Execute {tool.name} operation",
                    "parameters": tool.inputSchema if tool.inputSchema else {
                        "type": "object",
                        "properties": {}
                    }
                }
            }
            openai_tools.append(function_def)
        
        return openai_tools
    
    @staticmethod
    async def _execute_mcp_tool(session, tool_name, arguments):
        """Execute an MCP tool with given arguments."""
        try:
            result = await session.call_tool(tool_name, arguments)
            return result, None
        except Exception as e:
            return None, str(e)
    
    async def query(self, user_query: str) -> Dict[str, Any]:
        """
        Process a user query and return the result.
        This is the main entry point for evaluation.
        
        Args:
            user_query: Natural language query from the user
            
        Returns:
            Dictionary containing the query results with structure:
            {
                "collection": str,
                "filter": dict,
                "iterations": List[dict],
                "final_answer": str
            }
        """
        async with streamablehttp_client(self.mcp_server_url) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                
                # Connect to MongoDB
                await session.call_tool(
                    'connect', 
                    {"connectionString": self.mongodb_connection_string}
                )
                
                # Get available tools
                tools_response = await session.list_tools()
                
                # Run the agent query
                iterations = await self._run_agent_loop(
                    session, 
                    user_query, 
                    tools_response.tools
                )
                
                # Extract MongoDB query from tool calls
                query_result = self._extract_query_from_iterations(iterations)
                query_result["iterations"] = iterations
                
                return query_result
    
    async def _run_agent_loop(
        self, 
        session, 
        user_query: str, 
        mcp_tools
    ) -> List[Dict[str, Any]]:
        """Run the agent loop with tool calling."""
        
        openai_tools = self._convert_mcp_tools_to_openai_format(mcp_tools)
        
        messages = [
            {
                "role": "system",
                "content": f"""You are a MongoDB expert assistant. You have access to MongoDB MCP tools to query and analyze data.
                  The database you're working with is: {self.database_name}

                  When constructing MongoDB queries:
                  - Use proper BSON/EJSON format for special types
                  - For ObjectId: use {{"$oid": "hex_string"}}
                  - For ISODate: use {{"$date": "ISO8601_string"}}
                  - Always use the database name from the environment
                  - Check schema of the collection you are querying if you don't know the fields

                  Remember that:
                  - Check in/out events are in the events collection
                  - Today is {datetime.now().strftime("%Y-%m-%d")}

                  Analyze the user's question and use the appropriate tools to answer it."""
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
        
        iteration = 0
        results = []
        
        while iteration < self.max_iterations:
            iteration += 1
            
            iteration_data = {
                "iteration": iteration,
                "tool_calls": [],
                "final_answer": None
            }
            
            # Call OpenAI with available tools
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=openai_tools,
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            messages.append(assistant_message)
            
            # Check if the model wants to call tools
            if assistant_message.tool_calls:
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    # Execute the MCP tool
                    result, error = await self._execute_mcp_tool(session, tool_name, tool_args)
                    
                    tool_data = {
                        "name": tool_name,
                        "arguments": tool_args,
                        "success": error is None,
                        "error": error
                    }
                    
                    if result:
                        result_content = str(result.content) if hasattr(result, 'content') else str(result)
                        tool_data["result"] = result_content
                        
                        # Add tool result to messages
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result_content
                        })
                    else:
                        tool_data["result"] = f"Error: {error}"
                    
                    iteration_data["tool_calls"].append(tool_data)
            else:
                # No more tool calls, the assistant has a final answer
                iteration_data["final_answer"] = assistant_message.content
                results.append(iteration_data)
                break
            
            results.append(iteration_data)
        
        return results
    
    @staticmethod
    def _extract_query_from_iterations(iterations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract the MongoDB query (collection and filter) from the iteration results.
        Looks for 'find' or 'aggregate' tool calls.
        """
        result = {
            "collection": None,
            "filter": None,
            "final_answer": None
        }
        
        # Get final answer from last iteration
        if iterations:
            result["final_answer"] = iterations[-1].get("final_answer")
        
        # Look for MongoDB query tool calls
        for iteration in iterations:
            for tool_call in iteration.get("tool_calls", []):
                tool_name = tool_call.get("name", "")
                args = tool_call.get("arguments", {})
                
                if tool_name == "find":
                    result["collection"] = args.get("collection")
                    result["filter"] = args.get("filter", {})
                    break
                elif tool_name == "aggregate":
                    result["collection"] = args.get("collection")
                    # For aggregate, extract filter from $match stage if present
                    pipeline = args.get("pipeline", [])
                    for stage in pipeline:
                        if "$match" in stage:
                            result["filter"] = stage["$match"]
                            break
                    break
        
        return result
    
    def query_sync(self, user_query: str) -> Dict[str, Any]:
        """
        Synchronous wrapper for query() method.
        Use this for pydantic_evals integration.
        """
        return asyncio.run(self.query(user_query))

