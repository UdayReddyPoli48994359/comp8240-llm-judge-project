# COMP8240 Project Update — Video Script
**Target: 5:10 total · Face-cam required throughout (corner window while screen-sharing)**

---

## Slide 1 — Cover (0:00–0:15)
*On screen: title slide*

> Hi, I'm Uday. This is my Assignment 2 update for COMP8240, on reproducing and extending Zheng et al.'s LLM-as-a-judge paper using FastChat and MT-Bench. I'll recap the project, then walk through my replication progress and new data.

---

## Slide 2 — Project Basis (0:15–0:50)
*On screen: paper title, authors, venue, code repo*

> My project replicates "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena," by Zheng et al., published at NeurIPS 2023. The code is open-source — lm-sys's FastChat repository on GitHub, specifically its llm_judge module. I chose this paper because it sits squarely in LLM-as-judge and RAG evaluation, an area I wanted to build on, and because I could verify upfront that it was actually feasible: the code is public, well-documented, and — since judging only calls an API — doesn't need a GPU to run.

---

## Slide 3 — The Original Dataset (0:50–1:35)
*On screen: 80 questions / 8 categories / 2 turns*

> The paper's benchmark is MT-Bench: 80 carefully designed multi-turn questions spanning eight categories — writing, roleplay, extraction, reasoning, math, coding, STEM, and humanities. Each question has two turns, so a model has to hold context and follow up, not just answer once. The core idea the paper tests is LLM-as-a-judge: instead of paying humans to score every model response, you ask a strong model like GPT-4 to do it. Their headline result is that GPT-4's judgments agree with human preference more than eighty percent of the time — roughly as often as two humans agree with each other. That's the number I'm going to try to reproduce myself.

---

## Slide 4 — Architecture & Running the Code (1:35–2:35)
*On screen: pipeline diagram → **switch to screen share partway through this slide, at the exact cue below***

> Here's the high-level architecture. First, gen_api_answer.py calls each candidate model's API and saves its answers to the 80 MT-Bench questions. Then gen_judgment.py sends those answers, plus the question and — for math and coding — a reference answer, to GPT-4, which returns a numeric judgment. I ran this myself: cloned FastChat, installed its llm_judge dependencies, and confirmed all 80 questions across all 8 categories load correctly and the scripts execute without errors. I did this twice — once in this working environment, and again independently on my own MacBook Air, Python 3.12, to make sure it wasn't a fluke.
>
> **[Cut to screen share here. In your FastChat/fastchat/llm_judge directory, run exactly this:**
> ```
> python -c "import json; data=[json.loads(l) for l in open('data/mt_bench/question.jsonl')]; print(len(data), 'questions'); print(sorted(set(d['category'] for d in data)))"
> ```
> **This prints `80 questions` and the 8 category names — real, verifiable output that the original data loads correctly in your environment. Narrate it as "here's the environment with the 80 questions loading across the 8 categories," not as a full judged run.]**
>
> No GPU is needed for this part — it's pure API calls — so the only real requirement is an OpenAI API key and a modest amount of paid credit.

---

## Slide 5 — Two Real Issues, Fixed (2:35–3:05)
*On screen: dependency list + the KeyError fix*

> Along the way, I hit two real issues worth mentioning. First, four dependencies the package doesn't declare — anthropic, torch, transformers, and accelerate — are actually required just to import the judging code, even though the package's own install extras don't list them. Second, adding my own question category crashed grading with a KeyError, because every category has to be registered by name in a temperature-config dictionary with no fallback. I tracked down both and fixed them — one install step, one line of code.

---

## Slide 6 — The Headline Number, Reproduced (3:05–3:40)
*On screen: agreement-rate table*

> For the headline number itself, I found something better than running my own paid judging pass: the authors released their original GPT-4 votes and 3.3 thousand human votes as a public dataset on Hugging Face, in the exact format their own agreement script expects. I used that to reproduce their headline result directly, on my own machine: excluding ties, GPT-4 agreed with human preference 85.9% on turn one and 85.3% on turn two — both above their 80% claim, and actually slightly higher than human-to-human agreement itself.

---

## Slide 7 — New Data: Description (3:40–4:15)
*On screen: HumanEval card + new-questions card*

> For new data, I'm using one existing dataset and building one of my own. The existing one is HumanEval — 164 real coding problems, each with a prompt, a canonical solution, and an executable test suite — which gives an objective pass-fail signal I can compare against the judge's subjective score. The one I'm constructing is sixteen new MT-Bench-style questions in two categories: eight harder coding problems, and eight questions testing Australian local-context knowledge — things like GST, Medicare, and preferential voting — which the original benchmark never covers.

---

## Slide 8 — New Data: Progress (4:15–4:55)
*On screen: three verification checkmarks → **second screen-share cut partway through, at the exact cue below***

> On construction progress: all sixteen questions are written in FastChat's exact two-turn schema, so they drop straight into the pipeline.
>
> **[Cut to screen share here — second cut. In your new_data directory, run exactly this:**
> ```
> python test_refs.py
> ```
> **This is my own test harness, not FastChat's, executing live against the 8 reference answers I wrote for the new coding questions — including a 100-thread concurrency stress test and a file-backed IP-counting test. It prints `ALL 8 REFERENCE ANSWERS VERIFIED`. Narrate it as "this is my own code, actually running and passing" — this is the clearest live proof that the new-data work is real, not just described.]**
>
> One question's wording was corrected after testing showed its reference solution didn't actually use bounded memory as originally claimed. I also verified HumanEval's pass-fail mechanism actually discriminates, by running both a correct and a deliberately wrong solution through it.

---

## Slide 9 — Wrap-up (4:55–5:10)
*On screen: summary bullets*

> So: the original pipeline runs, the headline result reproduces, two real bugs are fixed, and sixteen new questions with tested references are ready. Next, I'll run the full judge across my new categories. Thanks for watching.

---

### Timing check
- Recap (slides 1–4): 0:00–2:35 (~2m35s, within the suggested 2.5–3 min)
- Update (slides 5–8): 2:35–4:55 (~2m20s, within the suggested 2–2.5 min; +10s over the original plan for the second screen-share cut)
- Wrap-up (slide 9): 4:55–5:10 (~15s)
- **Total: ~5:10**, pace ≈ 150 words/minute — read it conversationally, not rushed. Still well inside the 4:30–5:30 tolerance.

### Two live demos — what each one proves
- **Slide 4 (architecture):** running FastChat's own data-loading command. This proves the *original environment and dataset* work — it is explicitly **not** your own code, and the script says so. It's evidence for the Replication rubric item.
- **Slide 8 (new data progress):** running `test_refs.py`. This **is** your own code — the test harness and the 8 reference answers it checks were both written by you. If your professor's live-demo requirement is specifically about seeing code you personally wrote execute, this is the moment that satisfies it.

### Before you record
- Face visible in a corner window for the entire video (required by the rubric).
- Have your FastChat terminal ready to switch to during Slide 4, AND a terminal open in your new_data directory ready to switch to during Slide 8 — two separate screen-share cuts.
- Export at the end as **.mp4**, keep total length within 5:00 ± 10% (4:30–5:30), submit via the iLearn dropbox before 11:55pm, 9/10/26.

### Note (this is Assignment 2's video script — already submitted)
This script is kept here as the historical record of Assignment 2 (the project update video, submitted ~4:35 runtime). It is not the Final Report — see `README.md`, `annotation_record.md`, and the Final Report itself for the current, later-stage work (including the LLM-as-judge results on the new data, added after this video was submitted).
