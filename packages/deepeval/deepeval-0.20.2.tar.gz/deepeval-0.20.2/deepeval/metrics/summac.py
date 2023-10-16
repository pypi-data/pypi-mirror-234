"""SummaC Factual Consistency Metric
"""
from typing import List
from deepeval.test_case import LLMTestCase
from deepeval.metrics.metric import Metric
from deepeval.singleton import Singleton


class SummaCFactualConsistency(Metric, metaclass=Singleton):
    def __init__(
        self,
        minimum_score: float = 0.3,
        models=["vitc"],
        bins="percentile",
        granularity="sentence",
        nli_labels="e",
        device="cpu",
        start_file="default",
        agg="mean",
    ):
        try:
            from summac.model_summac import SummaCConv, SummaCZS
            import nltk

            nltk.download("punkt")
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "Please install summac using `pip install summac`"
            )

        self.model_conv = SummaCConv(
            models=models,
            bins=bins,
            granularity=granularity,
            nli_labels=nli_labels,
            device=device,
            start_file=start_file,
            agg=agg,
        )
        self.model_conv.load_model()
        self.minimum_score = minimum_score

    def measure(self, test_case: LLMTestCase) -> float:
        score_conv1 = self.model_conv.score(
            test_case.context, [test_case.output]
        )
        score = score_conv1["scores"][0]
        self.success = score > self.minimum_score
        return score

    def is_successful(self):
        return self.success
