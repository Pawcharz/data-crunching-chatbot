"""
Conversation-based dataset for MongoDB AI Agent evaluation.

This dataset captures the full interaction flow including:
- User request
- Tool calls (schema checks, queries, etc.)
- Agent's final textual response
"""

import datetime
import sys
import asyncio
import inspect
import json
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path to import MongoDBAgent
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import Evaluator, EvaluatorContext, LLMJudge
from mongodb_agent import MongoDBAgent

today = "2025-10-09"

# Conversation-based test cases
cases = [
    Case(
        name='check_ins_today_id',
        inputs=f'Show all visitors who checked in today (today is {today}) with Emirates ID 68e76c77087ed400125e9285.',
        expected_output={
            "conversation": [
                {
                    "role": "user",
                    "content": "Show all visitors who checked in today (today is {today}) with Emirates ID 68e76c77087ed400125e9285."
                },
                {
                    "role": "tool_call",
                    "tool": "collection-schema",
                    "arguments": {
                        "database": "buzzin-api-staging",
                        "collection": "events"
                    },
                },
                {
                    "role": "tool_call",
                    "tool": "find",
                    "arguments": {
                        "database": "buzzin-api-staging",
                        "collection": "events",
                        "filter": {
                            "type": "enterEvents",
                            "_id":  "ObjectId('68e76c77087ed400125e9285')",
                            "date": {
                                "$gte": "ISODate('2020-10-09')",
                                "$lt": "ISODate('2020-10-10')"
                            }
                        }
                    },
                },
                {
                    "role": "assistant",
                    "content": "The visitor with Emirates ID 68e76c77087ed400125e9285 who checked in today is SHAJAHAN ABDULR MOHAMMEDKUNHI."
                }
            ]
        },
        metadata={'difficulty': 'easy'},
    ),
    
    Case(
        name='check_ins_yesterday_eid_name',
        inputs='Provide details of visitor John Doe who checked in using Emirates ID yesterday (today is 2025-05-26).',
        expected_output={
            "conversation": [
                {
                    "role": "user",
                    "content": "Provide details of visitor John Doe who checked in using Emirates ID yesterday (today is 2025-05-26)."
                },
                {
                    "role": "tool_call",
                    "tool": "find",
                    "arguments": {
                        "database": "buzzin-api-staging",
                        "collection": "events",
                        "filter": {
                            "type": "enterEvents",
                            "guestName": "John Doe",
                            "entryType": "eid",
                            "date": {
                                "$gte": {"$date": "2025-05-25T00:00:00.000Z"},
                                "$lt": {"$date": "2025-05-26T00:00:00.000Z"}
                            }
                        }
                    },
                    "required_fields": ["type", "guestName", "entryType", "date"]
                },
                {
                    "role": "assistant",
                    "content_must_include": ["John Doe", "Emirates ID", "yesterday"],
                    "content_must_not_include": ["error"]
                }
            ]
        },
        metadata={'difficulty': 'easy'},
    ),
    
    Case(
        name='deliveries_today_amazon',
        inputs='Show all Amazon deliveries received today (today is 2025-05-26).',
        expected_output={
            "conversation": [
                {
                    "role": "user",
                    "content": "Show all Amazon deliveries received today (today is 2025-05-26)."
                },
                {
                    "role": "tool_call",
                    "tool": "find",
                    "arguments": {
                        "database": "buzzin-api-staging",
                        "collection": "events",
                        "filter": {
                            "type": "deliveryEvents",
                            "companyId": {"$oid": "6159af2a99e90e0013e5f071"},
                            "date": {
                                "$gte": {"$date": "2025-05-26T00:00:00.000Z"},
                                "$lt": {"$date": "2025-05-27T00:00:00.000Z"}
                            }
                        }
                    },
                    "required_fields": ["type", "companyId", "date"],
                    "alternatives": [
                        # Agent might search for company name first
                        {
                            "tool": "find",
                            "arguments": {
                                "database": "buzzin-api-staging",
                                "collection": "deliverycompanies",
                                "filter": {"name": {"$regex": "Amazon", "$options": "i"}}
                            }
                        }
                    ]
                },
                {
                    "role": "assistant",
                    "content_must_include": ["Amazon", "deliver", "today"],
                    "content_must_not_include": ["error"]
                }
            ]
        },
        metadata={'difficulty': 'medium'},
    ),
    
    Case(
        name='check_outs_manual_yesterday',
        inputs='List visitors who checked out manually yesterday (today is 2025-05-26).',
        expected_output={
            "conversation": [
                {
                    "role": "user",
                    "content": "List visitors who checked out manually yesterday (today is 2025-05-26)."
                },
                {
                    "role": "tool_call",
                    "tool": "find",
                    "arguments": {
                        "database": "buzzin-api-staging",
                        "collection": "events",
                        "filter": {
                            "type": "leaveEvents",
                            "leaveType": "manualExit",
                            "date": {
                                "$gte": {"$date": "2025-05-25T00:00:00.000Z"},
                                "$lt": {"$date": "2025-05-26T00:00:00.000Z"}
                            }
                        }
                    },
                    "required_fields": ["type", "leaveType", "date"]
                },
                {
                    "role": "assistant",
                    "content_must_include": ["check", "out", "manual", "yesterday"],
                    "content_must_not_include": ["error"]
                }
            ]
        },
        metadata={'difficulty': 'easy'},
    ),
    
    Case(
        name='check_ins_last_week_all_methods',
        inputs='Show me all check-ins from last week regardless of entry method (today is 2025-05-26).',
        expected_output={
            "conversation": [
                {
                    "role": "user",
                    "content": "Show me all check-ins from last week regardless of entry method (today is 2025-05-26)."
                },
                {
                    "role": "tool_call",
                    "tool": "find",
                    "arguments": {
                        "database": "buzzin-api-staging",
                        "collection": "events",
                        "filter": {
                            "type": "enterEvents",
                            "date": {
                                "$gte": {"$date": "2025-05-19T00:00:00.000Z"},
                                "$lt": {"$date": "2025-05-26T00:00:00.000Z"}
                            }
                        }
                    },
                    "required_fields": ["type", "date"],
                    "must_not_have": ["entryType"]  # Should NOT filter by entry method
                },
                {
                    "role": "assistant",
                    "content_must_include": ["check-in", "last week"],
                    "content_must_not_include": ["error"]
                }
            ]
        },
        metadata={'difficulty': 'easy'},
    ),
]

class VerboseLLMJudge(LLMJudge):
    """
    LLMJudge that prints what data it receives and its evaluation results.
    """

    async def evaluate(self, ctx: EvaluatorContext) -> float:
        """Override evaluate to add debug logging."""
        print("\n" + "=" * 80)
        print("DEBUG: DATA RECEIVED BY LLM JUDGE")
        print("=" * 80)
        
        print("\n[INPUTS]:")
        print(f"  Type: {type(ctx.inputs)}")
        print(f"  Value: {ctx.inputs}")
        
        print("\n[OUTPUT from ai_mongo_conversation]:")
        print(f"  Type: {type(ctx.output)}")
        if isinstance(ctx.output, dict):
            print(f"  Keys: {list(ctx.output.keys())}")
            print("\n  Content:")
            for key, value in ctx.output.items():
                if key == 'iterations':
                    print(f"    {key}: {len(value)} iterations")
                    for i, iteration in enumerate(value, 1):
                        print(f"      Iteration {i}:")
                        print(f"        - tool_calls: {len(iteration.get('tool_calls', []))}")
                        if iteration.get('final_answer'):
                            print(f"        - final_answer: {iteration.get('final_answer')[:100]}...")
                elif key == 'final_answer':
                    print(f"    {key}: {value}")
                else:
                    print(f"    {key}: {value}")
        else:
            print(f"  Value: {ctx.output}")
        
        print("\n[EXPECTED_OUTPUT]:")
        print(f"  Type: {type(ctx.expected_output)}")
        if isinstance(ctx.expected_output, dict):
            print(f"  Keys: {list(ctx.expected_output.keys())}")
            if 'conversation' in ctx.expected_output:
                conv = ctx.expected_output['conversation']
                print(f"  Conversation has {len(conv)} steps")
                for i, step in enumerate(conv, 1):
                    role = step.get('role', 'unknown')
                    print(f"    Step {i} - {role}:")
                    if role == 'assistant':
                        print(f"      Expected content: {step.get('content', 'N/A')}")
                    elif role == 'tool_call':
                        print(f"      Tool: {step.get('tool', 'N/A')}")
                        print(f"      Tool arguments: {step.get('arguments', 'N/A')}")
        else:
            print(f"  Value: {ctx.expected_output}")
        
        print("\n" + "=" * 80)
        print("CALLING PARENT LLMJudge.evaluate()...")
        print("=" * 80)
        
        # Call the parent evaluate method
        score = await super().evaluate(ctx)
        
        print("\n" + "=" * 80)
        print("LLM JUDGE RESULT")
        print("=" * 80)
        print(f"Score: {score}")
        print("=" * 80 + "\n")
        
        return score

# Create dataset with conversation-based evaluator
dataset = Dataset(cases=cases[:1], 
    evaluators=[VerboseLLMJudge(
        rubric="Output and Expected Output should represent the same answer, even if the tool calls don't match exactly, the final assistant answer must be simillar and explaining the same info",
        model="openai:gpt-4o-mini",
        include_input=True,
        include_expected_output=True
    )]
)


# Wrapper function for evaluation
def ai_mongo_conversation(user_query: str) -> dict:
    """
    AI function that returns full conversation including iterations.
    """
    agent = MongoDBAgent()
    result = agent.query_sync(user_query)
    return result  # Returns dict with 'iterations', 'collection', 'filter', 'final_answer'


# Example usage:
# dataset.evaluate_sync(ai_mongo_conversation)

