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


class DatasetBuilder:
    def __init__(self, today: str):
        self.today = datetime.datetime.strptime(today, "%Y-%m-%d")

        today_str = self.today.strftime("%Y-%m-%d (%A)")

        today_start = datetime.datetime.strptime(today, "%Y-%m-%d") # 00:00:00
        today_end = datetime.datetime.strptime(today, "%Y-%m-%d") + datetime.timedelta(days=1)
        yesterday_start = today_start - datetime.timedelta(days=1)
        yesterday_end = today_end - datetime.timedelta(days=1)
        week_start = today_start - datetime.timedelta(days=today_start.weekday())
        week_end = week_start + datetime.timedelta(days=7)
        
        self.cases = [
            Case(
                name='check_ins_today_id',
                inputs={
                  "text": f'Show all visitors who checked in today with Emirates ID 68e76c77087ed400125e9285.',
                  "today_date": '2025-10-09'
                },
                expected_output={
                    "conversation": [
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
                                    "_id":  "68e76c77087ed400125e9285",
                                    "date": {
                                        "$gte": "<today - start of day>",
                                        "$lt": "<today - end of day>"
                                    }
                                }
                            },
                            "obtained_data": """{
                                "_id": {
                                  "$oid": "68e76c77087ed400125e9285"
                                },
                                "left": true,
                                "additionalFlatsIds": [],
                                "type": "enterEvents",
                                "flatId": {
                                  "$oid": "648afc637459670012dc4e1a"
                                },
                                "deviceId": {
                                  "$oid": "60f003b02485680011207c7d"
                                },
                                "propertyId": {
                                  "$oid": "60ae026077dba90011862dfc"
                                },
                                "guestName": "SHAJAHAN ABDULR MOHAMMEDKUNHI",
                                "guestMobileNumber": "+971505117487",
                                "entryType": "eid",
                                "emiratesData": {
                                  "mrzData": {
                                    "issuing_country": "ARE",
                                    "dob_readable": "27.06.1994",
                                    "dob_raw": "940627",
                                    "raw_result": "ILARE1441202103784199493910329<<<<<<9406270M2703165IND<<<<<<<<<<<4<<<<<<MOHAMMEDKUNHI<<SHAJAHAN<ABDULR<<<<<<",
                                    "optionals": "784199493910329",
                                    "expiration_date_raw": "270316",
                                    "expiration_date_readable": "16.03.2027",
                                    "nationality": "IND",
                                    "document_number": "144120210",
                                    "sex": "M",
                                    "given_names_readable": "SHAJAHAN ABDULR",
                                    "surname": "MOHAMMEDKUNHI",
                                    "document_type_readable": "IL",
                                    "document_type_raw": "IL"
                                  }
                                },
                                "extraField": "567",
                                "secondExtraField": "Accounts",
                                "thirdExtraField": "007",
                                "isHostMobilePhoneEnter": false,
                                "message": "SHAJAHAN ABDULR MOHAMMEDKUNHI entered the unit HR",
                                "date": {
                                  "$date": "2025-10-09T08:04:07.699Z"
                                },
                                "createdAt": {
                                  "$date": "2025-10-09T08:04:07.700Z"
                                },
                                "updatedAt": {
                                  "$date": "2025-10-10T04:06:13.280Z"
                                },
                                "__v": 0
                              }"""
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
                inputs={
                  "text": f'Provide details of visitor SHAJAHAN ABDULR MOHAMMEDKUNHI who checked in using Emirates ID yesterday.',
                  "today_date": '2025-09-30'
                },
                expected_output={
                    "conversation": [
                        {
                            "role": "tool_call",
                            "tool": "find",
                            "arguments": {
                                "database": "buzzin-api-staging",
                                "collection": "events",
                                "filter": {
                                    "type": "enterEvents",
                                    "guestName": "SHAJAHAN ABDULR MOHAMMEDKUNHI",
                                    "entryType": "eid",
                                    "date": {
                                        "$gte": "<yesterday - start of day>",
                                        "$lt": "<yesterday - end of day>"
                                    }
                                }
                            },
                            "obtained_data": """{
                                "_id": {
                                  "$oid": "68da3c285a0387001217efeb"
                                },
                                "left": true,
                                "additionalFlatsIds": [],
                                "type": "enterEvents",
                                "flatId": {
                                  "$oid": "648afc637459670012dc4e16"
                                },
                                "deviceId": {
                                  "$oid": "68a45ec154ddb0bd2803a428"
                                },
                                "propertyId": {
                                  "$oid": "60ae026077dba90011862dfc"
                                },
                                "guestId": {
                                  "$oid": "66e3d7c6662029c070e947e3"
                                },
                                "guestName": "SHAJAHAN ABDULR MOHAMMEDKUNHI",
                                "guestMobileNumber": "+971505117487",
                                "entryType": "eid",
                                "emiratesData": {
                                  "mrzData": {
                                    "issuing_country": "ARE",
                                    "dob_readable": "27.06.1994",
                                    "dob_raw": "940627",
                                    "raw_result": "ILARE1441202103784199493910329<<<<<<9406270M2703165IND<<<<<<<<<<4<<<<<<<MOHAMMEDKUNHI<<SHAJAHAN<ABDULR<<<<<<",
                                    "optionals": "784199493910329 4",
                                    "expiration_date_raw": "270316",
                                    "expiration_date_readable": "16.03.2027",
                                    "nationality": "IND",
                                    "document_number": "144120210",
                                    "sex": "M",
                                    "given_names_readable": "SHAJAHAN ABDULR",
                                    "surname": "MOHAMMEDKUNHI",
                                    "document_type_readable": "IL",
                                    "document_type_raw": "IL"
                                  }
                                },
                                "extraField": "567",
                                "secondExtraField": "Accounts",
                                "thirdExtraField": "007",
                                "isHostMobilePhoneEnter": false,
                                "message": "SHAJAHAN ABDULR MOHAMMEDKUNHI entered the unit F&B",
                                "date": {
                                  "$date": "2025-09-29T07:58:32.622Z"
                                },
                                "createdAt": {
                                  "$date": "2025-09-29T07:58:32.625Z"
                                },
                                "updatedAt": {
                                  "$date": "2025-09-29T08:21:07.863Z"
                                },
                                "__v": 0
                              }"""
                        },
                        {
                            "role": "assistant",
                            "content": "SHAJAHAN ABDULR MOHAMMEDKUNHI entered the unit F&B on 2025-09-29 using Emirates ID yesterday He was born on 27.06.1994"
                        }
                    ]
                },
                metadata={'difficulty': 'easy'},
            ),
            
            Case(
                name='deliveries_today_amazon',
                inputs={
                  "text": f'Show all Amazon deliveries received today.',
                  "today_date": '2025-01-27'
                },
                expected_output={
                    "conversation": [
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
                                        "$gte": "<today - start of day>",
                                        "$lt": "<today - end of day>"
                                    }
                                }
                            },
                            "obtained_data": """{
                                "_id": {
                                  "$oid": "679768b2e4a7880011092fc9"
                                },
                                "left": true,
                                "additionalFlatsIds": [],
                                "type": "deliveryEvents",
                                "propertyId": {
                                  "$oid": "60ae026077dba90011862dfc"
                                },
                                "flatId": {
                                  "$oid": "64098199c9d51b00129c9474"
                                },
                                "hostId": {
                                  "$oid": "66f526173eba5a0012a23b42"
                                },
                                "companyId": {
                                  "$oid": "6159af2a99e90e0013e5f071"
                                },
                                "delivererId": {
                                  "$oid": "66f526173eba5a0012a23b42"
                                },
                                "deviceId": {
                                  "$oid": "60f003b02485680011207c7d"
                                },
                                "delivererName": "SURINDER RAM",
                                "delivererMobileNumber": "+971505117487",
                                "emiratesData": {
                                  "mrzData": {
                                    "raw_result": "IDKWTK170481362296031802642<<<9603183M2002178IND14196366<<<5RAM<<SURINDER<<<<<<<<<<<<<<<<<",
                                    "optionals": "296031802642 14196366",
                                    "est_issuing_date_readable": "Unknown",
                                    "expiration_date_raw": "200217",
                                    "est_issuing_date_raw": "",
                                    "issuing_country": "KWT",
                                    "dob_readable": "18.03.1996",
                                    "dob_raw": "960318",
                                    "expiration_date_readable": "17.02.2020",
                                    "nationality": "IND",
                                    "document_number": "K17048136",
                                    "sex": "M",
                                    "surname": "RAM",
                                    "given_names_readable": "SURINDER",
                                    "document_type_readable": "ID",
                                    "document_type_raw": "ID"
                                  }
                                },
                                "extraField": "123",
                                "secondExtraField": "Visitor",
                                "message": "New delivery from Amazon delivered by SURINDER RAM to unit 27",
                                "date": {
                                  "$date": "2025-01-27T11:06:26.858Z"
                                },
                                "createdAt": {
                                  "$date": "2025-01-27T11:06:26.859Z"
                                },
                                "updatedAt": {
                                  "$date": "2025-01-27T12:05:50.560Z"
                                },
                                "__v": 0
                              }"""
                        },
                        {
                            "role": "assistant",
                        }
                    ]
                },
                metadata={'difficulty': 'medium'},
            ),
            
            Case(
                name='check_outs_manual_yesterday',
                inputs={
                  "text": f'List visitors who checked out manually yesterday.',
                  "today_date": '2025-09-30'
                },
                expected_output={
                    "conversation": [
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
                                        "$gte": "<yesterday - start of day>",
                                        "$lt": "<yesterday - end of day>"
                                    }
                                }
                            },
                            "obtained_data": """{
                                "_id": {
                                  "$oid": "68da3b345a0387001217efd0"
                                },
                                "type": "leaveEvents",
                                "guestName": "Innocent ",
                                "thirdExtraField": "788",
                                "propertyId": {
                                  "$oid": "60ae026077dba90011862dfc"
                                },
                                "flatId": {
                                  "$oid": "641418c04edebf0012d5db93"
                                },
                                "hostId": {
                                  "$oid": "67875b78450a3200118e7b43"
                                },
                                "deviceId": {
                                  "$oid": "68a45ec154ddb0bd2803a428"
                                },
                                "leaveType": "manualExit",
                                "duration": 72652,
                                "message": "Innocent  left the unit 667",
                                "date": {
                                  "$date": "2025-09-29T07:54:28.415Z"
                                },
                                "createdAt": {
                                  "$date": "2025-09-29T07:54:28.416Z"
                                },
                                "updatedAt": {
                                  "$date": "2025-09-29T07:54:28.416Z"
                                },
                                "__v": 0
                              }"""
                        },
                        {
                            "role": "assistant",
                        }
                    ]
                },
                metadata={'difficulty': 'easy'},
            ),
            
            Case(
                name='check_ins_last_week_all_methods',
                inputs={
                  "text": f'Show me all check-ins from previous week regardless of entry method.',
                  "today_date": '2025-10-14'
                },
                expected_output={
                    "conversation": [
                        {
                            "role": "tool_call",
                            "tool": "find",
                            "arguments": {
                                "database": "buzzin-api-staging",
                                "collection": "events",
                                "filter": {
                                    "type": "enterEvents",
                                    "date": {
                                        "$gte": "<week - start of week (monday)>",
                                        "$lt": "<week - end of week (sunday)>"
                                    }
                                }
                            },
                            "obtained_data": """
                            - SHAJAHAN ABDULR MOHAMMEDKUNHI entered the unit HR on 2025-10-09
                            - SHAJAHAN ABDULR MOHAMMEDKUNHI entered the unit 667 on 2025-10-09
                            - Joji entered the unit 667 on 2025-10-09

                            (plus full data for each event)
                            """
                        },
                        {
                            "role": "assistant",
                            "content": """
                            - SHAJAHAN ABDULR MOHAMMEDKUNHI entered the unit HR on 2025-10-09
                            - SHAJAHAN ABDULR MOHAMMEDKUNHI entered the unit 667 on 2025-10-09
                            - Joji entered the unit 667 on 2025-10-09
                            """
                        }
                    ]
                },
                metadata={'difficulty': 'easy'},
            ),
        ]
    
    def build(self) -> Dataset:
        return Dataset(cases=self.cases, evaluators=[
            LLMJudge(
                rubric="Output and Expected Output's find query and filter should be equivalent and include the same values. Formating of dates, can be different, but only dates",
                model="openai:gpt-4o",
                include_input=True,
            ),
            LLMJudge(
                rubric="The obtained_data of the find query should be equivalent to the expected_output' obtained_data of the find query. Both should return the same documents, no less, no more. Only thing that can differ is formating. The format of the dates can be different, but only dates",
                model="openai:gpt-4o",
                include_input=True,
            )
        ])


# Create dataset with conversation-based evaluator
dataset = DatasetBuilder(today=today).build()

# Wrapper function for evaluation
def ai_mongo_conversation(user_query: Dict[str, Any]) -> dict:
    """
    AI function that returns full conversation including iterations.
    """

    # Pass date from input (dict) to agent, remove from query
    # Add more queries to the agent
    # Add expected output of find mongodb queries - separate llm judge

    agent = MongoDBAgent()
    result = agent.query_sync(user_query)

    # print('user_query', user_query)
    # print('\n\nresult: \n', result)
    
    return result


# Example usage:
# dataset.evaluate_sync(ai_mongo_conversation)

