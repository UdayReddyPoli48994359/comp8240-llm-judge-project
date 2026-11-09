# Assignment 2 — work done so far

## 1. New question set (`question_additions.jsonl`)
16 new MT-Bench-style two-turn questions, in FastChat's exact schema
(`question_id`, `category`, `turns: [turn1, turn2]`):

- 8 questions, category `"coding"` (ids 1001-1008) — harder/more varied
  than the original benchmark's coding questions (linked-list cycle
  detection, streaming top-K, buggy binary search, SQL window functions,
  race conditions, rate limiters, bracket/tag balancing, geo closest-pair).
- 8 questions, category `"au_context"` (ids 2001-2008) — Australian/local
  context (small business grants, GST, local government, preferential
  voting, Medicare, home buying, visas, daylight saving).

## 2. Reference answers (`reference_answer_additions.jsonl`)
FastChat's `NEED_REF_CATS` list includes `"coding"`, so the 8 coding
questions need reference answers to be judged in reference-guided mode.
Wrote real, correct solutions for all 8, and **all 8 are now
unit-tested** in `test_refs.py` — executed against concrete inputs
(including a 100-thread concurrency stress test for the rate limiter,
and a temp-file-backed run for the IP-counting question), not just
eyeballed. Running `python test_refs.py` prints
`ALL 8 REFERENCE ANSWERS VERIFIED`.

Question 1002's wording was also corrected: turn 1 originally asked to
solve the problem "using bounded memory," but its solution is actually
O(number of distinct IPs), not fixed — the question now asks to solve
it "without loading the entire file into memory," and the genuinely
fixed-memory, approximate version is introduced in turn 2 instead. See
`annotation_record.md` for the full construction/QC record, including
the per-question review criteria for both categories.

## 3. Real technical findings from re-running the install + extending it
Beyond the proposal's two known install quirks (`wavedrom` build
failure, `openai<1` pin), actually importing `fastchat/llm_judge/common.py`
end-to-end surfaced three more real dependency requirements not obvious
from the package's own declared `llm_judge` extras
(`pyproject.toml` only lists `openai<1`, `anthropic>=0.3`, `ray`):
`anthropic` (imported unconditionally even if unused as a judge),
then transitively `torch`, `transformers`, and `accelerate` — because
`common.py` unconditionally imports `fastchat.model.model_adapter`,
which is only actually needed for *local* model inference, not pure
API-based judging. All now installed and the import succeeds cleanly.

**New category registration bug (found + fixed):** adding a brand-new
question category (`"au_context"`) and trying to grade it raises
`KeyError: 'au_context'` from `temperature_config` in `common.py`,
because that dict has no default/fallback — every category must be
registered by name. Fixed with a one-line patch
(`"au_context": 0.7,`), verified the KeyError is gone and the category
now gets a sensible non-deterministic sampling temperature (0.7, same
as `writing`/`roleplay`, since it's open-ended, not reference-checked).

## 4. Headline-result reproduction — doesn't need an API key at all
Found that the original authors released the **actual GPT-4 judge votes
and 3.3K human votes** as a Hugging Face dataset
(`lmsys/mt_bench_human_judgments`), in exactly the vote-record format
FastChat's own `compute_agreement.py` expects. That means the paper's
headline ">80% GPT-4-vs-human agreement" figure can be reproduced for
free, with zero OpenAI spend — no live judging run required.

Wrote `reproduce_headline_agreement.py`, which loads that dataset and
computes both GPT-4-vs-human and human-vs-human agreement rates (with
and without ties), mirroring the original script's logic.

**This could not be run from this sandbox** — huggingface.co is
blocked by this environment's network policy (confirmed: direct `curl`
to huggingface.co gets rejected by the egress proxy). It was instead
run on Uday's own machine, and it worked:

```
Turn 1 | GPT-4 vs human | without ties | 911/1060 = 85.9%
Turn 1 | human vs human | without ties | 633/772  = 82.0%
Turn 2 | GPT-4 vs human | without ties | 912/1069 = 85.3%
Turn 2 | human vs human | without ties | 649/778  = 83.4%
```

Both turns reproduce the paper's ">80%" headline claim, and GPT-4's
agreement with human preference is actually slightly higher than
human-vs-human agreement itself, excluding ties. This is the strongest
piece of evidence for the "Replication of Original Work" rubric
criterion — it's a real number, independently reproduced, not just a
claim that the code "should work."

## What's still open
- No LLM judging pass has been run yet on the 16 new questions
  themselves (only the original 80-question MT-Bench headline result
  has been reproduced). Running even a small subset through
  `gen_api_answer.py` / `gen_judgment.py` would strengthen the
  "Replication of Original Work" section further, but is not required
  — see `annotation_record.md` and the video script for how this is
  framed without it.
