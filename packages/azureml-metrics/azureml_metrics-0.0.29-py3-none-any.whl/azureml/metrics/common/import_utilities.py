# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utilities for importing required dependencies."""
from azureml.metrics.common.exceptions import MissingDependencies


def load_sklearn():
    try:
        import sklearn
        import sklearn.metrics
    except ImportError:
        safe_message = "Tabular packages are not available. " \
                       "Please run pip install azureml-metrics[tabular]"
        raise MissingDependencies(
            safe_message, safe_message=safe_message
        )
    return sklearn


def load_evaluate():
    try:
        import evaluate
    except ImportError:
        safe_message = "evaluate package is not available. Please run pip install azureml-metrics[evaluate]"
        raise MissingDependencies(
            safe_message, safe_message=safe_message
        )
    return evaluate


def load_similarity_utils():
    try:
        from azureml.metrics.text.qa import _similarity_utils

    except ImportError:
        safe_message = "Relevant GPT Star metrics packages are not available. " \
                       "Please run pip install azureml-metrics[prompt-flow]"
        raise MissingDependencies(
            safe_message, safe_message=safe_message
        )
    return _similarity_utils


def load_rag_evaluation_speaker():
    """imports the rag_evaluation speaker module"""
    try:
        from rag_evaluation.data_models.prompt_models import Speaker
    except ImportError:
        # TODO: update with azureml-metrics dependency for rag_evaluation
        #  when rag_evaluation package is available in public pypi
        safe_message = "rag_evaluation package is not available. " \
                       "Please run pip install rag_evaluation"
        raise MissingDependencies(
            safe_message, safe_message=safe_message
        )
    return Speaker


def load_rag_evaluation_helper_methods():
    try:
        from rag_evaluation.quality.llm_helpers import init_llm
        from rag_evaluation.quality.llm_metrics import LLMMetrics
    except ImportError:
        # TODO: update with azureml-metrics dependency for rag_evaluation
        #  when rag_evaluation package is available in public pypi
        safe_message = "rag_evaluation package is not available. " \
                       "Please run pip install rag_evaluation"
        raise MissingDependencies(
            safe_message, safe_message=safe_message
        )
    return init_llm, LLMMetrics
