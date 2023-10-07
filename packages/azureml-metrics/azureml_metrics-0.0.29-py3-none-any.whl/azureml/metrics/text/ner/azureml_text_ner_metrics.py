# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Methods specific to a Text Named Entity Recognition task type."""

import logging
import numpy as np

from typing import Any, Dict, List, Optional, Callable, Iterator

from azureml.metrics import constants
from azureml.metrics.common import _scoring
from azureml.metrics.common.azureml_metrics import AzureMLMetrics


logger = logging.getLogger(__name__)


class AzureMLTextNERMetrics(AzureMLMetrics):
    """Class for AzureML text ner metrics."""

    def __init__(self,
                 metrics: Optional[List[str]] = None,
                 custom_dimensions: Optional[Dict[str, Any]] = None,
                 log_activity: Optional[Callable[[logging.Logger, str, Optional[str], Optional[Dict[str, Any]]],
                                                 Iterator[Optional[Any]]]] = None,
                 log_traceback: Optional[Callable[[BaseException, logging.Logger, Optional[str],
                                                   Optional[bool], Optional[Any]], None]] = None
                 ) -> None:
        """
        Given the scored data, generate metrics for classification task.

        :param label_list: unique labels list
        :param metrics: Classification metrics to compute point estimates
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
        self.metrics = metrics if metrics else constants.CLASSIFICATION_NLP_NER_SET
        self.__custom_dimensions = custom_dimensions
        super().__init__(log_activity, log_traceback)

    def compute(self, y_test: np.ndarray,
                y_pred: np.ndarray = None) -> Dict[str, Dict[str, Any]]:
        """
        Compute the metrics.

        :param y_test: Actual label values/label ids
        :param y_pred: Predicted values
        :return: Dict of computed metrics

        >>> from azureml.metrics import compute_metrics
        >>> y_true = [['O', 'O', 'O', 'B-MISC', 'I-MISC', 'I-MISC', 'O'], ['B-PER', 'I-PER', 'O']]
        >>> y_pred = [['O', 'O', 'B-MISC', 'I-MISC', 'I-MISC', 'I-MISC', 'O'], ['B-PER', 'I-PER', 'O']]
        >>> metrics_obj = compute_metrics(task_type="text-ner", y_test=y_true, y_pred=y_pred)
        """
        if isinstance(y_pred, str):
            prediction_str = y_pred
            y_pred = []
            predictions = prediction_str.split("\n\n")

            for prediction in predictions:
                prediction_label = prediction.split("\n")
                pred_labels = [token.split()[1] for token in prediction_label]
                y_pred.append(pred_labels)

        return _scoring._score_text_ner(
            log_activity=self._log_activity,
            log_traceback=self._log_traceback,
            y_test=y_test,
            y_pred=y_pred,
            metrics=self.metrics
        )

    @staticmethod
    def list_metrics():
        """Get the list of supported metrics.

            :return: List of supported metrics.
        """
        supported_metrics = constants.CLASSIFICATION_NLP_NER_SET
        return supported_metrics
