# LLM-as-Judge Results on the 16 New Questions

## Methodology and deviation from the original paper

The original paper's pipeline (`gen_api_answer.py` + `gen_judgment.py`) calls a candidate model's
API for answers, then calls GPT-4 as judge, both via paid OpenAI API access. No OpenAI API key was
available for this stage of the project. Rather than skip the "Results on new data" evidence
entirely, this run uses Claude (via the assistant session used for this project) as a free
substitute for **both** roles: generating one independent set of candidate answers to the 16 new
questions (`candidate_answer_additions.jsonl`, written without looking at the reference answers),
and then separately judging those candidate answers in a second pass using FastChat's single-answer
grading convention (1-10 scale, reference-guided for the `coding` category against
`reference_answer_additions.jsonl`, and the factual-correctness + appropriate-uncertainty
criterion from `annotation_record.md` for `au_context`).

**This is a methodology deviation, stated openly, not hidden:** using the same underlying model
family for both the candidate and the judge role introduces a known self-evaluation bias risk
documented in the LLM-as-judge literature (including discussed in the original paper itself), and
Claude is not GPT-4, the model the original paper evaluates. The scores below should be read as a
working demonstration that the judging pipeline and criteria are well-defined and discriminate
between stronger and weaker answers — not as a claim that they reproduce what a live GPT-4 judging
run would score.

## Scores

### Coding (reference-guided, scored against `reference_answer_additions.jsonl`)

| id | topic | turn 1 | turn 2 | notes |
|---|---|---|---|---|
| 1001 | linked-list cycle | 9 | 9 | matches reference approach closely, correct and idiomatic |
| 1002 | top-5 IPs | 8 | 6 | turn 1 solid; turn 2's eviction strategy (drop min-count entry) is cruder than the reference's count-min sketch — bounded but no collision-aware trade-off discussion |
| 1003 | binary search fix | 9 | 9 | correctly identifies and fixes the bug, matches reference |
| 1004 | SQL dense_rank | 7 | 9 | turn 1 uses ROW_NUMBER() (works only without ties, not flagged); turn 2 correctly self-corrects to DENSE_RANK() |
| 1005 | race condition | 9 | 8 | correct demonstration and fix; turn 2's explanation slightly thinner than reference |
| 1006 | rate limiter | 8 | 7 | correct design; turn 2 describes the fix well but doesn't show the fixed code, unlike reference |
| 1007 | bracket/tag balancer | 9 | 7 | turn 1 matches reference; turn 2 uses a combined single-pass approach — plausible but less clearly correct than the reference's separated two-pass check |
| 1008 | closest-pair haversine | 9 | 8 | turn 1 matches reference; turn 2's trade-off explanation is slightly less detailed |

Coding average: turn 1 = 8.50, turn 2 = 7.88, overall = **8.19**

### Australian context (factual correctness + appropriate uncertainty)

| id | topic | turn 1 | turn 2 | notes |
|---|---|---|---|---|
| 2001 | small-business grants (NSW) | 8 | 8 | correct process, appropriate caveats both turns |
| 2002 | GST vs payroll tax | 9 | 9 | correct distinction; worked example ($220/11=$20) is exactly right |
| 2003 | shire/council/state | 7 | 7 | broadly correct but a little thin on detail |
| 2004 | preferential voting | 8 | 8 | correct mechanism and a coherent worked example |
| 2005 | Medicare Safety Net | 8 | 8 | correct concept, sensible caveats about checking current thresholds |
| 2006 | buying a first home (NSW) | 8 | 7 | correct general process; FHBAS eligibility description a bit generic |
| 2007 | working holiday vs skilled migration | 8 | 8 | correct distinction, correct official sources named |
| 2008 | daylight saving | 9 | 9 | correct state-by-state explanation; time conversion (3pm AEDT -> 2pm Brisbane) is correct |

Au_context average: turn 1 = 8.13, turn 2 = 8.00, overall = **8.06**

### Overall

All 16 questions, both turns (32 scores): **8.13 / 10** average.
Lowest-scoring answer: 1002 turn 2 (6/10) — the clearest case of a candidate answer being
functionally adequate but noticeably weaker than the reference, which is useful signal that the
judge is actually discriminating rather than defaulting to uniformly high scores.

## What this does and doesn't show

What it shows: the 16 new questions and their grading criteria are usable end-to-end — a model can
answer them, and a judge (using the criteria documented during construction) can score the answers
with real, non-uniform differentiation between stronger and weaker responses.

What it doesn't show: GPT-4-vs-human agreement specifically on this new data, since no human
annotation pass or live GPT-4 judging run was performed on these 16 questions (unlike the original
80-question MT-Bench result, which was reproduced using the authors' own released human-vote
dataset — see `reproduce_headline_agreement.py` and its results). This is stated as a limitation in
the Final Report's Results and Conclusions sections.
