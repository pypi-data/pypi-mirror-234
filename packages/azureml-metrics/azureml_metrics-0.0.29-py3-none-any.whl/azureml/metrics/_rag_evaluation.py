# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Definitions for RAG Evaluation metrics."""
import logging
import numpy as np

from abc import abstractmethod
from typing import Any, List

from azureml.metrics._metric_base import Metric, NonScalarMetric
from azureml.metrics import constants

logger = logging.getLogger(__name__)


def load_rag_evaluation_speaker():
    """imports the rag_evaluation speaker module"""
    try:
        from rag_evaluation.data_models.prompt_models import Speaker
    except ImportError:
        logger.error("rag_evaluation package is not installed. Please run pip install rag_evaluation")
        raise Exception()
    return Speaker


class RagEvaluationMetric(Metric):
    """Base class for RAG Evaluation metric"""

    def __init__(self,
                 y_test: List[Any],
                 y_pred: dict,
                 rag_evaluation_params: dict,
                 score_version: str,
                 use_previous_conversation: bool) -> None:
        """
        :param y_test: Tokenized References in the test set
        :param y_pred: Tokenized Hypothesis predicted by language model
        :param rag_evaluation_params: Dictionary containing credentials to initialize or setup LLM
        :param score_version: Version of rag evaluation metrics to be computed
        :param use_previous_conversation: boolean value to indicate if we need to use_previous_conversation
             for computing rag-evaluation metrics.
        """
        self.y_test = y_test
        self.y_pred = y_pred
        self.rag_evaluation_params = rag_evaluation_params
        self.score_version = score_version
        self.use_previous_conversation = use_previous_conversation
        super().__init__()

    @abstractmethod
    def compute(self) -> Any:
        """Compute the score for the metric"""
        ...

    @staticmethod
    def aggregate(
            scores: List[Any]
    ) -> float:
        """
        Fold several scores from a computed metric together. For now,
        it is a list of list of strings, but the inside list has len 1

        :param scores: List of List of str, response from openai
        :return: Aggregated score.
        """
        int_scores = []
        for score in scores:
            try:
                int_scores.append(int(score[0]))
            except ValueError:
                int_scores.append(np.nan)

        if np.isnan(int_scores).sum() == len(int_scores):
            logger.error("Score aggregation failed with all non-integer scores")
            return float(np.nan)
        return float(np.nanmean(int_scores))

    def init_config(self):
        """Set the basic config required to compute RAG Evaluation metrics"""
        try:
            from rag_evaluation.quality.llm_helpers import init_llm
            from rag_evaluation.quality.llm_metrics import LLMMetrics
        except ImportError:
            logger.error("rag_evaluation package is not installed. Please run pip install rag_evaluation")
            raise Exception()

        # TODO: add a validation for rag_evaluation_params
        evaluation_llm = init_llm(**self.rag_evaluation_params)
        rag_metrics = LLMMetrics(evaluation_llm)

        return rag_metrics


class GenerationScore(RagEvaluationMetric, NonScalarMetric):
    """GenerationScore metric for rag evaluation"""

    def compute(self) -> Any:
        """Compute the score for GenerationScore metric"""

        Speaker = load_rag_evaluation_speaker()

        rag_metrics = self.init_config()
        generation_score_dict = {constants.ChatCompletionConstants.SCORE_PER_TURN: [],
                                 constants.ChatCompletionConstants.SCORE_PER_CONVERSATION: [],
                                 constants.ChatCompletionConstants.REASON: []}

        # iterating over multiple conversations
        for conv_question, conv_model_result, conv_retrieved_documents, conv_ground_truth \
                in zip(self.y_pred["question"], self.y_pred["model_result"],
                       self.y_pred["retrieved_documents"], self.y_pred["ground_truth"]):

            # reset the history after one conversation
            rag_metrics.reset_conversation_history()

            generation_score_per_conversation = []
            generation_reason_per_conversation = []

            # iterating turn by turn over a single conversation
            for question, model_result, retrieved_documents, ground_truth in zip(conv_question,
                                                                                 conv_model_result,
                                                                                 conv_retrieved_documents,
                                                                                 conv_ground_truth):
                generation_score, generation_reason = rag_metrics.get_generation_score(question, retrieved_documents,
                                                                                       model_result, ground_truth,
                                                                                       version=self.score_version)

                generation_score_per_conversation.append(generation_score)
                generation_reason_per_conversation.append(generation_reason)

                if self.use_previous_conversation:
                    # add this turn to chat history
                    logger.debug("adding previous turns to conversation history")
                    rag_metrics.add_to_conversation_history({Speaker.USER.value: question,
                                                             Speaker.BOT.value: model_result})

            generation_score_dict["score_per_turn"].append(generation_score_per_conversation)
            generation_score_dict["score_per_conversation"].append(
                np.nanmean(generation_score_per_conversation))
            generation_score_dict["reason"].append(generation_reason_per_conversation)

        return generation_score_dict


class RetrievalScore(RagEvaluationMetric, NonScalarMetric):
    """RetrievalScore metric for rag evaluation"""

    def compute(self) -> Any:
        """Compute the score for RetrievalScore metric"""

        Speaker = load_rag_evaluation_speaker()

        rag_metrics = self.init_config()
        retrieval_score_dict = {constants.ChatCompletionConstants.SCORE_PER_TURN: [],
                                constants.ChatCompletionConstants.SCORE_PER_CONVERSATION: [],
                                constants.ChatCompletionConstants.REASON: []}

        # iterating over multiple conversations
        for conv_question, conv_model_result, conv_retrieved_documents \
                in zip(self.y_pred["question"], self.y_pred["model_result"],
                       self.y_pred["retrieved_documents"]):

            # reset the history after one conversation
            rag_metrics.reset_conversation_history()

            retrieval_score_per_conversation = []
            retrieval_reason_per_conversation = []

            # iterating turn by turn over a single conversation
            for question, model_result, retrieved_documents in zip(conv_question,
                                                                   conv_model_result,
                                                                   conv_retrieved_documents):
                retrieval_score, retrieval_reason = rag_metrics.get_retrieval_score(question, retrieved_documents,
                                                                                    version=self.score_version)

                retrieval_score_per_conversation.append(retrieval_score)
                retrieval_reason_per_conversation.append(retrieval_reason)

                if self.use_previous_conversation:
                    # add this turn to chat history
                    logger.debug("adding previous turns to conversation history")
                    rag_metrics.add_to_conversation_history({Speaker.USER.value: question,
                                                             Speaker.BOT.value: model_result})

            retrieval_score_dict["score_per_turn"].append(retrieval_score_per_conversation)
            retrieval_score_dict["score_per_conversation"].append(np.nanmean(retrieval_score_per_conversation))
            retrieval_score_dict["reason"].append(retrieval_reason_per_conversation)
        return retrieval_score_dict


class GroundingScore(RagEvaluationMetric, NonScalarMetric):
    """GroundingScore metric for rag evaluation"""

    def compute(self) -> Any:
        """Compute the score for GroundingScore metric"""

        Speaker = load_rag_evaluation_speaker()

        rag_metrics = self.init_config()
        grounding_score_dict = {constants.ChatCompletionConstants.SCORE_PER_TURN: [],
                                constants.ChatCompletionConstants.SCORE_PER_CONVERSATION: [],
                                constants.ChatCompletionConstants.REASON: []}

        # iterating over multiple conversations
        for conv_question, conv_model_result, conv_retrieved_documents \
                in zip(self.y_pred["question"], self.y_pred["model_result"],
                       self.y_pred["retrieved_documents"]):

            # reset the history after one conversation
            rag_metrics.reset_conversation_history()

            grounding_score_per_conversation = []
            grounding_reason_per_conversation = []

            # iterating turn by turn over a single conversation
            for question, model_result, retrieved_documents in zip(conv_question,
                                                                   conv_model_result,
                                                                   conv_retrieved_documents):
                grounding_score, grounding_reason = rag_metrics.get_grounding_score(question, retrieved_documents,
                                                                                    model_result,
                                                                                    version=self.score_version)

                grounding_score_per_conversation.append(grounding_score)
                grounding_reason_per_conversation.append(grounding_reason)

                if self.use_previous_conversation:
                    # add this turn to chat history
                    logger.debug("adding previous turns to conversation history")
                    rag_metrics.add_to_conversation_history({Speaker.USER.value: question,
                                                             Speaker.BOT.value: model_result})

            grounding_score_dict["score_per_turn"].append(grounding_score_per_conversation)
            grounding_score_dict["score_per_conversation"].append(np.nanmean(grounding_score_per_conversation))
            grounding_score_dict["reason"].append(grounding_reason_per_conversation)

        return grounding_score_dict
