import datetime
import sys
from pathlib import Path

# Add parent directory to path to import MongoDBAgent
sys.path.insert(0, str(Path(__file__).parent.parent))

from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import Evaluator, EvaluatorContext
from mongodb_agent import MongoDBAgent

today = "2025-10-09"

cases = [
    Case(
        name='check_ins_today_id',
        inputs='Show all visitors who checked in today (today is {today}) with Emirates ID 68e76c77087ed400125e9285.',
        expected_output={
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
        metadata={'difficulty': 'easy'},
    ),
    Case(
        name='check_outs_date_id',
        inputs='List all check-outs for Emirates ID 60ae057577dba90011862e0a on 26/05/2021.',
        expected_output={
          "collection": "events",
          "filter": {
            "type": "leaveEvents",
            "_id": {"$oid": "60ae057577dba90011862e0a"},
            "date": {
              "$gte": "ISODate('2025-05-26')",
              "$lt": "ISODate('2025-05-27')"
            }
          }
        },
        metadata={'difficulty': 'easy'},
    ),
    Case(
        name='check_ins_yesterday_eid_unit_name',
        inputs='Provide details of visitor John Doe who checked in using Emirates ID at unit 123 yesterday (today is {today})',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "enterEvents",
                "guestName": "John Doe",
                "entryType": "eid",
                "date": {
                    "$gte": {"$date": "yesterday_start"},
                    "$lt": {"$date": "yesterday_end"}
                }
            }
        },
        metadata={'difficulty': 'easy'},
    ),
    Case( # Report is more complex and requires multiple queries
        name='check_ins_last_month_eid_unit_report',
        inputs='Give a report of check-ins for Emirates ID 784512369012347 at unit 456 last month (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "enterEvents",
                "entryType": "eid",
                "emiratesData.mrzData.document_number": "784512369012347",
                "date": {
                    "$gte": {"$date": "last_month_start"},
                    "$lt": {"$date": "last_month_end"}
                }
            }
        },
        metadata={'difficulty': 'easy'},
    ),
    Case(
        name='check_ins_today_qr_code_all_visitors',
        inputs='Show all visitors who checked in using QR code today (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "enterEvents",
                "entryType": "qrCode",
                "date": {
                    "$gte": {"$date": "today_start"},
                    "$lt": {"$date": "today_end"}
                }
            }
        },
        metadata={'difficulty': 'easy'},
    ),
    Case(
        name='check_outs_yesterday_qr_code_all_visitors',
        inputs='List all visitors who checked out using QR code yesterday (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "leaveEvents",
                "leaveType": "qrCode",
                "date": {
                    "$gte": {"$date": "yesterday_start"},
                    "$lt": {"$date": "yesterday_end"}
                }
            }
        },
        metadata={'difficulty': 'easy'},
    ),
    Case(
        name='check_ins_yesterday_qr_code_name_unit',
        inputs='Provide details of visitor Jane Smith who checked in with QR code at unit 123 yesterday (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "enterEvents",
                "guestName": "Jane Smith",
                "entryType": "qrCode",
                "date": {
                    "$gte": {"$date": "yesterday_start"},
                    "$lt": {"$date": "yesterday_end"}
                }
            }
        },
        metadata={'difficulty': 'easy'},
    ),
    Case(
        name='check_ins_this_week_qr_code_all_employees',
        inputs='Which employees checked in using QR code this week? (today is {today})',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "enterEvents",
                "entryType": "qrCode",
                "date": {
                    "$gte": {"$date": "week_start"},
                    "$lt": {"$date": "today_end"}
                }
            }
        },
        metadata={'difficulty': 'easy'},
    ),
    Case(
        name='check_ins_last_month_qr_code_unit_report',
        inputs='Give a report of QR code check-ins at unit 456 last month (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "enterEvents",
                "entryType": "qrCode",
                "date": {
                    "$gte": {"$date": "last_month_start"},
                    "$lt": {"$date": "last_month_end"}
                }
            }
        },
        metadata={'difficulty': 'easy'},
    ),
    Case(
        name='check_ins_manual_today_all_users',
        inputs='Show all users who checked in manually today (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "enterEvents",
                "entryType": "manual",
                "date": {
                    "$gte": {"$date": "today_start"},
                    "$lt": {"$date": "today_end"}
                }
            }
        },
        metadata={'difficulty': 'easy'},
    ),
    Case(
        name='check_outs_manual_yesterday_all_visitors',
        inputs='List visitors who checked out manually yesterday (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "leaveEvents",
                "leaveType": "manualExit",
                "date": {
                    "$gte": {"$date": "yesterday_start"},
                    "$lt": {"$date": "yesterday_end"}
                }
            }
        },
        metadata={'difficulty': 'easy'},
    ),
    Case(
        name='check_ins_outs_manual_date_name',
        inputs='Provide details of visitor John Doe who manually checked in and out on 05/10/2025.',
        expected_output={
            "collection": "events",
            "filter": {
                "$or": [
                    {
                        "type": "enterEvents",
                        "entryType": "manual",
                        "guestName": "John Doe",
                        "date": {
                            "$gte": {"$date": "2025-10-05T00:00:00.000Z"},
                            "$lt": {"$date": "2025-10-06T00:00:00.000Z"}
                        }
                    },
                    {
                        "type": "leaveEvents",
                        "leaveType": "manualExit",
                        "guestName": "John Doe",
                        "date": {
                            "$gte": {"$date": "2025-10-05T00:00:00.000Z"},
                            "$lt": {"$date": "2025-10-06T00:00:00.000Z"}
                        }
                    }
                ]
            }
        },
        metadata={'difficulty': 'easy'},
    ),
    Case(
        name='check_ins_this_week_manual_all_employees',
        inputs='Which employees checked in manually this week? (today is {today})',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "enterEvents",
                "entryType": "manual",
                "date": {
                    "$gte": {"$date": "week_start"},
                    "$lt": {"$date": "today_end"}
                }
            }
        },
        metadata={'difficulty': 'easy'},
    ),
    Case(
        name='check_outs_last_month_manual_unit',
        inputs='Show all manual check-outs for unit 123 last month (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "leaveEvents",
                "leaveType": "manualExit",
                "date": {
                    "$gte": {"$date": "last_month_start"},
                    "$lt": {"$date": "last_month_end"}
                }
            }
        },
        metadata={'difficulty': 'easy'},
    ),
    # Deliveries by delivery companies
    # Amazon ObjectId: 6159af2a99e90e0013e5f071
    # Noon ObjectId: 64e2f3be6e499a001219b0fa
    Case(
        name='deliveries_today_amazon_unit',
        inputs='Show all Amazon deliveries received at unit 123 today (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "deliveryEvents",
                "companyId": {"$oid": "6159af2a99e90e0013e5f071"},
                "date": {
                    "$gte": {"$date": "today_start"},
                    "$lt": {"$date": "today_end"}
                }
            }
        },
        metadata={'difficulty': 'easy'},
    ),
    Case(
        name='deliveries_date_noon_unit',
        inputs='List all Noon deliveries made to unit 456 on 05/10/2025.',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "deliveryEvents",
                "companyId": {"$oid": "64e2f3be6e499a001219b0fa"},
                "date": {
                    "$gte": {"$date": "2025-10-05T00:00:00.000Z"},
                    "$lt": {"$date": "2025-10-06T00:00:00.000Z"}
                }
            }
        },
        metadata={'difficulty': 'easy'},
    ),
    Case(
        name='deliveries_last_week_amazon_name_unit',
        inputs='Provide details of Amazon deliveries for visitor John Doe at unit 123 last week (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "deliveryEvents",
                "companyId": {"$oid": "6159af2a99e90e0013e5f071"},
                "delivererName": "John Doe",
                "date": {
                    "$gte": {"$date": "last_week_start"},
                    "$lt": {"$date": "last_week_end"}
                }
            }
        },
        metadata={'difficulty': 'easy'},
    ),
    Case(
        name='deliveries_this_month_dhl_name',
        inputs='Which deliveries were made by DHL for visitor Jane Smith this month? (today is {today})',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "deliveryEvents",
                "delivererName": "Jane Smith",
                "date": {
                    "$gte": {"$date": "month_start"},
                    "$lt": {"$date": "today_end"}
                }
            }
        },
        metadata={'difficulty': 'easy'},
    ),
    Case(
        name='deliveries_date_range_noon_unit_report',
        inputs='Give a report of Noon deliveries received at unit 789 between 01/10/2025 and 05/10/2025.',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "deliveryEvents",
                "companyId": {"$oid": "64e2f3be6e499a001219b0fa"},
                "date": {
                    "$gte": {"$date": "2025-10-01T00:00:00.000Z"},
                    "$lt": {"$date": "2025-10-06T00:00:00.000Z"}
                }
            }
        },
        metadata={'difficulty': 'easy'},
    ),
    # Filter by Extra Field
    Case(
        name='check_ins_all_extra_company_purpose',
        inputs='Show all visitors where Company Name is ABC Corp and Purpose of Visit is \'Maintenance\' (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "enterEvents",
                "extraField": "ABC Corp",
                "secondExtraField": "Maintenance"
            }
        },
        metadata={'difficulty': 'medium'},
    ),
    Case(
        name='check_ins_all_extra_badge_company',
        inputs='List all check-ins where Badge No. is B12345 and Company Name is XYZ Ltd (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "enterEvents",
                "thirdExtraField": "B12345",
                "extraField": "XYZ Ltd"
            }
        },
        metadata={'difficulty': 'medium'},
    ),
    Case(
        name='check_ins_manual_extra_purpose_company',
        inputs='Provide details of manual check-ins where Purpose of Visit is \'Inspection\' and Company Name is DEF Ltd (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "enterEvents",
                "entryType": "manual",
                "secondExtraField": "Inspection",
                "extraField": "DEF Ltd"
            }
        },
        metadata={'difficulty': 'medium'},
    ),
    Case(
        name='deliveries_all_extra_company_purpose',
        inputs='Show all deliveries where Company Name is ABC Corp and Purpose of Visit is \'Sample Collection\' (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "deliveryEvents",
                "extraField": "ABC Corp",
                "secondExtraField": "Sample Collection"
            }
        },
        metadata={'difficulty': 'medium'},
    ),
    Case(
        name='check_ins_qr_code_extra_badge_purpose_report',
        inputs='Give a report of QR code check-ins where Badge No. is Q98765 and Purpose of Visit is \'Delivery\' (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "enterEvents",
                "entryType": "qrCode",
                "thirdExtraField": "Q98765",
                "secondExtraField": "Delivery"
            }
        },
        metadata={'difficulty': 'medium'},
    ),
    Case(
        name='check_ins_eid_extra_company_badge',
        inputs='List all Emirates ID check-ins where Company Name is XYZ Ltd and Badge No. is E12345 (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "enterEvents",
                "entryType": "emiratesId",
                "extraField": "XYZ Ltd",
                "thirdExtraField": "E12345"
            }
        },
        metadata={'difficulty': 'medium'},
    ),
    Case(
        name='check_outs_manual_extra_purpose_company',
        inputs='Show manual check-outs where Purpose of Visit is \'Training\' and Company Name is LMN Ltd (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "leaveEvents",
                "leaveType": "manualExit",
                "secondExtraField": "Training",
                "extraField": "LMN Ltd"
            }
        },
        metadata={'difficulty': 'medium'},
    ),
    Case(
        name='deliveries_all_extra_badge_company',
        inputs='Provide all deliveries where Badge No. is D12345 and Company Name is ABC Corp (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "deliveryEvents",
                "thirdExtraField": "D12345",
                "extraField": "ABC Corp"
            }
        },
        metadata={'difficulty': 'medium'},
    ),
    Case(
        name='check_ins_qr_code_extra_purpose_company',
        inputs='Show all QR code check-ins where Purpose of Visit is \'Meeting\' and Company Name is XYZ Ltd (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "enterEvents",
                "entryType": "qrCode",
                "secondExtraField": "Meeting",
                "extraField": "XYZ Ltd"
            }
        },
        metadata={'difficulty': 'medium'},
    ),
    Case(
        name='check_ins_eid_extra_purpose_badge_report',
        inputs='Give a report of Emirates ID check-ins where Purpose of Visit is \'Interview\' and Badge No. is E54321 (today is {today}).',
        expected_output={
            "collection": "events",
            "filter": {
                "type": "enterEvents",
                "entryType": "emiratesId",
                "secondExtraField": "Interview",
                "thirdExtraField": "E54321"
            }
        },
        metadata={'difficulty': 'medium'},
    ),
]


class MongoQueryEvaluator(Evaluator[dict, dict]):
    """Evaluator that recursively compares MongoDB query structures."""
    
    def _is_valid_date_format(self, date_str):
        """Check if a string is a valid ISO date format."""
        if not isinstance(date_str, str):
            return False
        # Check for ISO 8601 format
        import re
        return bool(re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', date_str))
    
    def _compare(self, expected, actual):
        """Returns (matched_fields, total_expected_fields)."""
        if expected is None:
            return (1, 1) if actual is not None else (0, 1)
        
        if isinstance(expected, dict):
            if not isinstance(actual, dict):
                return (0, self._count_fields(expected))
            
            matched = total = 0
            for key, exp_val in expected.items():
                if key in actual:
                    m, t = self._compare(exp_val, actual[key])
                    matched += m
                    total += t
                else:
                    total += self._count_fields(exp_val)
            return (matched, total)
        
        elif isinstance(expected, list):
            if not isinstance(actual, list):
                return (0, self._count_fields(expected))
            
            matched = total = 0
            for i, exp_item in enumerate(expected):
                act_item = actual[i] if i < len(actual) else None
                m, t = self._compare(exp_item, act_item)
                matched += m
                total += t
            return (matched, total)
        
        else:
            # Primitive comparison
            if expected == actual:
                return (1, 1)
            
            # Handle string comparisons
            if isinstance(expected, str) and isinstance(actual, str):
                # Check if expected is a date placeholder
                date_placeholders = [
                    'today_start', 'today_end',
                    'yesterday_start', 'yesterday_end',
                    'week_start', 'last_week_start', 'last_week_end',
                    'month_start', 'last_month_start', 'last_month_end'
                ]
                if expected in date_placeholders and self._is_valid_date_format(actual):
                    return (1, 1)
                
                # Case-insensitive string comparison
                return (1, 1) if expected.lower() == actual.lower() else (0, 1)
            
            return (0, 1)
    
    def _count_fields(self, obj):
        """Count total fields in nested structure."""
        if isinstance(obj, dict):
            return sum(self._count_fields(v) for v in obj.values())
        elif isinstance(obj, list):
            return sum(self._count_fields(item) for item in obj)
        return 1
    
    def evaluate(self, ctx: EvaluatorContext[dict, dict]) -> float:

        print('output', ctx.output)
        print('expected_output', ctx.expected_output)
        if ctx.output == ctx.expected_output:
            return 1.0
        if not ctx.expected_output or not ctx.output:
            return 0.0
        
        matched, total = self._compare(ctx.expected_output, ctx.output)
        return matched / total if total > 0 else 0.0

dataset = Dataset(cases=cases[:5], evaluators=[MongoQueryEvaluator()])

# output {'collection': 'events', 'filter': {'entryType': 'qr', 'createdAt': {'$gte': {'$date': '2025-10-20T00:00:00Z'}, '$lt':
# {'$date': '2025-10-21T00:00:00Z'}}}}
# expected_output {'collection': 'events', 'filter': {'type': 'enterEvents', 'entryType': 'qrCode', 'date': {'$gte': {'$date':
# 'today_start'}, '$lt': {'$date': 'today_end'}}}}

# Create AI function wrapper for pydantic_evals
def ai_mongo_query(user_query: str) -> dict:
    """
    AI function that can be used with pydantic_evals.
    Takes a natural language query and returns MongoDB query structure.
    """
    agent = MongoDBAgent()
    result = agent.query_sync(user_query)
    return {
        "collection": result.get("collection"),
        "filter": result.get("filter")
    }

# Example usage for evaluation:
# dataset.evaluate_sync(ai_mongo_query)
# 
# Or run specific cases:
# result = ai_mongo_query("Show all visitors who checked in today")
