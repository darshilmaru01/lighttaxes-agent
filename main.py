# main.py
import json
import sys
import os
from orchestrator.runner import run_pipeline
from tools.input_normalizer import normalize_input

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <input.json>")
        sys.exit(1)

    input_path = sys.argv[1]

    with open(input_path, "r") as f:
        raw_input = json.load(f)

    input_data = normalize_input(raw_input)

    result = run_pipeline(input_data)

    print("\n=== FORM 1040 OUTPUT ===")
    for k, v in result.items():
        print(f"{k}: {v}")

    # fpr testing only
    expected_xml_path = os.path.join(
        os.path.dirname(input_path),
        "output.xml"
    )

    # if os.path.exists(expected_xml_path):
    #     from tools.xml_compare import extract_1040_values

    #     expected = extract_1040_values(expected_xml_path)

    #     print("\n=== XML COMPARISON (Your Output vs Expected) ===")
    #     for k, v in expected.items():
    #         print(f"{k}: your={result.get(k)} | expected={v}")
    # else:
    #     print("\n(No expected XML found for comparison)")

if __name__ == "__main__":
    main()