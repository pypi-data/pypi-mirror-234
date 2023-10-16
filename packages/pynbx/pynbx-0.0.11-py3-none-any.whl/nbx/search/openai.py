from bs4 import NavigableString
import openai
from typing import List
from nbx import nbx


def construct_prompt(query, document):
    return "<|endoftext|>{document}\n\n---\n\nThe above passage is related to: {query}".format(
        document=document, query=query
    )


def get_score(context, query, log_probs, text_offsets) -> float:
    SCORE_MULTIPLIER = 100.0

    log_prob = 0
    count = 0
    cutoff = len(context) - len(query)

    for i in range(len(text_offsets) - 1, 0, -1):
        log_prob += log_probs[i]
        count += 1

        if text_offsets[i] <= cutoff and text_offsets[i] != text_offsets[i - 1]:
            break

    return log_prob / float(count) * SCORE_MULTIPLIER


def openai_search(query, documents, engine):
    prompts = [construct_prompt(query, doc) for doc in [""] + documents]

    resps = openai.Completion.create(
        model=engine,
        prompt=prompts,
        temperature=1.0,
        top_p=1.0,
        max_tokens=0,
        logprobs=0,
        n=1,
        echo=True,
    )

    resps_by_index = {choice["index"]: choice for choice in resps["choices"]}

    scores = [
        get_score(
            prompts[i],
            query,
            resps_by_index[i]["logprobs"]["token_logprobs"],
            resps_by_index[i]["logprobs"]["text_offset"],
        )
        for i in range(len(prompts))
    ]

    # Process results
    scores = [score - scores[0] for score in scores][1:]

    return [
        {
            "object": "search_result",
            "document": document_idx,
            "score": round(score, 3),
        }
        for document_idx, score in enumerate(scores)
    ]


def find_match(text_objs: List[NavigableString], query: str, model: str) -> List[NavigableString]:
    token = nbx.load_openai_token()
    if token != "":
        openai.api_key = token
    else:
        print("[Error] No openai token")
        return []

    # search
    MATCH_THRESHOLD_GPT3 = 200
    res = []
    search_results = openai_search(query, text_objs, model)
    for search_result in search_results:
        if search_result['score'] >= MATCH_THRESHOLD_GPT3:
            res.append(text_objs[search_result['document']])
    return res
