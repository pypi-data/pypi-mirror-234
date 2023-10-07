# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
# Source for BERT Score: https://github.com/huggingface/evaluate/blob/main/metrics/bertscore/bertscore.py
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Definitions for Question/Answering metrics."""
import re
import string
import logging
import importlib.util
import numpy as np

from abc import abstractmethod
from collections import Counter
from typing import Any, List, Optional

from azureml.metrics.common._metric_base import Metric, ScalarMetric
from azureml.metrics import constants
from azureml.metrics.common.import_utilities import load_evaluate, load_similarity_utils
from azureml.metrics.common.utilities import retry
from azureml.metrics.common.exceptions import MissingDependencies


logger = logging.getLogger(__name__)


class Seq2SeqQAMetric(Metric):
    """Base class for Sequence to Sequence Question Answering metric"""

    def __init__(self,
                 y_test: List[Any],
                 y_pred: List[str],
                 tokenizer: Any,
                 regexes_to_ignore: List[str],
                 ignore_case: bool,
                 ignore_punctuation: bool,
                 ignore_numbers: bool,
                 lang: Optional[str] = "en",
                 model_type: Optional[str] = None,
                 idf: Optional[bool] = False,
                 rescale_with_baseline: Optional[bool] = True,
                 questions: Optional[List[str]] = None,
                 contexts: Optional[List[str]] = None,
                 openai_api_batch_size: Optional[int] = 20,
                 openai_params: Optional[dict] = None,
                 use_chat_completion_api: Optional = None,) -> None:
        """
        :param y_test: Tokenized References in the test set
        :param y_pred: Tokenized Hypothesis predicted by language model
        :param tokenizer: function that takes input a string, and returns a list of tokens
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
        :param openai_params: Dictionary contating credentials for openai API.
        :param use_chat_completion_api: boolean flag to choose between openAI completion vs chat completion API.
        """
        self.y_test = y_test
        self.y_pred = y_pred
        self.tokenizer = tokenizer
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
        super().__init__()

    @abstractmethod
    def compute(self) -> Any:
        """Compute the score for the metric"""
        ...

    """
    Function is same as normalize_answer(s) with name changed to normalize_text(self, text)
    Modified from
    https://github.com/huggingface/evaluate/blob/main/metrics/squad_v2/compute_score.py
    """

    def normalize_text(self, text) -> str:
        """Lower text and remove punctuation, articles and extra whitespace."""

        def remove_articles(text):
            return re.sub(r"\b(a|an|the)\b", " ", text)

        def white_space_fix(text):
            return " ".join(text.split())

        def remove_punc(text):
            exclude = set(string.punctuation)
            return "".join(ch for ch in text if ch not in exclude)

        def lower(text):
            return text.lower()

        return white_space_fix(remove_articles(remove_punc(lower(text))))

    def check_kwargs(self, metric_key: str) -> Any:
        """Compute the score for GPT Star metrics"""

        if metric_key in [constants.Metric.GPTGroundedness, constants.Metric.GPTRelevance]:
            if self.contexts is None:
                logger.warning("{} metric is not applicable as it needs question and context "
                               "for every example.".format(metric_key))
                return "nan"

        elif self.questions is None:
            logger.warning("{} metric is not applicable as it needs question "
                           "for every example.".format(metric_key))
            return "nan"

        # TODO : remove logit bias when we add explaination.
        # so that it returns values between 1 and 5
        if isinstance(self.openai_params, dict):
            self.openai_params["logit_bias"] = {16: 100, 17: 100, 18: 100, 19: 100, 20: 100}


class ExactMatch(Seq2SeqQAMetric, ScalarMetric):
    """ExactMatch metric for Sequence to Sequence Question Answering Tasks"""

    hf_exact_match = None

    def compute(self) -> Any:
        """Compute the score for ExactMatch metric"""
        # We will lazy load hf_exact_match to avoid loading it in non seg2seq tasks
        self.load_exact_match()

        exact_match_args = {
            "regexes_to_ignore": self.regexes_to_ignore,
            "ignore_case": self.ignore_case,
            "ignore_punctuation": self.ignore_punctuation,
            "ignore_numbers": self.ignore_numbers,
        }
        res = ExactMatch.hf_exact_match.compute(
            predictions=self.y_pred, references=self.y_test, **exact_match_args
        )
        return res["exact_match"]

    @retry(max_attempts=constants.RetryConstants.MAX_ATTEMPTS,
           delay=constants.RetryConstants.DELAY_TIME)
    def load_exact_match(self):
        evaluate = load_evaluate()
        if ExactMatch.hf_exact_match is None:
            ExactMatch.hf_exact_match = evaluate.load("exact_match")


class F1Score(Seq2SeqQAMetric, ScalarMetric):
    """F1 score metric for Sequence to Sequence Question Answering Tasks"""

    """
    Function is similar to compute_f1(a_gold, a_pred) with modifications
    Modified from
    https://github.com/huggingface/evaluate/blob/main/metrics/squad_v2/compute_score.py
    """

    def compute(self) -> Any:
        """Compute the score for F1 score metric"""

        f1_score_list = []
        for reference, prediction in zip(self.y_test, self.y_pred):

            prediction_tokens = self.normalize_text(prediction)
            reference_tokens = self.normalize_text(reference)
            prediction_tokens = self.tokenizer(prediction_tokens)
            reference_tokens = self.tokenizer(reference_tokens)

            common_tokens = Counter(prediction_tokens) & Counter(reference_tokens)
            num_common_tokens = sum(common_tokens.values())

            if num_common_tokens == 0:
                f1_score_list.append(0)
                continue

            precision = 1.0 * num_common_tokens / len(prediction_tokens)
            recall = 1.0 * num_common_tokens / len(reference_tokens)

            f1_score = (2 * precision * recall) / (precision + recall)

            f1_score_list.append(f1_score)

        return np.mean(f1_score_list)


class BERTScore(Seq2SeqQAMetric, ScalarMetric):
    """BERTScore metric for comparison of similarity between ground truths and predictions"""

    hf_bertscore = None

    def compute(self) -> Any:
        """Compute the score for BERT Score metric"""
        self.load_bertscore()

        if self.model_type is None:
            result = BERTScore.hf_bertscore.compute(predictions=self.y_pred, references=self.y_test,
                                                    lang=self.lang, idf=self.idf,
                                                    rescale_with_baseline=self.rescale_with_baseline)
        else:
            result = BERTScore.hf_bertscore.compute(predictions=self.y_pred, references=self.y_test,
                                                    lang=self.lang, model_type=self.model_type,
                                                    idf=self.idf,
                                                    rescale_with_baseline=self.rescale_with_baseline)
        return result

    @retry(max_attempts=constants.RetryConstants.MAX_ATTEMPTS,
           delay=constants.RetryConstants.DELAY_TIME)
    def load_bertscore(self):
        try:
            import evaluate
            bertscore_spec = importlib.util.find_spec("bert_score")
            torch_spec = importlib.util.find_spec("torch")
            transformers_spec = importlib.util.find_spec("transformers")

            if torch_spec is None or transformers_spec is None \
                    or bertscore_spec is None:
                raise ImportError

        except ImportError:
            safe_message = "bert-score packages are not available. " \
                           "Please run pip install azureml-metrics[bert-score]"

            raise MissingDependencies(
                safe_message, safe_message=safe_message
            )
        if BERTScore.hf_bertscore is None:
            BERTScore.hf_bertscore = evaluate.load("bertscore")


class GPTSimilarity(Seq2SeqQAMetric, ScalarMetric):
    """GPTSimilarity metric for comparison of similarity between ground truths and predictions"""

    def compute(self) -> Any:
        """Compute the score for GPT Similarity metric"""
        _similarity_utils = load_similarity_utils()
        if self.check_kwargs(constants.Metric.GPTSimilarity) == "nan":
            return ["not-applicable" for _ in range(len(self.y_pred))]

        prompt_list = []
        # validation for presence of y_test and y_pred happens in compute_metrics() method.
        for question, test, pred in zip(self.questions, self.y_test, self.y_pred):
            prompt = _similarity_utils.create_similarity_prompt(question, test, pred)
            prompt_list.append(prompt)

        results = _similarity_utils.get_prediction(prompt_list=prompt_list, openai_params=self.openai_params,
                                                   openai_api_batch_size=self.openai_api_batch_size,
                                                   use_chat_completion_api=self.use_chat_completion_api)

        logger.debug("gpt similarity results : {}".format(results))
        return results


class GPTCoherence(Seq2SeqQAMetric, ScalarMetric):
    """GPTCoherence metric for comparison of coherence between ground truths and predictions"""

    def compute(self) -> Any:
        """compute the score for GPTCoherence metric"""
        _similarity_utils = load_similarity_utils()
        if self.check_kwargs(constants.Metric.GPTCoherence) == "nan":
            return ["not-applicable" for _ in range(len(self.y_pred))]

        prompt_list = []

        for question, prediction in zip(self.questions, self.y_pred):
            prompt = _similarity_utils.create_coherence_prompt(question, prediction)
            prompt_list.append(prompt)

        results = _similarity_utils.get_prediction(prompt_list=prompt_list, openai_params=self.openai_params,
                                                   openai_api_batch_size=self.openai_api_batch_size,
                                                   use_chat_completion_api=self.use_chat_completion_api)

        logger.debug("gpt coherence results : {}".format(results))
        return results


class GPTRelevance(Seq2SeqQAMetric, ScalarMetric):
    """GPTRelevance metric for comparison of coherence between ground truths and predictions"""

    def compute(self) -> Any:
        """compute the score for GPTRelevance metric"""
        _similarity_utils = load_similarity_utils()
        if self.check_kwargs(constants.Metric.GPTRelevance) == "nan":
            return ["not-applicable" for _ in range(len(self.y_pred))]

        prompt_list = []

        for context, question, prediction in zip(self.contexts, self.questions, self.y_pred):
            prompt = _similarity_utils.create_relevance_prompt(context, question, prediction)
            prompt_list.append(prompt)

        results = _similarity_utils.get_prediction(prompt_list=prompt_list, openai_params=self.openai_params,
                                                   openai_api_batch_size=self.openai_api_batch_size,
                                                   use_chat_completion_api=self.use_chat_completion_api)
        logger.debug("gpt relevance results : {}".format(results))
        return results


class GPTFluency(Seq2SeqQAMetric, ScalarMetric):
    """GPTFluency metric for comparison of coherence between ground truths and predictions"""

    def compute(self) -> Any:
        """compute the score for GPTFluency metric"""
        _similarity_utils = load_similarity_utils()
        if self.check_kwargs(constants.Metric.GPTFluency) == "nan":
            return ["not-applicable" for _ in range(len(self.y_pred))]

        prompt_list = []

        for question, prediction in zip(self.questions, self.y_pred):
            prompt = _similarity_utils.create_fluency_prompt(question, prediction)
            prompt_list.append(prompt)

        results = _similarity_utils.get_prediction(prompt_list=prompt_list, openai_params=self.openai_params,
                                                   openai_api_batch_size=self.openai_api_batch_size,
                                                   use_chat_completion_api=self.use_chat_completion_api)
        logger.debug("gpt fluency results : {}".format(results))
        return results


class SquadV2(Seq2SeqQAMetric, ScalarMetric):
    """Squad_v2 metrics for Question Answering Tasks"""

    hf_squadv2 = None

    def compute(self) -> Any:
        """Compute score for Squad_v2 metrics"""
        # We will lazy load hf_squadv2 to avoid loading it in non seg2seq tasks
        self.load_squadv2()

        squad_v2_args = {"predictions": self.y_pred, "references": self.y_test}
        res = SquadV2.hf_squadv2.compute(
            predictions=self.y_pred, references=self.y_test, **squad_v2_args
        )

        return res

    @retry(max_attempts=constants.RetryConstants.MAX_ATTEMPTS,
           delay=constants.RetryConstants.DELAY_TIME)
    def load_squadv2(self):
        evaluate = load_evaluate()
        if SquadV2.hf_squadv2 is None:
            SquadV2.hf_squadv2 = evaluate.load("squad_v2")
