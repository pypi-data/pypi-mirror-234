# Measuring Faithfulness with You.com
import requests
from deepeval.metrics.summac import SummaCFactualConsistency

you_api_key = "cjjMpwCMr45hM0XxLMyc6aHmD0HRg5AH3gbWPvEm"


def get_ai_snippets_for_query(query: str):
    headers = {"X-API-Key": you_api_key}
    results = requests.get(
        f"https://api.ydc-index.io/search?query={query}",
        headers=headers,
    ).json()

    # We return many text snippets for each search hit so we need to explode both levels
    return ["\n".join(hit["snippets"]) for hit in results["hits"]]


snippets = get_ai_snippets_for_query("LlamaIndex started in 2018")
