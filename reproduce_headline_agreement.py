"""
Reproduce Zheng et al. (2023)'s headline agreement-rate result WITHOUT
needing an OpenAI API key or any paid API spend.

The original authors released:
  - 3.3K expert/author pairwise human votes
  - GPT-4's own pairwise votes on the same question/model pairs
both as the `lmsys/mt_bench_human_judgments` dataset on Hugging Face
(splits: "human" and "gpt4_pair"), in the exact vote-record schema used
by FastChat's own fastchat/llm_judge/compute_agreement.py.

This script loads that dataset and computes:
  1. GPT-4-vs-human agreement rate (the paper's headline >80% claim)
  2. human-vs-human agreement rate (their point of comparison)

Run this on a machine with normal internet access (this sandbox's
network egress blocks huggingface.co, so it could not be run from here).

Usage:
    pip install datasets
    python reproduce_headline_agreement.py
"""
from datasets import load_dataset
from collections import defaultdict


def revert(vote):
    return {"model_a": "model_b", "model_b": "model_a"}.get(vote, vote)


def normalise_key(row):
    """Order (model_a, model_b) consistently so the same pair always
    hashes to the same key regardless of which side was 'a' vs 'b'."""
    if row["model_a"] < row["model_b"]:
        return (row["question_id"], row["model_a"], row["model_b"]), row["winner"]
    else:
        return (row["question_id"], row["model_b"], row["model_a"]), revert(row["winner"])


def build_index(dataset_split, turn):
    """key -> list of winner votes, for a given turn (1 or 2)."""
    idx = defaultdict(list)
    for row in dataset_split:
        if row["turn"] != turn:
            continue
        key, winner = normalise_key(row)
        idx[key].append(winner)
    return idx


def agreement(human_idx, gpt4_idx, ban_ties=False):
    agree, total = 0, 0
    for key, gpt4_votes in gpt4_idx.items():
        if key not in human_idx:
            continue
        gpt4_vote = gpt4_votes[0]
        if ban_ties and "tie" in gpt4_vote:
            continue
        for h_vote in human_idx[key]:
            if ban_ties and "tie" in h_vote:
                continue
            total += 1
            agree += int(gpt4_vote == h_vote)
    return agree, total


def human_human_agreement(human_idx, ban_ties=False):
    agree, total = 0, 0
    for votes in human_idx.values():
        for i in range(len(votes)):
            for j in range(i + 1, len(votes)):
                v1, v2 = votes[i], votes[j]
                if ban_ties and ("tie" in v1 or "tie" in v2):
                    continue
                total += 1
                agree += int(v1 == v2)
    return agree, total


if __name__ == "__main__":
    ds = load_dataset("lmsys/mt_bench_human_judgments")
    human, gpt4 = ds["human"], ds["gpt4_pair"]

    for turn in (1, 2):
        h_idx = build_index(human, turn)
        g_idx = build_index(gpt4, turn)

        a, t = agreement(h_idx, g_idx, ban_ties=False)
        print(f"Turn {turn} | GPT-4 vs human | with ties   | {a}/{t} = {a/t:.1%}")

        a, t = agreement(h_idx, g_idx, ban_ties=True)
        print(f"Turn {turn} | GPT-4 vs human | without ties| {a}/{t} = {a/t:.1%}")

        a, t = human_human_agreement(h_idx, ban_ties=False)
        print(f"Turn {turn} | human vs human | with ties   | {a}/{t} = {a/t:.1%}")

        a, t = human_human_agreement(h_idx, ban_ties=True)
        print(f"Turn {turn} | human vs human | without ties| {a}/{t} = {a/t:.1%}")
        print()
