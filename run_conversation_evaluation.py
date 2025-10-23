"""
Run conversation-based evaluation of MongoDB AI Agent.

This evaluates:
- Tool call sequences
- Query filters
- Agent's textual responses

Usage:
    python run_conversation_evaluation.py
"""

import sys
from pathlib import Path
from dotenv import load_dotenv
import json

# Add dataset directory to path
sys.path.insert(0, str(Path(__file__).parent / "dataset"))

from conversation_dataset import dataset, ai_mongo_conversation

# Load environment variables
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()

import logfire

from pydantic_ai import Agent

logfire.configure()  
logfire.instrument_pydantic_ai()


def main():
    print("=" * 80)
    print("MongoDB AI Agent - Conversation Evaluation")
    print("=" * 80)
    print()
    
    print("Running evaluation on conversation dataset...")
    print(f"Total cases: {len(dataset.cases)}")
    print()
    
    
    # Run full evaluation
    try:
        results = dataset.evaluate_sync(ai_mongo_conversation)
        
        print("\n" + "=" * 80)
        print("EVALUATION RESULTS")
        print("=" * 80)
        
        # Show the results table
        try:
            print(results)
        except UnicodeEncodeError:
            print("[Note: Results table contains characters that cannot be displayed in this console]")
            print(f"Results: {len(results.cases)} successful, {len(results.failures)} failed")

        # Print analysis
        # print_conversation_details(results)
        
        # Show summary
        print(f"\n[Summary]:")
        print(f"   Total cases: {len(dataset.cases)}")
        print(f"   Successful: {len(results.cases)}")
        print(f"   Failed: {len(results.failures)}")
        
    except Exception as e:
        print(f"\n[ERROR] Fatal Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

