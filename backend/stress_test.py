"""Run 8 pipeline tests with varied inputs. Tracks pass/fail count."""
import sys
from test_pipeline import run_pipeline, validate

DECISIONS = [
    "I took a wrong turn and ended up at a bookstore",
    "I signed up for a free cooking class on a whim",
    "I sat next to a stranger on the train and said hello",
    "I adopted a stray cat I found behind the grocery store",
    "I started waking up at 5 AM every morning",
    "I picked up a crumpled flyer for a marathon off the ground",
    "I switched from coffee to green tea one random Monday",
    "I volunteered at a local animal shelter for one weekend",
]

passed = 0
failed = 0

for i, decision in enumerate(DECISIONS, start=3):
    print(f"\n{'='*60}")
    print(f"TEST {i}/10: {decision}")
    print(f"{'='*60}")
    try:
        result = run_pipeline(decision)
        validate(result)
        passed += 1
    except Exception as e:
        print(f"FAILED: {e}")
        failed += 1

print(f"\n{'='*60}")
print(f"RESULTS: {passed}/8 passed, {failed}/8 failed")
print(f"TOTAL (including earlier runs): {passed + 2}/10")
print(f"EXIT CONDITION (9/10): {'MET' if passed + 2 >= 9 else 'NOT MET'}")
print(f"{'='*60}")
