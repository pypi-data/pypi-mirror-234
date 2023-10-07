# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Methods specific to Sequence to Sequence Translation task type."""

import logging
from typing import Any, Dict, List, Optional, Callable, Iterator

from azureml.metrics import constants
from azureml.metrics.common import _scoring
from azureml.metrics.common.azureml_metrics import AzureMLMetrics

logger = logging.getLogger(__name__)


class AzureMLTranslationMetrics(AzureMLMetrics):
    def __init__(self,
                 metrics: Optional[List[str]] = None,
                 tokenizer: Optional[Any] = None,
                 smoothing: Optional[bool] = False,
                 custom_dimensions: Optional[Dict[str, Any]] = None,
                 log_activity: Optional[Callable[[logging.Logger, str, Optional[str], Optional[Dict[str, Any]]],
                                                 Iterator[Optional[Any]]]] = None,
                 log_traceback: Optional[Callable[[BaseException, logging.Logger, Optional[str],
                                                   Optional[bool], Optional[Any]], None]] = None) -> None:
        """
        Given the references (groundtruth) and hypothesis (prediction),
        generate metrics for translation task.

        :param metrics: Bleu-N metrics to compute point estimates
        :param tokenizer: function that can tokenize input data
        :params smoothing: Boolean to indicate whether to smooth out the bleu score
        :param custom_dimensions to report the telemetry data.
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
        self.metrics = metrics if metrics else constants.Metric.TRANSLATION_SET
        self.tokenizer = tokenizer
        self.smoothing = smoothing
        self.__custom_dimensions = custom_dimensions
        super().__init__(log_activity, log_traceback)

    def compute(self, y_test: List[Any], y_pred: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Compute all metrics for translation task based on the config.

        :param y_test: Actual list of list of references (Bleu supports multiple references)
        :param y_pred: Actual list of predictions
        :return: Dict of computed metrics
        """
        scored_metrics = _scoring._score_translation(
            self._log_activity,
            self._log_traceback,
            y_test,
            y_pred,
            self.metrics,
            self.tokenizer,
            self.smoothing
        )

        return scored_metrics

    @staticmethod
    def list_metrics():
        """Get the list of supported metrics.

            :return: List of supported metrics.
        """
        supported_metrics = constants.Metric.TRANSLATION_SET
        return supported_metrics
