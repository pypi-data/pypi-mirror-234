# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Methods specific to Sequence to Sequence QA task type."""

import logging
from typing import Any, Dict, List, Optional, Callable, Iterator

from azureml.metrics import constants
from azureml.metrics.common import _scoring
from azureml.metrics.common.azureml_metrics import AzureMLMetrics

logger = logging.getLogger(__name__)


class QASplitTokenizer:
    def __call__(self, line):
        """Tokenizes an input line using split() on whitespace

        :param line: a segment to tokenize
        :return: the tokenized line
        """

        return line.split()


class AzureMLQAMetrics(AzureMLMetrics):
    def __init__(self,
                 metrics: Optional[List[str]] = None,
                 tokenizer: Optional[Any] = None,
                 regexes_to_ignore: Optional[List[str]] = None,
                 ignore_case: Optional[bool] = False,
                 ignore_punctuation: Optional[bool] = False,
                 ignore_numbers: Optional[bool] = False,
                 lang: Optional[str] = "en",
                 model_type: Optional[str] = None,
                 idf: Optional[bool] = False,
                 rescale_with_baseline: Optional[bool] = True,
                 questions: Optional[List[str]] = None,
                 contexts: Optional[List[str]] = None,
                 openai_api_batch_size: Optional[int] = 20,
                 openai_params: Optional[dict] = None,
                 use_chat_completion_api: Optional = None,
                 custom_dimensions: Optional[Dict[str, Any]] = None,
                 log_activity: Optional[Callable[[logging.Logger, str, Optional[str], Optional[Dict[str, Any]]],
                                                 Iterator[Optional[Any]]]] = None,
                 log_traceback: Optional[Callable[[BaseException, logging.Logger, Optional[str],
                                                   Optional[bool], Optional[Any]], None]] = None) -> None:
        """
        Given the references (groundtruth) and hypothesis (prediction),
        generate metrics for QA task.

        :param metrics: question answerng metrics to compute point estimates
        :param tokenizer: function that can tokenize input data
        :params regexes_to_ignore: List of string regular expressions to ignore
        :params ignore_case: Boolean to indicate whether to ignore case
        :params ignore_punctuation: Boolean to indicate whether to ignore punctuation
        :params ignore_numbers: Boolean to indicate whether to ignore numbers
        :params lang: String value to indicate the language of provided data.
        :param model_type: String to indicate the type of model while computing BERT score.
        :param idf: Boolean to indicate whether to use idf while computing BERT score.
        :param rescale_with_baseline: Boolean to indicate if we need to rescale BERT score.
        :param questions: Question used for the data sample used in computation of gpt-similarity metric.
        :param contexts: Context information used in Question Answering task for computing gpt-related metrics.
        :param openai_api_batch_size: number of prompts to be batched in one API call.
        :param openai_params: Dictionary containing credentials for openai API.
        :param use_chat_completion_api: boolean flag to choose between openAI completion vs chat completion API.
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
        self.metrics = metrics if metrics else constants.Metric.QA_SET
        self.tokenizer = tokenizer if tokenizer else QASplitTokenizer()
        self.regexes_to_ignore = regexes_to_ignore
        self.ignore_case = ignore_case
        self.ignore_punctuation = ignore_punctuation
        self.ignore_numbers = ignore_numbers
        self.lang = lang
        self.model_type = model_type
        self.idf = idf
        self.rescale_with_baseline = rescale_with_baseline
        self.questions = questions
        self.contexts = contexts
        self.openai_api_batch_size = openai_api_batch_size
        self.openai_params = openai_params
        self.use_chat_completion_api = use_chat_completion_api
        self.__custom_dimensions = custom_dimensions
        super().__init__(log_activity, log_traceback)

    def compute(self, y_test: List[Any], y_pred: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Compute all metrics for QA task based on the config.

        :param y_test: Actual list of list of references
        :param y_pred: Actual list of predictions
        :return: Dict of computed metrics
        """
        if self.openai_params is None:
            supported_metrics = set(self.metrics).difference(constants.Metric.QA_GPT_METRICS_SET)
            self.metrics = list(supported_metrics)
            logger.warning("GPT related metrics need openai_params to be computed. "
                           "Computing metrics for {}".format(self.metrics))

        scored_metrics = _scoring._score_qa(
            self._log_activity,
            self._log_traceback,
            y_test,
            y_pred,
            self.metrics,
            self.tokenizer,
            self.regexes_to_ignore,
            self.ignore_case,
            self.ignore_punctuation,
            self.ignore_numbers,
            self.lang,
            self.model_type,
            self.idf,
            self.rescale_with_baseline,
            self.questions,
            self.contexts,
            self.openai_api_batch_size,
            self.openai_params,
            self.use_chat_completion_api
        )

        return scored_metrics

    @staticmethod
    def list_metrics():
        """Get the list of supported metrics.

            :return: List of supported metrics.
        """
        supported_metrics = constants.Metric.QA_SET
        return supported_metrics
