# RFQ-Parser
This is a request quotation parcel of varied language sentences for B2B packaging requirement products for kypson pvt ltd.
I habve uploaded score result along with all for files including NOte.md for reasons and questions asked, Parse.py for RFQ key values calling and return function, requirement.txt and my_test.jsol custom data file of sentences. 
In order to see results Upload score.py first in any v env like collab /vscode
then parse.py, then requiremnts.txt and then my-tests.jsonl
run this command then to see score-
!python score.py my_tests.jsonl
Run this code to see mismatch(In my casse min 3 were shown)-
#In my sentences in my_tests.jsonl
import json
from parse import parse_rfq

# Open MY test file and find mismatches
with open("my_tests.jsonl", "r", encoding="utf-8") as f:
    mismatches = 0
    for i, line in enumerate(f):
        if not line.strip():
            continue
        data = json.loads(line)
        text = data["text"]
        expected = data["expected"]
        got = parse_rfq(text)
        
        # Compare dictionaries
        if got != expected:
            mismatches += 1
            print(f"--- Mismatch #{mismatches} (Row {i+1}) ---")
            print(f"Text:     {text}")
            print(f"Expected: {expected}")
            print(f"Got:      {got}\n")
            if mismatches >= 3:
                break # Stop after finding 3

