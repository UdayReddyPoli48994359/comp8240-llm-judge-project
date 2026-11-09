# HumanEval — inspected properties (for "New Data – Description")

Source: official OpenAI repo, `openai/human-eval`, `data/HumanEval.jsonl.gz`
(fetched and unzipped directly — not taken from memory).

- **164 problems total** (not thousands — worth saying explicitly, since
  it's easy to assume it's larger).
- Each row has 5 fields: `task_id`, `prompt` (function signature +
  docstring with examples), `entry_point` (function name to call),
  `canonical_solution` (the correct reference implementation), and
  `test` (a `check(candidate)` function with multiple `assert`s).
- Size: prompts average 451 characters (range 115–1360), canonical
  solutions average 181 characters (range 16–864), test code averages
  509 characters (range 117–1804).
- **Verified the pass/fail mechanism actually works**, both ways:
  - Ran `prompt + canonical_solution + test` for problem `HumanEval/0`
    (`has_close_elements`) — passed its own unit tests.
  - Ran the same problem with a deliberately wrong one-line solution
    (`return False`) — it correctly failed with an `AssertionError`.

This is the concrete evidence for the proposal's claim that HumanEval
gives "an objective pass/fail correctness signal that can be directly
compared against the LLM judge's subjective score": the signal is real,
discriminating, and independently confirmed here, not just assumed.
