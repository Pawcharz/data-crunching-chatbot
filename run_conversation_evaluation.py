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

def print_conversation_details(result):
    """Pretty print a conversation result."""
    print("\n" + "=" * 80)
    print("CONVERSATION FLOW")
    print("=" * 80)
    
    iterations = result.get("iterations", [])
    
    for i, iteration in enumerate(iterations, 1):
        print(f"\n--- Iteration {i} ---")
        
        # Show tool calls
        tool_calls = iteration.get("tool_calls", [])
        if tool_calls:
            print(f"\n🔧 Tool Calls ({len(tool_calls)}):")
            for tc in tool_calls:
                print(f"   • {tc['name']}")
                args = tc.get('arguments', {})
                if 'collection' in args:
                    print(f"     Collection: {args['collection']}")
                if 'filter' in args:
                    print(f"     Filter: {json.dumps(args['filter'], indent=6)}")
                if tc.get('success'):
                    print(f"     ✓ Success")
                else:
                    print(f"     ✗ Failed: {tc.get('error', 'Unknown error')}")
        
        # Show final answer
        final_answer = iteration.get("final_answer")
        if final_answer:
            print(f"\n💬 Agent Response:")
            print(f"   {final_answer[:200]}...")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Collection: {result.get('collection')}")
    print(f"Filter: {json.dumps(result.get('filter'), indent=2)}")
    print(f"Total Iterations: {len(iterations)}")

def main():
    print("=" * 80)
    print("MongoDB AI Agent - Conversation Evaluation")
    print("=" * 80)
    print()
    
    print("Running evaluation on conversation dataset...")
    print(f"Total cases: {len(dataset.cases)}")
    print()
    
    # Option to test single case first
    test_single = False
    if test_single:
        print("Testing single case first...\n")
        test_case = dataset.cases[0]
        print(f"Test Case: {test_case.name}")
        print(f"Input: {test_case.inputs}")
        
        try:
            result = ai_mongo_conversation(test_case.inputs)
            print_conversation_details(result)
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
        return
    
    # Run full evaluation
    try:
        results = dataset.evaluate_sync(ai_mongo_conversation)
        
        print("\n" + "=" * 80)
        print("EVALUATION RESULTS")
        print("=" * 80)
        
        # Show the results table
        print(results)
        
        # Show summary
        print(f"\n📊 Summary:")
        print(f"   Total cases: {len(dataset.cases)}")
        print(f"   Successful: {len(results.cases)}")
        print(f"   Failed: {len(results.failures)}")
        
        # Show details of successful cases
        if results.cases:
            print("\n" + "-" * 80)
            print("✅ SUCCESSFUL CASES")
            print("-" * 80)
            for case_result in results.cases:
                print(f"\n• {case_result.name}")
                scores = case_result.scores
                for evaluator_name, score in scores.items():
                    print(f"  Score: {score:.2f}")
                    if score < 0.8:
                        print(f"  ⚠️  Score below 80% - review needed")
        
        # Show failures with details
        if results.failures:
            print("\n" + "-" * 80)
            print("❌ FAILED CASES")
            print("-" * 80)
            for failure in results.failures:
                print(f"\n• {failure.name}")
                print(f"  Input: {failure.inputs[:80]}...")
                print(f"  Error: {failure.error_message}")
                if failure.error_stacktrace:
                    # Show last 5 lines of stack trace
                    lines = [l for l in failure.error_stacktrace.split('\n') if l.strip()]
                    print(f"  Stack trace (last 5 lines):")
                    for line in lines[-5:]:
                        print(f"    {line}")
        
        # Show average scores
        if results.cases:
            print("\n" + "-" * 80)
            print("📈 AVERAGE SCORES")
            print("-" * 80)
            try:
                avg = results.averages()
                if callable(avg):
                    avg = avg()
                print(avg)
            except Exception as e:
                print(f"Could not compute averages: {e}")
        
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

