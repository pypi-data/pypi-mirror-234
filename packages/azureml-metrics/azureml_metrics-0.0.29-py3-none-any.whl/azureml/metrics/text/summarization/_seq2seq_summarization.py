# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Definitions for Machine Translation metrics."""
import importlib.util
from abc import abstractmethod
from typing import Any, List

from azureml.metrics.common._metric_base import Metric, ScalarMetric
from azureml.metrics.common.utilities import retry
from azureml.metrics import constants
from azureml.metrics.common.exceptions import MissingDependencies


class Seq2SeqSummarizationMetric(Metric):
    """Base class for Sequence to Sequence Translation metric"""

    def __init__(self,
                 y_test: List[Any],
                 y_pred: List[str],
                 metrics: List[str],
                 tokenizer: Any,
                 aggregator: bool,
                 stemmer: bool) -> None:
        """
        :param y_test: Tokenized References in the test set
        :param y_pred: Tokenized Hypothesis predicted by language model
        :param tokenizer: function that takes input a string, and returns a list of tokens
        :params aggregator: Boolean to indicate whether to aggregate scores
        :params stemmer: Boolean to indicate whether to use Porter stemmer for word suffixes
        """
        self.y_test = y_test
        self.y_pred = y_pred
        self.metrics = metrics
        self.tokenizer = tokenizer
        self.aggregator = aggregator
        self.stemmer = stemmer
        super().__init__()

    @abstractmethod
    def compute(self) -> Any:
        """Compute the score for the metric"""
        ...


class Rouge(Seq2SeqSummarizationMetric, ScalarMetric):
    """Wrapper class for Rouge metric for Sequence to Sequence NLG Tasks"""

    hf_rouge = None

    def compute(self) -> Any:
        """Compute the score for the metric."""
        self.load_rouge()
        rouge_args = {
            'rouge_types': self.metrics,
            'use_stemmer': self.stemmer,
            'use_aggregator': self.aggregator
        }
        if self.tokenizer:
            rouge_args.update({'tokenizer': self.tokenizer})
        return Rouge.hf_rouge.compute(predictions=self.y_pred, references=self.y_test,
                                      **rouge_args)

    @retry(max_attempts=constants.RetryConstants.MAX_ATTEMPTS,
           delay=constants.RetryConstants.DELAY_TIME)
    def load_rouge(self):
        try:
            import evaluate
            rougescore_spec = importlib.util.find_spec("rouge_score")

            if rougescore_spec is None:
                raise ImportError

        except ImportError:
            safe_message = "Text packages are not available. " \
                           "Please run pip install azureml-metrics[text]"
            raise MissingDependencies(
                safe_message, safe_message=safe_message
            )
        if Rouge.hf_rouge is None:
            Rouge.hf_rouge = evaluate.load("rouge")
