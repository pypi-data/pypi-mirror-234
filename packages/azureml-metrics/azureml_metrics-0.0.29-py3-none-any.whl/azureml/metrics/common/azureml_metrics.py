# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Methods specific to a Classification task type."""

import contextlib
import logging
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, Optional, Union, Iterator, Callable

from azureml.metrics.common import utilities
from azureml.metrics.constants import MetricExtrasConstants

logger = logging.getLogger(__name__)


class AzureMLMetrics(ABC):
    """Abstract class for AzureML metrics."""

    def __init__(self,
                 log_activity: Callable[[logging.Logger, str, Optional[str],
                                         Optional[Dict[str, Any]]], Iterator[Optional[Any]]],
                 log_traceback: Callable[[BaseException, logging.Logger, Optional[str],
                                          Optional[bool], Optional[Any]], None],
                 ):
        """
        Create the azuremlmetric base class.

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
            :param tb: The traceback to use for logging; if not provided, the one attached to the exception is used.
        """
        self._log_activity = log_activity if log_activity else default_log_activity
        self._log_traceback = log_traceback if log_traceback else default_log_traceback

    @abstractmethod
    def compute(self, y_test: Any,
                y_pred: Optional[Any] = None) -> Dict[str, Any]:
        """
        Compute all metrics for classification task based on the config.

        :param y_test: Actual label values
        :param y_pred: Predicted values
        :return: Dict of computed metrics
        """
        pass

    def merge_confidence_interval_metrics(self, scored_metrics: Dict[str, Any],
                                          scored_confidence_intervals: Dict[str, Any]):
        """
        Merge the regular and confidence interval scores.

        :param scored_metrics regular scores for the task
        :param scored_confidence_intervals confidence intervals.
        """
        scored_metrics = utilities.amalgamate_scalar_non_scalar(scored_metrics)
        scored_confidence_intervals = utilities.amalgamate_scalar_non_scalar(scored_confidence_intervals)
        joined_metrics = {}  # type: Dict[str, Any]
        for metric in scored_metrics.keys():

            computed_metric = scored_metrics[metric]
            joined_metrics[metric] = computed_metric

            if metric in scored_confidence_intervals:
                ci_metric = scored_confidence_intervals[metric]  # type: Dict[str, Any]
                ci_metric[MetricExtrasConstants.VALUE] = computed_metric
                joined_metrics[MetricExtrasConstants.MetricExtrasFormat.format(metric)] = ci_metric
        return utilities.segregate_scalar_non_scalar(joined_metrics)


@contextlib.contextmanager
def default_log_activity(
        logger: logging.Logger,
        activity_name: str,
        activity_type: Optional[str] = None,
        custom_dimensions: Optional[Dict[str, Any]] = None,
) -> Iterator[Optional[Any]]:
    """
    Log the activity status with duration.

    :param logger: logger
    :param activity_name: activity name
    :param activity_type: activity type
    :param custom_dimensions: custom dimensions
    """
    start_time = datetime.utcnow()
    activity_info = {"activity_name": activity_name, "activity_type": activity_type}  # type: Dict[str, Any]
    log_record = {"activity": activity_name, "type": activity_type, "dimesions": custom_dimensions}
    logger.info(f"activity: {activity_name}, type: {activity_type}, dimesions: {custom_dimensions}")
    completion_status = "SUCCESS"
    try:
        yield
    except Exception as e:
        completion_status = "FAILED"
        logger.error(str(e))
    finally:
        end_time = datetime.utcnow()
        duration_ms = round((end_time - start_time).total_seconds() * 1000, 2)
        activity_info["durationMs"] = duration_ms
        activity_info["completionStatus"] = completion_status

        logger.info(
            "ActivityCompleted: Activity={}, HowEnded={}, Duration={}[ms]".format(
                activity_name, completion_status, duration_ms
            ),
            extra={"properties": activity_info},
        )

    return log_record


def default_log_traceback(
        exception: BaseException,
        logger: Optional[Union[logging.Logger, logging.LoggerAdapter]],
        override_error_msg: Optional[str] = None,
        is_critical: Optional[bool] = True,
        tb: Optional[Any] = None,
) -> None:
    """
    Log exception traces.

    :param exception: The exception to log.
    :param logger: The logger to use.
    :param override_error_msg: The message to display that will override the current error_msg.
    :param is_critical: If is_critical, the logger will use log.critical, otherwise log.error.
    :param tb: The traceback to use for logging; if not provided, the one attached to the exception is used.
    """
    if override_error_msg is not None:
        error_msg = override_error_msg
    else:
        error_msg = str(exception)

    # Some exceptions may not have a __traceback__ attr
    traceback_obj = tb or exception.__traceback__ if hasattr(exception, "__traceback__") else None or sys.exc_info()[2]

    exception_class_name = exception.__class__.__name__

    # User can see original log message in their log file
    message = [
        "Class: {}".format(exception_class_name),
        "Message: {}".format(error_msg),
    ]

    if is_critical:
        logger.critical("\n".join(message))
    else:
        logger.error("\n".join(message))

    if traceback_obj is not None and hasattr(traceback_obj, "format_exc"):
        logger.debug(traceback_obj.format_exc())
