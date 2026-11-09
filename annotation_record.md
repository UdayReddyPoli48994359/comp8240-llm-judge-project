# New Data — Annotation & Quality-Control Record

Every new question went through the same construction pass: written by hand against FastChat's
exact two-turn schema, then reviewed against the criterion below before being included. This
record exists to give explicit annotation/quality-control evidence for the "New Data – Progress"
rubric item, not just a description of the data itself.

## Coding questions (8) — criterion: executable correctness

Each reference answer was reviewed against one criterion: *does running it against concrete test
inputs produce the behaviour the question asks for?* All 8 are now verified this way in
`test_refs.py` (see "Reference answer testing" below for what changed since the first pass).

| question_id | topic | criterion | reviewed | notes |
|---|---|---|---|---|
| 1001 | linked-list cycle detection | correctness | yes | tested with a real cycle and a real non-cycle list |
| 1002 | top-5 IPs, bounded vs. approximate memory | correctness + memory-model accuracy | yes | turn 1 wording corrected (see below); turn 2's approximate structure tested for a fixed candidate set |
| 1003 | binary search bug fix | correctness | yes | tested against the exact off-by-one case the bug introduces |
| 1004 | SQL dense_rank query | correctness | yes | executed against an in-memory SQLite table with a deliberate salary tie |
| 1005 | race condition, then fixed | correctness of the fix specifically | yes | racy version checked only for a plausible range; locked version asserted exact every run |
| 1006 | token-bucket rate limiter, thread safety | correctness under concurrency | yes | single-threaded behaviour checked, then a 100-thread stress test confirms the lock caps allowed requests at capacity |
| 1007 | bracket / tag balancer | correctness | yes | tested on nested, mismatched, and empty input |
| 1008 | closest-pair via haversine | correctness | yes | tested against two real-world coordinate pairs with a known approximate distance |

## Reference answer testing — what changed

The first pass only executed 4 of the 8 reference answers (1001, 1003, 1004, 1007) in
`test_refs.py`, while the written solutions existed for all 8. That gap has been closed: all 8 are
now executed and asserted in `test_refs.py`, and it prints `ALL 8 REFERENCE ANSWERS VERIFIED` on a
clean run. The remaining 4 (1002, 1005, 1006, 1008) needed test harnesses that didn't exist yet —
a temp-file-backed test for the IP counter, a multi-threaded run for the race condition and the
rate limiter, and a real-coordinate check for the haversine distance — which is why they weren't
done in the first pass.

## Question wording fix — 1002

Turn 1 originally asked to solve the problem "using bounded memory," but the reference solution's
own memory use is O(number of distinct IPs), not a fixed bound — the solution's comment already
said as much. The question now asks to solve it "without loading the entire file into memory,"
which is what the turn-1 solution actually achieves; turn 2 is where the genuinely fixed-memory,
approximate version is introduced (Count-Min Sketch). This makes the two-turn progression
accurate: turn 1 is exact-but-distinct-IP-bounded, turn 2 is approximate-but-truly-fixed-memory.

## Australian-context questions (8) — criterion: factual framing, not fixed facts

These questions (small-business grants, GST vs payroll tax, local government structure,
preferential voting, the Medicare Safety Net, home-buying, visas, daylight saving) all touch rules
that change over time — grant amounts, thresholds, visa categories. That's treated as a property of
the category, not a flaw to hide, so the review criterion here is different from the coding
questions: not "is there one fixed correct answer" but "does the question push the model toward a
defensible, well-framed answer."

| question_id | topic | criterion | reviewed | notes |
|---|---|---|---|---|
| 2001 | small-business grants (NSW) | factuality + appropriate uncertainty | yes | prompt already asks the model to note where to check current rules |
| 2002 | GST vs payroll tax | conceptual correctness | yes | distinction is structurally stable even if rates/thresholds move |
| 2003 | shire vs. city council vs. state government | conceptual correctness | yes | structural, not time-sensitive |
| 2004 | preferential voting | conceptual correctness | yes | mechanism is stable; no numeric thresholds to date |
| 2005 | Medicare Safety Net | factuality + appropriate uncertainty | yes | thresholds change yearly; judged on direction and caveats, not exact dollar figures |
| 2006 | buying a first home (NSW) | factuality + appropriate uncertainty | yes | process/sequence is stable even where specific schemes change |
| 2007 | working holiday vs. skilled migration | conceptual correctness | yes | category distinction is structurally stable |
| 2008 | daylight saving across states | factual correctness | yes | which states observe DST is slow-changing and checkable |

For judging these with an LLM, the criterion to encode in the judge prompt (per the course's LLM
evaluation material) should be: *factual correctness of stable structure/process + appropriate
uncertainty or sourcing language where figures or rules could have changed*, rather than exact
string matching against a single reference answer. This is noted here as a decision made during
construction, to be carried into the actual judging prompt later.
