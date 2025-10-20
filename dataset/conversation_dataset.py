"""
Conversation-based dataset for MongoDB AI Agent evaluation.

This dataset captures the full interaction flow including:
- User request
- Tool calls (schema checks, queries, etc.)
- Agent's final textual response
"""

import datetime
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path to import MongoDBAgent
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import Evaluator, EvaluatorContext
from mongodb_agent import MongoDBAgent

today = "2025-05-26"

# Conversation-based test cases
cases = [
    Case(
        name='check_ins_today_qr_code',
        inputs='Show all visitors who checked in using QR code today (today is 2025-05-26).',
        expected_output={
            "conversation": [
                {
                    "role": "user",
                    "content": "Show all visitors who checked in using QR code today (today is 2025-05-26)."
                },
                {
                    "role": "tool_call",
                    "tool": "collection-schema",
                    "arguments": {
                        "database": "buzzin-api-staging",
                        "collection": "events"
                    },
                    "optional": True  # Agent may or may not call this
                },
                {
                    "role": "tool_call",
                    "tool": "find",
                    "arguments": {
                        "database": "buzzin-api-staging",
                        "collection": "events",
                        "filter": {
                            "type": "enterEvents",
                            "entryType": "qrCode",
                            "date": {
                                "$gte": {"$date": "2025-05-26T00:00:00.000Z"},
                                "$lt": {"$date": "2025-05-27T00:00:00.000Z"}
                            }
                        }
                    },
                    "required_fields": ["type", "entryType", "date"]
                },
                {
                    "role": "assistant",
                    "content_must_include": ["visitor", "QR code", "check", "today"],
                    "content_must_not_include": ["error", "failed"]
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


class ConversationEvaluator(Evaluator[dict, dict]):
    """
    Evaluator that checks conversation flow including:
    - Tool calls made
    - Filter structure in tool calls
    - Agent's textual response quality
    """
    
    def _check_tool_call(self, expected_tool, actual_iterations):
        """Check if expected tool was called with correct arguments."""
        if expected_tool.get("optional", False):
            return 1.0  # Optional tools don't affect score
        
        required_fields = expected_tool.get("required_fields", [])
        tool_name = expected_tool.get("tool")
        expected_filter = expected_tool.get("arguments", {}).get("filter", {})
        
        # Search through all iterations for matching tool call
        for iteration in actual_iterations:
            for tool_call in iteration.get("tool_calls", []):
                if tool_call.get("name") == tool_name:
                    actual_args = tool_call.get("arguments", {})
                    actual_filter = actual_args.get("filter", {})
                    
                    # Check required fields are present
                    score = 0
                    for field in required_fields:
                        if field in actual_filter:
                            # Check if value matches or is reasonable
                            if field in expected_filter:
                                if self._compare_values(expected_filter[field], actual_filter[field]):
                                    score += 1
                            else:
                                score += 1  # Field present, no specific value required
                    
                    return score / len(required_fields) if required_fields else 1.0
        
        return 0.0  # Tool not called
    
    def _compare_values(self, expected, actual):
        """Compare values with some flexibility."""
        if expected == actual:
            return True
        
        # For dates, just check structure is correct
        if isinstance(expected, dict) and "$date" in expected:
            return isinstance(actual, dict) and "$date" in actual
        
        # For ObjectIds
        if isinstance(expected, dict) and "$oid" in expected:
            return isinstance(actual, dict) and "$oid" in actual
        
        # For nested dicts
        if isinstance(expected, dict) and isinstance(actual, dict):
            return all(k in actual for k in expected.keys())
        
        return False
    
    def _check_assistant_response(self, expected_response, actual_iterations):
        """Check if agent's final response meets criteria."""
        # Get final answer from last iteration
        final_answer = None
        for iteration in reversed(actual_iterations):
            if iteration.get("final_answer"):
                final_answer = iteration["final_answer"]
                break
        
        if not final_answer:
            return 0.0
        
        final_answer_lower = final_answer.lower()
        
        # Check must include
        must_include = expected_response.get("content_must_include", [])
        include_score = sum(1 for phrase in must_include if phrase.lower() in final_answer_lower)
        include_score = include_score / len(must_include) if must_include else 1.0
        
        # Check must not include
        must_not_include = expected_response.get("content_must_not_include", [])
        exclude_score = sum(1 for phrase in must_not_include if phrase.lower() not in final_answer_lower)
        exclude_score = exclude_score / len(must_not_include) if must_not_include else 1.0
        
        return (include_score + exclude_score) / 2
    
    def evaluate(self, ctx: EvaluatorContext[dict, dict]) -> float:
        """
        Evaluate the conversation flow.
        ctx.output should contain the iterations from the agent.
        ctx.expected_output contains the expected conversation structure.
        """
        if not ctx.output or not ctx.expected_output:
            return 0.0
        
        actual_iterations = ctx.output.get("iterations", [])
        expected_conversation = ctx.expected_output.get("conversation", [])

        print('actual_iterations: ', actual_iterations)
        print('expected_conversation: ', expected_conversation)
        
        if not actual_iterations or not expected_conversation:
            return 0.0
        
        scores = []
        
        # Evaluate tool calls
        for turn in expected_conversation:
            if turn.get("role") == "tool_call":
                score = self._check_tool_call(turn, actual_iterations)
                scores.append(score)
            elif turn.get("role") == "assistant":
                score = self._check_assistant_response(turn, actual_iterations)
                scores.append(score)
        
        return sum(scores) / len(scores) if scores else 0.0


# Create dataset with conversation-based evaluator
dataset = Dataset(cases=cases[:1], evaluators=[ConversationEvaluator()])


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

