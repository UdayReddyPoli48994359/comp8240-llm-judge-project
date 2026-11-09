# COMP8240 Assignment 2 — Everything So Far

**Status: Assignment 2 (this video/package) is done and submitted (~4:35 runtime). This folder is
kept as the historical record of that stage. The project has since moved on to Assessment Task #3
(the Project Final Report) — see that work separately.**

## The slide deck (already built, with speaker notes + timings)
https://claude.ai/artifact/8nH6HjAfkLDaxfCBBvQQxj
9 slides, structured as: Cover -> Project Basis -> Original Dataset -> Architecture & Running the Code ->
Environment Fixes -> Replication Result -> New Data Description -> New Data Progress -> Wrap-up.
Open it and use the notes/presenter view to see the speaker notes on each slide.

## Files in this folder

- **video_script.md** — the full word-for-word script, slide by slide, with exact timings (0:00-5:10),
  **two** screen-share cues, and a pre-recording checklist. Kept as the historical record.

- **README.md** — summary of all the work done: new question set, reference answers, the three hidden
  dependencies found, the category-registration bug found & fixed, and the headline-replication approach.

- **question_additions.jsonl** — 16 new MT-Bench-style questions (8 coding, 8 au_context), in FastChat's
  exact schema.

- **reference_answer_additions.jsonl** — unit-tested reference answers for the 8 new coding questions.

- **test_refs.py** — the test file that actually executes and verifies all 8 of those reference answers
  (including a 100-thread concurrency stress test for the rate limiter and a temp-file-backed test for
  the IP-counting question). Prints `ALL 8 REFERENCE ANSWERS VERIFIED` on a clean run.

- **annotation_record.md** — the quality-control record: the review criterion applied to each of the
  16 new questions, and the 1002 wording fix explained.

- **build_questions.py / build_reference_answers.py** — the scripts used to generate the two jsonl files
  above.

- **common_py_au_context_category.patch** — the one-line fix for the KeyError: 'au_context' bug in
  FastChat's common.py (temperature_config dict).

- **humaneval_inspection.md** — notes from inspecting the HumanEval dataset (164 problems, verified
  pass/fail mechanism works both ways).

- **reproduce_headline_agreement.py** — the script that reproduces the paper's headline GPT-4-vs-human
  agreement number from the authors' own released votes (lmsys/mt_bench_human_judgments on Hugging Face).
  You already ran this on your own machine and got:
    Turn 1: GPT-4 vs human 85.9% (excl. ties) | human vs human 82.0%
    Turn 2: GPT-4 vs human 85.3% (excl. ties) | human vs human 83.4%

## Assignment 2 brief, condensed
- 5-minute MP4 video, submitted via iLearn dropbox, due 11:55pm 9/10/26, worth 40% of unit grade
- Face required in a corner window throughout
- Structure: Recap & justification (~2.5-3 min) then Update/progress (~2-2.5 min) then Wrap-up (~10-15s)
- Rubric: Recap/Justification (6), Replication of Original Work (8), New Data - Description (8),
  New Data - Progress (8), Presentation Quality (10) = 40 marks total

## Assignment 2 — what was done (for the record)
1. Recorded with two terminal switches — Architecture slide (FastChat's own data) and New Data
   Progress slide (`python test_refs.py`)
2. Kept total length within 4:30-5:30 (came in at ~4:35)
3. Exported as .mp4 and submitted via iLearn dropbox before the deadline

## Next: Assessment Task #3 — Project Final Report
8-10 page ACL-LaTeX report via Overleaf, worth 40 marks/40% of unit grade. Requires a public
GitHub repo link with scripts, and a "Results on new data" section — the LLM-as-judge pass on the
16 new questions still needs to be run for this (not required for Assignment 2, but is required
here). See the Final Report work for current status on both of those.
