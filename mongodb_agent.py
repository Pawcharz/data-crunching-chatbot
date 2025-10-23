import asyncio
import os
import json
from datetime import datetime
from typing import Optional, List, Dict, Any

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from openai import OpenAI


events_schema = """
================================================================================
Schema Analysis for Collection: events
Documents Analyzed: 10000
================================================================================

Field: __v
  Present in: 10000/10000 documents (100.0%)
  Type(s): integer
  Unique values (1):
    - 0

Field: _id
  Present in: 10000/10000 documents (100.0%)
  Type(s): ObjectId
  Unique values: 11 (> 10, treated as string)

Field: accessCardId
  Present in: 2896/10000 documents (29.0%)
  Type(s): string
  Unique values: 11 (> 10, treated as string)

Field: accessId
  Present in: 748/10000 documents (7.5%)
  Type(s): ObjectId
  Unique values: 11 (> 10, treated as string)

Field: additionalFlatsIds
  Present in: 927/10000 documents (9.3%)
  Type(s): array
  Unique values: 11 (> 10, treated as string)

Field: additionalPhoto
  Present in: 29/10000 documents (0.3%)
  Type(s): string
  Unique values: 11 (> 10, treated as string)

Field: autoSignOut
  Present in: 123/10000 documents (1.2%)
  Type(s): boolean
  Unique values (1):
    - True

Field: communityEventId
  Present in: 82/10000 documents (0.8%)
  Type(s): ObjectId
  Unique values: 11 (> 10, treated as string)

Field: communityId
  Present in: 285/10000 documents (2.9%)
  Type(s): ObjectId

Field: companyId
  Present in: 409/10000 documents (4.1%)
  Type(s): ObjectId
  CompanyID is a foreign key to the 'deliverycompanies' collection, where you can get the id of the company that is making deliveries

Field: createdAt
  Present in: 10000/10000 documents (100.0%)
  Type(s): datetime
  Unique values: 11 (> 10, treated as string)

Field: date
  Present in: 10000/10000 documents (100.0%)
  Type(s): datetime
  Unique values: 11 (> 10, treated as string)

# Deliverer related fields
DelivererName is the name of the person making the delivery, not the name of the company.

Field: delivererId
  Present in: 221/10000 documents (2.2%)
  Type(s): ObjectId
  Unique values: 11 (> 10, treated as string)

Field: delivererMobileNumber
  Present in: 457/10000 documents (4.6%)
  Type(s): string
  Unique values: 11 (> 10, treated as string)

Field: delivererName
  Present in: 757/10000 documents (7.6%)
  Type(s): string
  Unique values: 11 (> 10, treated as string)

Field: deviceId
  Present in: 10000/10000 documents (100.0%)
  Type(s): ObjectId
  Unique values: 11 (> 10, treated as string)

Field: duration
  Present in: 3301/10000 documents (33.0%)
  Type(s): integer, number
  Unique values: 11 (> 10, treated as string)

Field: emiratesData
  Present in: 3240/10000 documents (32.4%)
  Type(s): object
  Unique values: 11 (> 10, treated as string)

Field: employeesIds
  Present in: 177/10000 documents (1.8%)
  Type(s): array
  Unique values: 11 (> 10, treated as string)

Field: enterEventDate
  Present in: 6/10000 documents (0.1%)
  Type(s): datetime

Field: entryType
  Present in: 2589/10000 documents (25.9%)
  Type(s): string
  Unique values (7):
    - eid
    - hikCentralQRCode
    - liveAldarQRCode
    - manual
    - nfc
    - nfcForm
    - qrCode

Field: extraField
  Present in: 1142/10000 documents (11.4%)
  Type(s): string
  Unique values: 11 (> 10, treated as string)

Field: flatId
  Present in: 6973/10000 documents (69.7%)
  Type(s): ObjectId
  Unique values: 11 (> 10, treated as string)

Field: guardName
  Present in: 197/10000 documents (2.0%)
  Type(s): string
  Unique values: 11 (> 10, treated as string)

Field: guestId
  Present in: 2074/10000 documents (20.7%)
  Type(s): ObjectId
  Unique values: 11 (> 10, treated as string)

Field: guestMobileNumber
  Present in: 3839/10000 documents (38.4%)
  Type(s): string
  Unique values: 11 (> 10, treated as string)

Field: guestName
  Present in: 6144/10000 documents (61.4%)
  Type(s): string
  Unique values: 11 (> 10, treated as string)

Field: hikCentralReservationId
  Present in: 36/10000 documents (0.4%)
  Type(s): ObjectId
  Unique values: 11 (> 10, treated as string)

Field: hostAccessCardId
  Present in: 56/10000 documents (0.6%)
  Type(s): string
  Unique values (5):

Field: hostId
  Present in: 7675/10000 documents (76.8%)
  Type(s): ObjectId
  Unique values: 11 (> 10, treated as string)

Field: isBuzzinAppVisit
  Present in: 523/10000 documents (5.2%)
  Type(s): boolean
  Unique values (2):
    - False
    - True

Field: isDigitalCard
  Present in: 22/10000 documents (0.2%)
  Type(s): boolean
  Unique values (1):
    - True

Field: isHostMobilePhoneEnter
  Present in: 102/10000 documents (1.0%)
  Type(s): boolean
  Unique values (2):
    - False
    - True

Field: leaveType
  Present in: 3359/10000 documents (33.6%)
  Type(s): string
  Unique values (8):
    - autoSignOut
    - eidExit
    - hikCentralQRCode
    - liveAldarQRCode
    - manualExit
    - nfc
    - qrCode
    - selfCheckout

Field: left
  Present in: 4607/10000 documents (46.1%)
  Type(s): boolean
  Unique values (2):
    - False
    - True

Field: liveAldarDetails
  Present in: 33/10000 documents (0.3%)
  Type(s): object
  Unique values: 11 (> 10, treated as string)

Field: message
  Present in: 10000/10000 documents (100.0%)
  Type(s): string
  Unique values: 11 (> 10, treated as string)

Field: passId
  Present in: 291/10000 documents (2.9%)
  Type(s): ObjectId
  Unique values: 11 (> 10, treated as string)

Field: propertyId
  Present in: 10000/10000 documents (100.0%)
  Type(s): ObjectId
  Unique values (3):
    - 60adf5ddd37cb70012cecc01
    - 60ae026077dba90011862dfc
    - 60ddad6f3cf87d0014d8b720

Field: reportCaseId
  Present in: 367/10000 documents (3.7%)
  Type(s): ObjectId
  Unique values: 11 (> 10, treated as string)

Field: resolveNotes
  Present in: 180/10000 documents (1.8%)
  Type(s): string
  Unique values: 11 (> 10, treated as string)

Field: secondExtraField
  Present in: 889/10000 documents (8.9%)
  Type(s): string
  Unique values: 11 (> 10, treated as string)

Field: thirdExtraField
  Present in: 52/10000 documents (0.5%)
  Type(s): string
  Unique values: 11 (> 10, treated as string)

Field: type
  Present in: 10000/10000 documents (100.0%)
  Type(s): string
  Unique values: 11 (> 10, treated as string)

Field: updatedAt
  Present in: 10000/10000 documents (100.0%)
  Type(s): datetime
  Unique values: 11 (> 10, treated as string)

Field: validationDate
  Present in: 16/10000 documents (0.2%)
  Type(s): datetime

Field: validationDuration
  Present in: 6/10000 documents (0.1%)
  Type(s): integer

Field: validationPropertyAgentId
  Present in: 16/10000 documents (0.2%)
  Type(s): ObjectId, null
  Null values: 2

Field: validationWaitDuration
  Present in: 16/10000 documents (0.2%)
  Type(s): integer

Field: visitorAccessCardId
  Present in: 56/10000 documents (0.6%)
  Type(s): string

Field: visitorId
  Present in: 56/10000 documents (0.6%)
  Type(s): ObjectId

"""

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
        model: str = "gpt-4.1",
        max_iterations: int = 5
    ):
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.mongodb_connection_string = mongodb_connection_string or os.getenv("MDB_MCP_CONNECTION_STRING")
        self.database_name = database_name or os.getenv("MDB_MCP_DATABASE")
        self.mcp_server_url = mcp_server_url
        self.model = model
        self.max_iterations = max_iterations

        # self.mongo_client = MongoClient(self.mongodb_connection_string)
        # db = self.mongo_client[self.database_name]
        # self.unique_countries = db.users.distinct("country")
        
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
    
    async def query(self, user_query: Dict[str, Any]) -> Dict[str, Any]:
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
        print('user_query', user_query)
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
        user_query: Dict[str, Any], 
        mcp_tools
    ) -> List[Dict[str, Any]]:
        """Run the agent loop with tool calling."""
        
        openai_tools = self._convert_mcp_tools_to_openai_format(mcp_tools)

        # print('\n\nuser_query: \n', user_query)
        current_date = user_query.get("today_date")
        querry_text = user_query.get("text")
        
        messages = [
            {
                "role": "system",
                "content": f"""You are a MongoDB expert assistant. You have access to MongoDB MCP tools to query and analyze data.
                  The database you're working with is: {self.database_name}
                  The schema of the collection you are querying is: \n\n {events_schema} \n\n

                  When constructing MongoDB queries:
                  - Use proper BSON/EJSON format for special types
                  - Always use the database name from the environment
                  - Check schema of the collection you are querying if you don't know the fields
                  - whenever you need to use a field describing some type, first check unique values of that field

                  Remember that:
                  - you need to check the schema of the collection before performing any find or aggregate operation
                  - whenever you need to use any field that is not name or date, first check unique values of that field. This should generally apply to all information that could potentially be described as enums
                  - Check in/out events are in the events collection

                  The current date is {current_date}

                  Analyze the user's question and use the appropriate tools to answer it."""
            },
            {
                "role": "user",
                "content": querry_text
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
    
    def query_sync(self, user_query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synchronous wrapper for query() method.
        Use this for pydantic_evals integration.
        """
        return asyncio.run(self.query(user_query))

