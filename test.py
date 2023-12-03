import os
import subprocess
import sys

def run_test(test_name, adventure_script, map_file):
    with open(f"test/{test_name}.in", 'r') as infile, open(f"test/{test_name}.out", 'r') as expected_outfile:
        try:
            # Run the game and capture the output
            completed_process = subprocess.run(
                [sys.executable, adventure_script, map_file],
                stdin=infile, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True
            )
            actual_output = completed_process.stdout

            # Read the expected output
            expected_output = expected_outfile.read()

            # Compare actual output to expected output
            return actual_output == expected_output

        except Exception as e:
            return f"Error: {e}"

def main():
    adventure_script = "adventure.py"
    map_file = "loop.map"
    test_folder = "test"

    test_results = {}
    failed_tests = 0

    # List all .in files in the test directory
    for filename in os.listdir(test_folder):
        if filename.endswith(".in"):
            test_name = filename[:-3]
            result = run_test(test_name, adventure_script, map_file)
            test_results[test_name] = result
            if result is not True:
                failed_tests += 1

    # Print summary of test results
    for test_name, result in test_results.items():
        if result is True:
            print(f"Test {test_name}: PASSED")
        else:
            print(f"Test {test_name}: FAILED - {result}")

    print("\nSummary:")
    print(f"Total tests: {len(test_results)}")
    print(f"Passed: {len(test_results) - failed_tests}")
    print(f"Failed: {failed_tests}")

    # Exit with non-zero status if any test failed
    if failed_tests > 0:
        sys.exit(1)

if __name__ == "__main__":
    main()