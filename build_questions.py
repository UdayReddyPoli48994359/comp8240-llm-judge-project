import json

# ---- New "coding" category questions (need reference answers; temp 0.0) ----
coding_questions = [
    {
        "question_id": 1001,
        "category": "coding",
        "turns": [
            "Write a Python function `has_cycle(head)` that detects whether a singly linked list contains a cycle, without using any extra data structure (O(1) extra space).",
            "Now modify your function so that if a cycle exists, it returns the node where the cycle begins, instead of just True/False."
        ]
    },
    {
        "question_id": 1002,
        "category": "coding",
        "turns": [
            "You have a log file far too large to fit in memory, with one IP address per line. Write Python code to find the top-5 most frequent IP addresses using bounded memory.",
            "Now suppose the log is an infinite stream (e.g. read from a socket) rather than a file. Modify your approach to maintain an approximate top-5 in a fixed, small amount of memory, and explain the trade-off you accept."
        ]
    },
    {
        "question_id": 1003,
        "category": "coding",
        "turns": [
            "Here is a Python binary search function:\n\n```python\ndef binary_search(arr, target):\n    lo, hi = 0, len(arr)\n    while lo < hi:\n        mid = (lo + hi) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            hi = mid\n        else:\n            lo = mid + 1\n    return -1\n```\n\nThis has a bug. Find it, explain why it's wrong, and fix it.",
            "Now write a variant, `insertion_point(arr, target)`, that returns the index where `target` should be inserted to keep `arr` sorted, if it is not already present."
        ]
    },
    {
        "question_id": 1004,
        "category": "coding",
        "turns": [
            "Given a table `employees(id, name, department, salary)`, write a SQL query to find the second-highest salary within each department.",
            "Rewrite the query so that if there is a tie for second-highest salary in a department, all tied employees are returned."
        ]
    },
    {
        "question_id": 1005,
        "category": "coding",
        "turns": [
            "Explain what a race condition is in concurrent programming, and write a short Python example using the `threading` module that demonstrates one (e.g. two threads incrementing a shared counter).",
            "Fix the race condition in your example using an appropriate synchronization primitive, and explain why your fix works."
        ]
    },
    {
        "question_id": 1006,
        "category": "coding",
        "turns": [
            "Design a simple token-bucket rate limiter as a Python class, with a `allow_request()` method that returns True/False.",
            "Your rate limiter will be used by multiple threads in the same process. Explain what could go wrong with your original implementation under concurrent access, and show how you would make it thread-safe."
        ]
    },
    {
        "question_id": 1007,
        "category": "coding",
        "turns": [
            "Write a function `is_balanced(s)` that checks whether a string containing `()`, `{}`, and `[]` has balanced brackets.",
            "Extend your function to also validate that simple custom tags like `<div>...</div>` are properly opened and closed in a simplified HTML-like string (you can assume tags never have attributes)."
        ]
    },
    {
        "question_id": 1008,
        "category": "coding",
        "turns": [
            "Write a Python function that takes a list of GPS coordinates and returns the pair of points that are closest together, using the haversine formula for distance.",
            "Explain how you would modify it to run faster than O(n^2) for a large input, and what the trade-off is."
        ]
    },
]

# ---- New "au_context" category questions (general/open-ended; no reference needed) ----
au_context_questions = [
    {
        "question_id": 2001,
        "category": "au_context",
        "turns": [
            "A small business in regional New South Wales wants to apply for a state government small-business grant. Explain, in plain language, the general steps such a business would typically need to take.",
            "Note two things they should verify on the relevant state government website before applying, and why those checks matter."
        ]
    },
    {
        "question_id": 2002,
        "category": "au_context",
        "turns": [
            "Explain the difference between GST and payroll tax for an Australian small business owner, in plain language.",
            "Give a simple worked example: calculate the GST component of a $220 sale (GST-inclusive)."
        ]
    },
    {
        "question_id": 2003,
        "category": "au_context",
        "turns": [
            "A friend overseas asks what the difference is between a 'shire', a 'city council', and 'state government' in Australia. Explain it simply.",
            "Give one example of a responsibility typically handled by each of the three levels."
        ]
    },
    {
        "question_id": 2004,
        "category": "au_context",
        "turns": [
            "Summarise how preferential voting works in an Australian federal election, for someone who has never voted before.",
            "Walk through a simplified example with 3 candidates showing how a voter's preferences get distributed if their first choice is eliminated."
        ]
    },
    {
        "question_id": 2005,
        "category": "au_context",
        "turns": [
            "Explain what the Medicare Safety Net is and roughly when it applies, in plain language for someone new to Australia.",
            "Note two things they should double-check on the official Services Australia website before relying on your explanation."
        ]
    },
    {
        "question_id": 2006,
        "category": "au_context",
        "turns": [
            "Describe the general process and rough timeline for buying a first home in New South Wales, including stamp duty and the cooling-off period.",
            "Explain, in one paragraph, who is typically eligible for the First Home Buyer Assistance scheme."
        ]
    },
    {
        "question_id": 2007,
        "category": "au_context",
        "turns": [
            "Explain the difference between a working holiday visa and a skilled migration pathway for someone who wants to stay in Australia long-term.",
            "List two official sources they should check for current, authoritative visa rules rather than relying on your answer alone."
        ]
    },
    {
        "question_id": 2008,
        "category": "au_context",
        "turns": [
            "A tourist asks why daylight saving time differs between Australian states and territories. Explain it simply.",
            "If it is 3:00pm AEDT in Sydney on a day when daylight saving is in effect, what time is it in Brisbane, which does not observe daylight saving?"
        ]
    },
]

all_questions = coding_questions + au_context_questions
with open("/tmp/comp8240/new_data/question_additions.jsonl", "w") as f:
    for q in all_questions:
        f.write(json.dumps(q) + "\n")

print(f"Wrote {len(all_questions)} new questions "
      f"({len(coding_questions)} coding + {len(au_context_questions)} au_context)")
