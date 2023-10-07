# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Methods specific to RAG_EVALUATION task type."""

import logging
from typing import Any, Dict, List, Optional, Callable, Iterator

from azureml.metrics import constants
from azureml.metrics.common import _scoring
from azureml.metrics.common.azureml_metrics import AzureMLMetrics

logger = logging.getLogger(__name__)


class AzureMLRagEvaluationMetrics(AzureMLMetrics):
    def __init__(self,
                 metrics: Optional[List[str]] = None,
                 rag_evaluation_params: Optional[dict] = None,
                 score_version: Optional[str] = "v1",
                 use_previous_conversation: Optional[bool] = False,
                 custom_dimensions: Optional[Dict[str, Any]] = None,
                 log_activity: Optional[Callable[[logging.Logger, str, Optional[str], Optional[Dict[str, Any]]],
                                                 Iterator[Optional[Any]]]] = None,
                 log_traceback: Optional[Callable[[BaseException, logging.Logger, Optional[str],
                                                   Optional[bool], Optional[Any]], None]] = None) -> None:
        """
        Given the references (groundtruth) and hypothesis (prediction),
        generate metrics for Text Generation task.

        :param metrics: RAG Evaluation Metrics to provide the score with the help of LLMs
        :param rag_evaluation_params: Dictionary containing credentials to initialize or setup LLM
        :param score_version: Version of rag evaluation metrics to be computed
        :param use_previous_conversation: boolean value to indicate if we need to use_previous_conversation
             for computing rag-evaluation metrics.
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
        self.metrics = metrics if metrics else constants.Metric.RAG_EVALUATION_SET

        self.rag_evaluation_params = rag_evaluation_params
        self.score_version = score_version
        self.use_previous_conversation = use_previous_conversation

        self.__custom_dimensions = custom_dimensions
        super().__init__(log_activity, log_traceback)

    def compute(self, y_test: List[Any], y_pred: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Compute all metrics for Chat completion task based on the config.

        :param y_test: Actual list of list of references
        :param y_pred: Actual list of predictions
        :return: Dict of computed metrics
        """
        scored_metrics = _scoring._score_rag_evaluation(
            self._log_activity,
            self._log_traceback,
            y_test,
            y_pred,
            self.metrics,
            self.rag_evaluation_params,
            self.score_version,
            self.use_previous_conversation
        )

        return scored_metrics

    @staticmethod
    def list_metrics():
        """Get the list of supported metrics.

            :return: List of supported metrics.
        """
        supported_metrics = constants.Metric.RAG_EVALUATION_SET
        return supported_metrics
