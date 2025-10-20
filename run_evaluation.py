"""
Run evaluation of MongoDB AI Agent using pydantic_evals.

Usage:
    python run_evaluation.py
"""

import sys
from pathlib import Path
from dotenv import load_dotenv

# Add dataset directory to path
sys.path.insert(0, str(Path(__file__).parent / "dataset"))

from dataset import dataset, ai_mongo_query

# Load environment variables
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()

def main():
    print("=" * 80)
    print("MongoDB AI Agent Evaluation")
    print("=" * 80)
    print()
    
    # Option 1: Evaluate all cases
    print("Running evaluation on dataset...")
    print(f"Total cases: {len(dataset.cases)}")
    print()
    
    # Option 2: Test with a single case
    # print("Testing with a single example...")
    # test_query = "Show all visitors who checked in today with Emirates ID 60ae050577dba90011862e03"
    # print(f"Query: {test_query}")
    # print()
    
    try:
        results = dataset.evaluate_sync(ai_mongo_query)


        print("Result:")
        print(results)
        # print(f"  Collection: {result.get('collection')}")
        # print(f"  Filter: {result.get('filter')}")
        # print()
        # print("✅ Test successful!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

