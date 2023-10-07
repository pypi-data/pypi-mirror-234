# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Methods specific to Sequence to Sequence Text generation task type."""

import logging
from typing import Any, Dict, List, Optional, Callable, Iterator

from azureml.metrics import constants
from azureml.metrics.common import _scoring
from azureml.metrics.common.azureml_metrics import AzureMLMetrics

logger = logging.getLogger(__name__)


class AzureMLTextGenerationMetrics(AzureMLMetrics):
    def __init__(self,
                 metrics: Optional[List[str]] = None,
                 tokenizer: Optional[Any] = None,
                 smoothing: Optional[bool] = False,
                 aggregator: Optional[bool] = True,
                 stemmer: Optional[bool] = False,
                 model_id: Optional[str] = "gpt2",
                 batch_size: Optional[int] = 16,
                 add_start_token: Optional[bool] = True,
                 custom_dimensions: Optional[Dict[str, Any]] = None,
                 log_activity: Optional[Callable[[logging.Logger, str, Optional[str], Optional[Dict[str, Any]]],
                                                 Iterator[Optional[Any]]]] = None,
                 log_traceback: Optional[Callable[[BaseException, logging.Logger, Optional[str],
                                                   Optional[bool], Optional[Any]], None]] = None) -> None:
        """
        Given the references (groundtruth) and hypothesis (prediction),
        generate metrics for Text Generation task.

        :param metrics: Rouge and Bleu-N metrics to compute point estimates
        :param tokenizer: function that can tokenize input data
        :params smoothing: Boolean to indicate whether to smooth out the bleu score
        :params aggregator: Boolean to indicate whether to aggregate scores
        :params stemmer: Boolean to indicate whether to use Porter stemmer for word suffixes
        :param model_id: model used for calculating Perplexity.
                         Perplexity can only be calculated for causal language models.
        :param batch_size (int): the batch size to run texts through the model. Defaults to 16.
        :param add_start_token (bool): whether to add the start token to the texts,
            so the perplexity can include the probability of the first word. Defaults to True.
        :param log_activity is a callback to log the activity with parameters
        :param log_activity is a callback to log the activity with parameters
            :param logger: logger
            :param activity_name: activity name
            :param activity_type: activity type
            :param custom_dimensions: custom dimensions
        :param log_traceback is a callback to log exception traces. with parameters
            :param exception: The exception to log.
            :param logger: The logger to use.
            :param override_error_msg: The message to display that will override the current error_msg.
            :param is_critical: If is_critical, the logger will use log.critical, otherwise log.error.
            :param tb: The traceback to use for logging; if not provided,
                        the one attached to the exception is used.
        :return: None
        """
        self.metrics = metrics if metrics else constants.Metric.TEXT_GENERATION_SET
        self.tokenizer = tokenizer
        self.smoothing = smoothing
        self.aggregator = aggregator
        self.stemmer = stemmer
        self.model_id = model_id
        self.batch_size = batch_size
        self.add_start_token = add_start_token
        self.__custom_dimensions = custom_dimensions
        super().__init__(log_activity, log_traceback)

    def compute(self, y_test: List[Any], y_pred: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Compute all metrics for Text Generation task based on the config.

        :param y_test: Actual list of list of references
        :param y_pred: Actual list of predictions
        :return: Dict of computed metrics
        """
        scored_metrics = _scoring._score_text_generation(
            self._log_activity,
            self._log_traceback,
            y_test,
            y_pred,
            self.metrics,
            self.tokenizer,
            self.smoothing,
            self.aggregator,
            self.stemmer,
            self.model_id,
            self.batch_size,
            self.add_start_token,
        )

        return scored_metrics

    @staticmethod
    def list_metrics():
        """Get the list of supported metrics.

            :return: List of supported metrics.
        """
        supported_metrics = constants.Metric.TEXT_GENERATION_SET
        return supported_metrics
