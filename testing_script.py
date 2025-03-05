import json

from SpellboundTransmutations import (
    naive_recursive_edit_distance,
    iterative_edit_distance,
    memoized_edit_distance
)

def test_naive_from_json(naive_data):
    """
    Re-computes naive recursive distances for each test stored in JSON
    and compares with the previously saved 'naive_distance'.
    """
    print("=== Testing Naive Recursive Approach (from JSON) ===")
    summary = {"total": 0, "passed": 0, "failed": 0}

    for record in naive_data:
        summary["total"] += 1

        test_id = record.get("test_id")
        source = record.get("source")
        target = record.get("target")
        costs = record.get("costs", {})
        stored_distance = record.get("naive_distance")

        ci = costs.get("insert", 10)
        cd = costs.get("delete", 50)
        cs = costs.get("substitute", 100)
        ct = costs.get("transpose", 20)

        # Compute fresh distance
        computed_distance = naive_recursive_edit_distance(source, target, ci, cd, cs, ct)

        # Compare
        if computed_distance == stored_distance:
            result_str = "Success"
            summary["passed"] += 1
        else:
            result_str = f"Failed (Expected: {stored_distance}, Got: {computed_distance})"
            summary["failed"] += 1

        print(f"Test {test_id}: '{source}' -> '{target}'")
        print(f"  Stored Naive Distance: {stored_distance}")
        print(f"  Computed Naive Distance: {computed_distance} => {result_str}")
        print("  Transformed Output: N/A (Naive approach does not track output)\n")

    return summary


def test_dp_from_json(dp_data):
    """
    Re-computes iterative and memoized DP results for each test stored in JSON
    and compares with the previously saved distances/outputs.
    """
    print("=== Testing Dynamic Programming Approaches (from JSON) ===")
    iterative_summary = {"total": 0, "passed": 0, "failed": 0}
    memoized_summary = {"total": 0, "passed": 0, "failed": 0}

    for record in dp_data:
        test_id = record.get("test_id")
        source = record.get("source")
        target = record.get("target")
        costs = record.get("costs", {})

        stored_iter_dist = record.get("iterative_distance")
        stored_iter_out = record.get("iterative_output")
        stored_memo_dist = record.get("memoized_distance")
        stored_memo_out = record.get("memoized_output")

        ci = costs.get("insert", 10)
        cd = costs.get("delete", 50)
        cs = costs.get("substitute", 100)
        ct = costs.get("transpose", 20)

        # ==============================
        # Iterative DP
        # ==============================
        iterative_summary["total"] += 1
        comp_iter_dist, comp_iter_out = iterative_edit_distance(source, target, ci, cd, cs, ct)

        if comp_iter_dist == stored_iter_dist and comp_iter_out == stored_iter_out:
            iter_result = "Success"
            iterative_summary["passed"] += 1
        else:
            iter_result = (
                "Failed\n"
                f"    (Distance Expected: {stored_iter_dist}, Got: {comp_iter_dist}\n"
                f"     Output Expected: '{stored_iter_out[:50]}...', Got: '{comp_iter_out[:50]}...')"
            )
            iterative_summary["failed"] += 1

        # ==============================
        # Memoized DP
        # ==============================
        memoized_summary["total"] += 1
        comp_memo_dist, comp_memo_out = memoized_edit_distance(source, target, ci, cd, cs, ct)

        if comp_memo_dist == stored_memo_dist and comp_memo_out == stored_memo_out:
            memo_result = "Success"
            memoized_summary["passed"] += 1
        else:
            memo_result = (
                "Failed\n"
                f"    (Distance Expected: {stored_memo_dist}, Got: {comp_memo_dist}\n"
                f"     Output Expected: '{stored_memo_out[:50]}...', Got: '{comp_memo_out[:50]}...')"
            )
            memoized_summary["failed"] += 1

        # ==============================
        # Print results
        # ==============================
        print(f"\nTest {test_id}:")
        if len(source.split()) > 50:
            print("Source: [Large text with {} words]".format(len(source.split())))
        else:
            print(f"Source: {source}")

        if len(target.split()) > 50:
            print("Target: [Large text with {} words]".format(len(target.split())))
        else:
            print(f"Target: {target}")

        print(f"\nCosts: Insert={ci}, Delete={cd}, Substitute={cs}, Transpose={ct}")

        print(f"\nIterative DP Edit Distance (stored vs. computed): {stored_iter_dist} vs. {comp_iter_dist}")
        print(f"Stored DP Output:   '{stored_iter_out[:50]}...'")
        print(f"Computed DP Output: '{comp_iter_out[:50]}...' => {iter_result}")

        print(f"\nMemoized DP Edit Distance (stored vs. computed): {stored_memo_dist} vs. {comp_memo_dist}")
        print(f"Stored DP Output:   '{stored_memo_out[:50]}...'")
        print(f"Computed DP Output: '{comp_memo_out[:50]}...' => {memo_result}\n")

    return iterative_summary, memoized_summary


def print_summary(naive_sum, iter_sum, memo_sum):
    """
    Print a summary table of pass/fail totals for naive, iterative, and memoized.
    """
    total_tests = naive_sum["total"] + iter_sum["total"] + memo_sum["total"]
    total_passed = naive_sum["passed"] + iter_sum["passed"] + memo_sum["passed"]
    total_failed = naive_sum["failed"] + iter_sum["failed"] + memo_sum["failed"]

    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print("{:<25} {:<10} {:<10} {:<10}".format("Approach", "Total", "Passed", "Failed"))
    print("-"*70)
    print("{:<25} {:<10} {:<10} {:<10}".format("Naive Recursive", naive_sum["total"], naive_sum["passed"], naive_sum["failed"]))
    print("{:<25} {:<10} {:<10} {:<10}".format("Iterative DP", iter_sum["total"], iter_sum["passed"], iter_sum["failed"]))
    print("{:<25} {:<10} {:<10} {:<10}".format("Memoized DP", memo_sum["total"], memo_sum["passed"], memo_sum["failed"]))
    print("-"*70)
    print("{:<25} {:<10} {:<10} {:<10}".format("Overall", total_tests, total_passed, total_failed))
    print("="*70)


def main():
    # Load the stored distances/results from JSON (generated by admin.py)
    with open("test_distances.json", "r", encoding="utf-8") as f:
        all_data = json.load(f)

    # Extract naive and dp test data
    naive_data = all_data.get("naive_tests", [])
    dp_data = all_data.get("dp_tests", [])

    # Compare naive results
    naive_summary = test_naive_from_json(naive_data)

    # Compare DP results
    iterative_summary, memoized_summary = test_dp_from_json(dp_data)

    # Print final summary
    print_summary(naive_summary, iterative_summary, memoized_summary)


if __name__ == "__main__":
    main()
