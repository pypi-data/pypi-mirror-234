"""Testing for SummaC
"""
from deepeval.metrics.summac import SummaCFactualConsistency
from deepeval.test_case import LLMTestCase
from deepeval.run_test import assert_test


def test_summac():
    query = "What if these shoes don't fit?"
    context = (
        "All customers are eligible for a 30 day full refund at no extra costs."
    )

    # Replace this with the actual output from your LLM application
    actual_output = "We offer a 30-day full refund at no extra costs."
    summac_metric = SummaCFactualConsistency(minimum_score=0.7)
    test_case = LLMTestCase(query=query, output=actual_output, context=context)
    assert_test(test_case, [summac_metric])
