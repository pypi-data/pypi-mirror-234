# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Computation of AzureML model evaluation metrics."""
import logging
import numpy as np
import pandas as pd

from azureml.metrics import _scoring_utilities, constants
from azureml.metrics.common import _validation, utilities
from azureml.metrics.tabular.forecasting._forecasting import _NormalizedRegressorWrapper
from azureml.metrics.common._metric_base import NonScalarMetric
from azureml.metrics.rai._utils import (parse_simulator_conversation_history,
                                        parse_simulator_context,
                                        parse_persona_name)
from azureml.metrics.constants import MetricExtrasConstants, Metric, ALL_TIME
from typing import Any, Callable, Dict, List, Iterator, Optional, Sequence, Tuple, Union


logger = logging.getLogger(__name__)


def _score_classification(
        log_activity: Callable[[logging.Logger, str, Optional[str],
                                Optional[Dict[str, Any]]], Iterator[Optional[Any]]],
        log_traceback: Callable[[BaseException, logging.Logger, Optional[str],
                                 Optional[bool], Optional[Any]], None],
        y_test: np.ndarray,
        y_pred: Optional[np.ndarray],
        y_pred_probs: Optional[np.ndarray],
        metrics: List[str],
        class_labels: np.ndarray,
        train_labels: np.ndarray,
        sample_weight: Optional[np.ndarray] = None,
        y_transformer: Optional = None,
        use_binary: bool = False,
        multilabel: Optional[bool] = False,
        positive_label: Optional[Any] = None,
        ensure_contiguous: bool = False
) -> Dict[str, Union[float, Dict[str, Any]]]:
    """
    Compute model evaluation metrics for a classification task.

    All class labels for y should come
    as seen by the fitted model (i.e. if the fitted model uses a y transformer the labels
    should also come transformed).

    All metrics present in `metrics` will be present in the output dictionary with either
    the value(s) calculated or `nan` if the calculation failed.

    :param y_test: The target values (Transformed if using a y transformer)
    :param y_pred: The predicted values (Transformed if using a y transformer)
    :param y_pred_probs: The predicted probabilities for all classes.
    :param metrics: Classification metrics to compute
    :param class_labels: All classes found in the full dataset (includes train/valid/test sets).
        These should be transformed if using a y transformer.
    :param train_labels: Classes as seen (trained on) by the trained model. These values
        should correspond to the columns of y_pred_probs in the correct order.
    :param sample_weight: Weights for the samples (Does not need
        to match sample weights on the fitted model)
    :param y_transformer: Used to inverse transform labels from `y_test`. Required for non-scalar metrics.
        y_transformer is of type sklearn.base.TransformerMixin
    :param use_binary: Compute metrics only on the true class for binary classification.
    :param positive_label: class designed as positive class in later binary classification metrics.
    :param multilabel: Indicate if it is multilabel classification.
    :param ensure_contiguous: Whether to pass contiguous NumPy arrays to the sklearn functions computing metrics.
    :return: A dictionary mapping metric name to metric score.
    """
    if not multilabel:
        y_test = _validation.format_1d(y_test, 'y_test')
        if y_pred is not None:
            y_pred = _validation.format_1d(y_pred, 'y_pred')

    _validation.validate_classification(y_test, y_pred, y_pred_probs, metrics,
                                        class_labels, train_labels,
                                        sample_weight, multilabel=multilabel)
    _validation.log_classification_debug(y_test, y_pred, y_pred_probs, class_labels,
                                         train_labels, sample_weight=sample_weight, multilabel=multilabel)

    scoring_dto = _scoring_utilities.ClassificationDataDto(y_test,
                                                           y_pred,
                                                           y_pred_probs,
                                                           class_labels,
                                                           train_labels,
                                                           sample_weight,
                                                           y_transformer,
                                                           multilabel=multilabel,
                                                           positive_label=positive_label)
    positive_label_encoded = scoring_dto.positive_label_encoded

    results = {}
    skipped_metrics = []
    computed_metrics = []
    for name in metrics:
        if y_pred_probs is None and name in Metric.CLASSIFICATION_PROB_REQUIRED_SET:
            skipped_metrics.append(name)
            continue
        try:
            metric_class = _scoring_utilities.get_metric_class(name)
            test_targets, pred_targets, labels, positive_label = scoring_dto.get_targets(
                encoded=utilities.is_scalar(name),
                classwise=utilities.is_classwise(name))

            metric = metric_class(
                test_targets, scoring_dto.y_pred_probs_padded, scoring_dto.y_test_bin,
                pred_targets, labels, sample_weight=sample_weight, use_binary=use_binary,
                positive_label_encoded=positive_label_encoded, multilabel=multilabel, y_transformer=y_transformer,
                ensure_contiguous=ensure_contiguous)

            results[name] = metric.compute()
            computed_metrics.append(name)
        except MemoryError:
            raise
        except Exception as e:
            safe_name = _scoring_utilities.get_safe_metric_name(name)
            logger.error("Scoring failed for classification metric {}".format(safe_name))
            log_traceback(e, logger, is_critical=False)
            if utilities.is_scalar(name):
                results[name] = np.nan
            else:
                results[name] = NonScalarMetric.get_error_metric()

    logger.info(f"Metrics computed:\n {computed_metrics}\n")

    if len(skipped_metrics) >= 1:
        logger.warning(f"Metrics skipped due to missing y_pred_proba:\n {skipped_metrics}")

    return utilities.segregate_scalar_non_scalar(results)


def _score_regression(
        log_activity: Callable[[logging.Logger, str, Optional[str],
                                Optional[Dict[str, Any]]], Iterator[Optional[Any]]],
        log_traceback: Callable[[BaseException, logging.Logger, Optional[str],
                                 Optional[bool], Optional[Any]], None],
        y_test: np.ndarray,
        y_pred: np.ndarray,
        metrics: List[str],
        y_max: Optional[float] = None,
        y_min: Optional[float] = None,
        y_std: Optional[float] = None,
        sample_weight: Optional[np.ndarray] = None,
        bin_info: Optional[Dict[str, float]] = None
) -> Dict[str, Union[float, Dict[str, Any]]]:
    """
    Compute model evaluation metrics for a regression task.

    The optional parameters `y_min`, `y_min`, and `y_min` should be based on the
        target column y from the full dataset.

    - `y_max` and `y_min` should be used to control the normalization of
    normalized metrics. The effect will be division by max - min.
    - `y_std` is used to estimate a sensible range for displaying non-scalar
    regression metrics.

    If the metric is undefined given the input data, the score will show
        as nan in the returned dictionary.

    :param y_test: The target values.
    :param y_pred: The predicted values.
    :param metrics: List of metric names for metrics to calculate.
    :type metrics: list
    :param y_max: The max target value.
    :param y_min: The min target value.
    :param y_std: The standard deviation of targets value.
    :param sample_weight:
        The sample weight to be used on metrics calculation. This does not need
        to match sample weights on the fitted model.
    :param bin_info:
        The binning information for true values. This should be calculated from make_dataset_bins. Required for
        calculating non-scalar metrics.
    :return: A dictionary mapping metric name to metric score.
    """
    # Lenient on shape of y_test and y_pred
    y_test = _validation.format_1d(y_test, 'y_test')
    y_test = _validation.convert_decimal_to_float(y_test)
    y_pred = _validation.format_1d(y_pred, 'y_pred')

    _validation.validate_regression(y_test, y_pred, metrics)
    _validation.log_regression_debug(y_test, y_pred, y_min, y_max, sample_weight=sample_weight)

    y_min = np.min(y_test) if y_min is None else y_min
    y_max = np.max(y_test) if y_max is None else y_max
    y_std = np.std(y_test) if y_std is None else y_std

    results = {}
    for name in metrics:
        safe_name = _scoring_utilities.get_safe_metric_name(name)
        try:
            metric_class = _scoring_utilities.get_metric_class(name)
            metric = metric_class(y_test, y_pred, y_min=y_min, y_max=y_max, y_std=y_std,
                                  bin_info=bin_info, sample_weight=sample_weight)
            results[name] = metric.compute()

            if utilities.is_scalar(name) and np.isinf(results[name]):
                logger.error("Found infinite regression score for {}, setting to nan".format(safe_name))
                results[name] = np.nan
        except MemoryError:
            raise
        except Exception as e:
            logger.error("Scoring failed for regression metric {}".format(safe_name))
            log_traceback(e, logger, is_critical=False)
            if utilities.is_scalar(name):
                results[name] = np.nan
            else:
                results[name] = NonScalarMetric.get_error_metric()

    return utilities.segregate_scalar_non_scalar(results)


def _score_forecasting(
        log_activity: Callable[[logging.Logger, str, Optional[str],
                                Optional[Dict[str, Any]]], Iterator[Optional[Any]]],
        log_traceback: Callable[[BaseException, logging.Logger, Optional[str],
                                 Optional[bool], Optional[Any]], None],
        y_test: np.ndarray,
        y_pred: np.ndarray,
        horizons: np.ndarray,
        X_test: pd.DataFrame,
        metrics: List[str],
        time_column_name: str,
        time_series_id_column_names: List[str],
        aggregation_method: Callable[[Sequence[float]], float] = np.mean,
        origin_column_name: Optional[str] = None,
        y_min_dict: Dict[Union[str, Tuple[str]], float] = None,
        y_max_dict: Dict[Union[str, Tuple[str]], float] = None,
        y_std: Optional[float] = None,
        sample_weight: Optional[np.ndarray] = None,
        X_train: Optional[pd.DataFrame] = None,
        y_train: Optional[np.ndarray] = None,
) -> Dict[str, Union[float, Dict[str, Any]]]:
    """
    Compute model evaluation metrics for a forecasting task.

    The optional parameters `y_min`, `y_min`, and `y_min` should be based on the
        target column y from the full dataset.

    - `y_max` and `y_min` should be used to control the normalization of
    normalized metrics. The effect will be division by max - min.
    - `y_std` is used to estimate a sensible range for displaying non-scalar
    regression metrics.

    If the metric is undefined given the input data, the score will show
        as nan in the returned dictionary.

    :param log_activity is a callback to log the activity with parameters
    :param log_traceback is a callback to log exception traces. with parameters
    :param y_test: The target values.
    :param y_pred: The predicted values.
    :param horizons: The integer horizon aligned to each y_test. These values should be computed
            by the timeseries transformer. If the timeseries transformer does not compute a horizon,
            ensure all values are the same (ie. every y_test should be horizon 1.)
    :param metrics: List of metric names for metrics to calculate.
    :param time_column_name: The time column name.
    :param time_series_id_column_names: The time series id column names also known as
                                        grain column names.
    :param origin_column_name: The origin time column name.
    :param y_min_dict: The dictionary, with minimum target values per time series ID, time series ID
                       is used as a key.
    :param y_max_dict: The dictionary, with maximum target values per time series ID, time series ID
                       is used as a key.
    :param sample_weight:
        The sample weight to be used on metrics calculation. This does not need
        to match sample weights on the fitted model.
    :param X_train: The inputs which were used to train the model.
    :param y_train: The targets which were used to train the model.
    :param aggregation_method: The function used to aggregate by grain metrics.
    :return: A dictionary mapping metric name to metric score.
    """
    # Lenient on shape of y_test and y_pred
    y_test = _validation.format_1d(y_test, 'y_test')
    y_test = _validation.convert_decimal_to_float(y_test)
    y_pred = _validation.format_1d(y_pred, 'y_pred')
    if y_train is not None:
        y_train = _validation.format_1d(y_train, 'y_train')
        y_train = _validation.convert_decimal_to_float(y_train)

    _validation.validate_forecasting(y_test, y_pred, metrics)

    if y_min_dict is None:
        y_min_dict = {}
    if y_max_dict is None:
        y_max_dict = {}
    y_min = np.min(y_test) if not y_min_dict else np.min(list(y_min_dict.values()))
    y_max = np.max(y_test) if not y_max_dict else np.max(list(y_max_dict.values()))
    _validation.log_forecasting_debug(y_test, y_pred, y_min, y_max, sample_weight=sample_weight)

    y_std = np.std(y_test) if y_std is None else y_std

    results = {}
    for name in metrics:
        safe_name = _scoring_utilities.get_safe_metric_name(name)
        try:
            metric_class = _scoring_utilities.get_metric_class(name)
            if name in constants.FORECASTING_NONSCALAR_SET:
                metric = metric_class(
                    y_test=y_test,
                    y_pred=y_pred,
                    horizons=horizons,
                    y_min=y_min,
                    y_max=y_max,
                    y_std=y_std,
                    sample_weight=sample_weight,
                    X_test=X_test,
                    X_train=X_train,
                    y_train=y_train,
                    time_series_id_column_names=time_series_id_column_names,
                    time_column_name=time_column_name,
                    origin_column_name=origin_column_name,
                    y_min_dict=y_min_dict,
                    y_max_dict=y_max_dict
                )
            elif name in constants.REGRESSION_NORMALIZED_SET:
                # Calculate the metrics by grain/time_series_id.
                metric = _NormalizedRegressorWrapper(
                    y_test=y_test,
                    y_pred=y_pred,
                    horizons=horizons,
                    y_min_dict=y_min_dict,
                    y_max_dict=y_max_dict,
                    sample_weight=sample_weight,
                    X_test=X_test,
                    time_series_id_column_names=time_series_id_column_names,
                    time_column_name=time_column_name,
                    metric_class=metric_class,
                    aggregation_function=aggregation_method)
            else:
                # Other regression metrics, which do not require normalization.
                metric = metric_class(y_test, y_pred, y_min=y_min, y_max=y_max, y_std=y_std,
                                      sample_weight=sample_weight)
            results[name] = metric.compute()

            if utilities.is_scalar(name) and np.isinf(results[name]):
                logger.error("Found infinite forecasting score for {}, setting to nan".format(safe_name))
                results[name] = np.nan
        except MemoryError:
            raise
        except Exception as e:
            logger.error("Scoring failed for forecasting metric {}".format(safe_name))
            log_traceback(e, logger, is_critical=False)
            if utilities.is_scalar(name):
                results[name] = np.nan
            else:
                results[name] = NonScalarMetric.get_error_metric()

    return utilities.segregate_scalar_non_scalar(results)


def _score_text_ner(
        log_activity: Callable[[logging.Logger, str, Optional[str],
                                Optional[Dict[str, Any]]], Iterator[Optional[Any]]],
        log_traceback: Callable[[BaseException, logging.Logger, Optional[str],
                                 Optional[bool], Optional[Any]], None],
        y_test: Union[List[List[str]], np.ndarray],
        y_pred: Union[List[List[str]], np.ndarray],
        metrics: List[str]
) -> Dict[str, Union[float, Dict[str, Any]]]:
    # We are using seqeval to calculate metrics instead of sklearn for other classification problem
    # because seqeval supports evaluation at entity-level

    _validation.validate_ner(y_test, y_pred, metrics)
    _validation.log_ner_debug(y_test, y_pred)

    results = {}
    for name in metrics:
        if name in constants.CLASSIFICATION_NLP_NER_SET:
            try:
                metric_class = _scoring_utilities.get_metric_class_text_ner(name)
                metric = metric_class(y_test, y_pred)
                results[name] = metric.compute()
            except MemoryError:
                raise
            except Exception as e:
                safe_name = _scoring_utilities.get_safe_metric_name(name)
                logger.error("Scoring failed for NER metric {}".format(safe_name))
                log_traceback(e, logger, is_critical=False)
                if utilities.is_scalar(name):
                    results[name] = np.nan
                else:
                    results[name] = NonScalarMetric.get_error_metric()
    return utilities.segregate_scalar_non_scalar(results)


def _score_translation(
        log_activity: Callable[[logging.Logger, str, Optional[str],
                                Optional[Dict[str, Any]]], Iterator[Optional[Any]]],
        log_traceback: Callable[[BaseException, logging.Logger, Optional[str],
                                 Optional[bool], Optional[Any]], None],
        y_test: List[Any],
        y_pred: List[str],
        metrics: List[str],
        tokenizer: Any,
        smoothing: bool):
    """
    Compute model evaluation metrics for a translation task.

    y_test should be a list of list of string references (even if there is only one reference)
    y_pred should be a list of string predictions
    tokenizer could be any function that takes input a string, and returns a list of tokens

    :param y_test: Actual list of list of references
    :param y_pred: Actual list of predictions
    :param metrics: List of metric names for metrics to calculate.
    :param tokenizer: function that takes input a string, and returns a list of tokens
    :param smoothing: boolean to indicate if smoothing is required for bleu score
    """
    _validation.validate_translation(y_test, y_pred, metrics, tokenizer, smoothing)
    _validation.log_translation_debug(y_test, y_pred, tokenizer, smoothing)

    results = {}
    for name in metrics:
        safe_name = _scoring_utilities.get_safe_metric_name(name)
        max_ngram = constants.Metric.TRANSLATION_NGRAM_MAP[name]
        try:
            metric_class = _scoring_utilities.get_metric_class(name)
            metric = metric_class(y_test, y_pred, tokenizer, max_ngram, smoothing)
            results[name] = metric.compute()
        except MemoryError:
            raise
        except Exception as e:
            logger.error("Scoring failed for translation metric {}".format(safe_name))
            log_traceback(e, logger, is_critical=False)
            results[name] = np.nan
    return utilities.segregate_scalar_non_scalar(results)


def _score_summarization(
        log_activity: Callable[[logging.Logger, str, Optional[str],
                                Optional[Dict[str, Any]]], Iterator[Optional[Any]]],
        log_traceback: Callable[[BaseException, logging.Logger, Optional[str],
                                 Optional[bool], Optional[Any]], None],
        y_test: List[Any],
        y_pred: List[str],
        metrics: List[str],
        tokenizer: Any,
        aggregator: bool,
        stemmer: bool):
    """
    Compute model evaluation metrics for a summarization task.

    y_test should be a list of string references
    y_pred should be a list of string predictions
    tokenizer could be any function that takes input a string, and returns a list of tokens

    :param y_test: Actual list of list of references
    :param y_pred: Actual list of predictions
    :param metrics: List of metric names for metrics to calculate.
    :param tokenizer: function that takes input a string, and returns a list of tokens
    :params aggregator: Boolean to indicate whether to aggregate scores
    :params stemmer: Boolean to indicate whether to use Porter stemmer for word suffixes
    """
    _validation.validate_summarization(y_test, y_pred, metrics, tokenizer, aggregator, stemmer)
    _validation.log_summarization_debug(y_test, y_pred, tokenizer, aggregator, stemmer)

    results = {}
    safe_names = []
    for name in metrics:
        safe_names.append(_scoring_utilities.get_safe_metric_name(name))
    safe_names = ', '.join(safe_names)

    try:
        # NOTE: This will only work if all metrics are Rouge for summarization
        metric_class = _scoring_utilities.get_metric_class(list(metrics)[0])
        metric = metric_class(y_test, y_pred, metrics, tokenizer, aggregator, stemmer)
        results = metric.compute()
    except MemoryError:
        raise
    except Exception as e:
        logger.error("Scoring failed for summarization metrics {}".format(safe_names))
        log_traceback(e, logger, is_critical=False)
        for name in metrics:
            results[name] = np.nan
    return utilities.segregate_scalar_non_scalar(results)


def _score_text_generation(
        log_activity: Callable[[logging.Logger, str, Optional[str],
                                Optional[Dict[str, Any]]], Iterator[Optional[Any]]],
        log_traceback: Callable[[BaseException, logging.Logger, Optional[str],
                                 Optional[bool], Optional[Any]], None],
        y_test: List[Any],
        y_pred: List[str],
        metrics: List[str],
        tokenizer: Any,
        smoothing: bool,
        aggregator: bool,
        stemmer: bool,
        model_id: Optional[str],
        batch_size: Optional[int],
        add_start_token: Optional[bool],):
    """
    Compute model evaluation metrics for a text generation task.

    y_test should be a list of list of string references
    y_pred should be a list of string predictions
    tokenizer could be any function that takes input a string, and returns a list of tokens

    :param y_test: Actual list of list of references
    :param y_pred: Actual list of predictions
    :param metrics: List of metric names for metrics to calculate.
    :param tokenizer: function that takes input a string, and returns a list of tokens
    :params smoothing: Boolean to indicate whether to smooth out the bleu score
    :params aggregator: Boolean to indicate whether to aggregate scores
    :params stemmer: Boolean to indicate whether to use Porter stemmer for word suffixes
    :param model_id: model used for calculating Perplexity.
                        Perplexity can only be calculated for causal language models.
    :param batch_size (int): the batch size to run texts through the model. Defaults to 16.
    :param add_start_token (bool): whether to add the start token to the texts,
        so the perplexity can include the probability of the first word. Defaults to True.
    """
    _validation.validate_text_generation(y_test, y_pred, metrics, tokenizer,
                                         smoothing, aggregator, stemmer,
                                         model_id, batch_size, add_start_token)
    _validation.log_text_generation_debug(y_test, y_pred, tokenizer,
                                          smoothing, aggregator, stemmer,
                                          model_id, batch_size, add_start_token)

    results = {}
    for name in metrics:
        safe_name = _scoring_utilities.get_safe_metric_name(name)
        max_ngram = constants.Metric.TRANSLATION_NGRAM_MAP.get(name, None)
        try:
            metric_class = _scoring_utilities.get_metric_class(name)
            if max_ngram is not None:
                metric = metric_class(y_test, y_pred, tokenizer, max_ngram, smoothing)
            elif name in constants.FILL_MASK_NONSCALAR_SET:
                metric = metric_class(y_test, y_pred, model_id,
                                      batch_size, add_start_token)
            else:
                metric = metric_class(y_test, y_pred, [name], tokenizer, aggregator, stemmer)
            computed_result = metric.compute()
            results[name] = computed_result.get(name, None) \
                if isinstance(computed_result, dict) else computed_result
        except MemoryError:
            raise
        except Exception as e:
            logger.error("Scoring failed for text generation metric {}".format(safe_name))
            log_traceback(e, logger, is_critical=False)
            results[name] = np.nan
    return utilities.segregate_scalar_non_scalar(results)


def _score_code_generation(
        log_activity: Callable[[logging.Logger, str, Optional[str],
                                Optional[Dict[str, Any]]], Iterator[Optional[Any]]],
        log_traceback: Callable[[BaseException, logging.Logger, Optional[str],
                                 Optional[bool], Optional[Any]], None],
        y_test: List[Any],
        y_pred: List[Any],
        metrics: List[str],
        test_cases: List[str],
        allow_code_eval: Optional[bool],
        no_of_candidates: Optional[List[int]],
        num_workers: Optional[int],
        timeout: Optional[Any],
        tokenizer: Any,
        smoothing: bool,
        aggregator: bool,
        stemmer: bool,):
    """
    Compute model evaluation metrics for a code generation task.

    :param y_test: Actual list of test cases
    :param y_pred: list of list of predictions or code candidates
            generated by model.
    :param metrics: pass@k metric to be computed for code generation task
    :param test_cases: list of strings which contains the assertion or test case statements.
    :param allow_code_eval: Boolean to indicate whether to execute untrusted model generated code
    :param no_of_candidates: number of code candidates to consider in the evaluation.
    :param num_workers: number of workers used to evaluate the candidate programs
    :param timeout: The maximum time taken to produce a prediction before it is considered a “timeout”.
    :param tokenizer: function that can tokenize input data
    :params smoothing: Boolean to indicate whether to smooth out the bleu score
    :params aggregator: Boolean to indicate whether to aggregate scores
    :params stemmer: Boolean to indicate whether to use Porter stemmer for word suffixes
    """
    _validation.validate_code_generation(y_test, y_pred, metrics, test_cases,
                                         allow_code_eval, no_of_candidates,
                                         num_workers, timeout, tokenizer,
                                         smoothing, aggregator, stemmer)
    _validation.log_code_generation_debug(y_test, y_pred, metrics, test_cases,
                                          allow_code_eval, no_of_candidates,
                                          num_workers, timeout, tokenizer,
                                          smoothing, aggregator, stemmer)
    logger.warning("using only first prediction for every data sample as "
                   "bleu or rouge metrics doesn't support multiple predictions")
    processed_y_pred = [pred_sample[0] for pred_sample in y_pred]
    results = {}
    for name in metrics:
        safe_name = _scoring_utilities.get_safe_metric_name(name)
        max_ngram = constants.Metric.TRANSLATION_NGRAM_MAP.get(name, None)
        try:
            metric_class = _scoring_utilities.get_metric_class(name)
            if max_ngram is not None:
                metric = metric_class(y_test, processed_y_pred, tokenizer, max_ngram, smoothing)
            elif name in constants.Metric.SUMMARIZATION_SET:
                metric = metric_class(y_test, processed_y_pred, [name], tokenizer, aggregator, stemmer)
            else:
                metric = metric_class(y_test, y_pred, test_cases, allow_code_eval,
                                      no_of_candidates, num_workers, timeout)
            computed_result = metric.compute()

            if name is constants.Metric.CodeGenerationPassRateScore:
                results.update(computed_result)
            else:
                results[name] = computed_result.get(name, None) \
                    if isinstance(computed_result, dict) else computed_result
        except MemoryError:
            raise
        except Exception as e:
            logger.error("Scoring failed for Code generation metric {}".format(safe_name))
            log_traceback(e, logger, is_critical=False)
            results[name] = np.nan
    return utilities.segregate_scalar_non_scalar(results)


def _score_chat_completion(
        log_activity: Callable[[logging.Logger, str, Optional[str],
                                Optional[Dict[str, Any]]], Iterator[Optional[Any]]],
        log_traceback: Callable[[BaseException, logging.Logger, Optional[str],
                                 Optional[bool], Optional[Any]], None],
        y_test: List[Any],
        y_pred: List[Any],
        metrics: List[str],
        tokenizer: Any,
        smoothing: bool,
        aggregator: bool,
        stemmer: bool,
        model_id: Optional[str],
        batch_size: Optional[int],
        add_start_token: Optional[bool],
        openai_params: Optional[dict] = None):
    """
    Compute model evaluation metrics for a chat completion task.

    y_test should be a list of list of string references
    y_pred should be a list of string predictions
    tokenizer could be any function that takes input a string, and returns a list of tokens

    :param y_test: Actual list of list of references
    :param y_pred: Actual list of predictions
    :param metrics: List of metric names for metrics to calculate.
    :param tokenizer: function that takes input a string, and returns a list of tokens
    :params smoothing: Boolean to indicate whether to smooth out the bleu score
    :params aggregator: Boolean to indicate whether to aggregate scores
    :params stemmer: Boolean to indicate whether to use Porter stemmer for word suffixes
    :param model_id: model used for calculating Perplexity.
                        Perplexity can only be calculated for causal language models.
    :param batch_size (int): the batch size to run texts through the model. Defaults to 16.
    :param add_start_token (bool): whether to add the start token to the texts,
        so the perplexity can include the probability of the first word. Defaults to True.
    """
    # TODO: add validation for input contract of chat completion task
    _validation.validate_chat_completion(y_test, y_pred, metrics, tokenizer,
                                         smoothing, aggregator, stemmer,
                                         model_id, batch_size, add_start_token)
    _validation.log_chat_completion_debug(y_test, y_pred, tokenizer,
                                          smoothing, aggregator, stemmer,
                                          model_id, batch_size, add_start_token)

    processed_y_test = {"y_test": []}
    processed_y_pred = {"y_pred": []}

    processed_conversation_history = []
    processed_context = []
    processed_persona_name = []

    try:
        if y_test is not None:
            for conversation_num, each_conversation in enumerate(y_test):
                for turn_num, each_turn in enumerate(each_conversation):
                    persona = each_turn["role"]
                    if persona == "user":
                        continue

                    test_sample = each_turn["content"]
                    processed_y_test["y_test"].append([test_sample])

        for conversation_num, each_conversation in enumerate(y_pred):
            for turn_num, each_turn in enumerate(each_conversation):
                persona = each_turn["role"]
                if persona == "user":
                    continue

                test_sample = each_turn["content"]
                processed_y_pred["y_pred"].append(test_sample)
    except Exception:
        try:
            # if not llama format, check it's dictionary with conversation simulator format
            processed_conversation_history = [parse_simulator_conversation_history(conversation)
                                              for conversation in y_pred]
            processed_context = [parse_simulator_context(conversation) for conversation in y_pred]
            processed_persona_name = [parse_persona_name(conversation) for conversation in y_pred]
        except Exception:
            raise Exception("Invalid input format for chat completion task")

    results = {}
    for name in metrics:
        safe_name = _scoring_utilities.get_safe_metric_name(name)
        max_ngram = constants.Metric.TRANSLATION_NGRAM_MAP.get(name, None)
        try:
            metric_class = _scoring_utilities.get_metric_class(name)

            if name == Metric.ConversationGroundingScore:
                if openai_params is None:
                    raise ValueError("OpenAI parameters are required for ConversationGroundingScore")
                else:
                    metric = metric_class(processed_conversation_history,
                                          tokenizer, processed_context, processed_persona_name, openai_params)
            elif max_ngram is not None:
                metric = metric_class(processed_y_test["y_test"],
                                      processed_y_pred["y_pred"], tokenizer, max_ngram, smoothing)
            elif name in constants.FILL_MASK_NONSCALAR_SET:
                metric = metric_class(y_test, processed_y_pred["y_pred"],
                                      model_id, batch_size,
                                      add_start_token)
            else:
                metric = metric_class(processed_y_test["y_test"],
                                      processed_y_pred["y_pred"],
                                      [name], tokenizer, aggregator, stemmer)

            computed_result = metric.compute()
            results[name] = computed_result.get(name, None) \
                if isinstance(computed_result, dict) else computed_result

        except MemoryError:
            raise
        except Exception as e:
            logger.error("Scoring failed for chat completion metric {}".format(safe_name))
            log_traceback(e, logger, is_critical=False)
            results[name] = np.nan
    return utilities.segregate_scalar_non_scalar(results)


def _score_rag_evaluation(
        log_activity: Callable[[logging.Logger, str, Optional[str],
                                Optional[Dict[str, Any]]], Iterator[Optional[Any]]],
        log_traceback: Callable[[BaseException, logging.Logger, Optional[str],
                                 Optional[bool], Optional[Any]], None],
        y_test: List[Any],
        y_pred: List[str],
        metrics: List[str],
        rag_evaluation_params: dict,
        score_version: str,
        use_previous_conversation: bool):
    """
    Compute model evaluation metrics for a rag evaluation task.

    y_test, y_pred represent multi-turn conversations

    :param metrics: RAG Evaluation Metrics to provide the score with the help of LLMs
    :param rag_evaluation_params: Dictionary containing credentials to initialize or setup LLM
    :param score_version: Version of rag evaluation metrics to be computed.
    :param use_previous_conversation: boolean value to indicate if we need to use_previous_conversation
             for computing rag-evaluation metrics.
    """
    CONVERSATION_NUM = constants.ChatCompletionConstants.CONVERSATION_NUMBER
    TURN_NUM = constants.ChatCompletionConstants.TURN_NUMBER
    # TODO: add validation for y_test by adding ground truth as input
    _validation.validate_rag_evaluation(y_test, y_pred, metrics, rag_evaluation_params,
                                        score_version, use_previous_conversation)
    # _validation.log_chat_completion_debug(y_test, y_pred, tokenizer,
    #                                       smoothing, aggregator, stemmer)

    processed_y_pred = {"question": [],
                        "model_result": [],
                        "retrieved_documents": [],
                        "ground_truth": [],
                        "conversation_num": [],
                        "turn_num": []}

    for conversation_num, each_conversation in enumerate(y_pred):

        questions_per_conversation = []
        model_result_per_conversation = []
        retrieved_documents_per_conversation = []
        ground_truth_per_conversation = []
        conversation_num_per_conversation = []
        turn_num_per_conversation = []

        for turn_num, each_turn in enumerate(each_conversation):
            question = each_turn["user"]["content"]
            model_result = each_turn["assistant"]["content"]
            retrieved_documents = each_turn["retrieved_documents"]

            # Check if we need to take the input of ground_truth seperately
            ground_truth = ""

            questions_per_conversation.append(question)
            model_result_per_conversation.append(model_result)
            retrieved_documents_per_conversation.append(retrieved_documents)
            ground_truth_per_conversation.append(ground_truth)
            conversation_num_per_conversation.append(conversation_num)
            turn_num_per_conversation.append(turn_num)

        processed_y_pred["question"].append(questions_per_conversation)
        processed_y_pred["model_result"].append(model_result_per_conversation)
        processed_y_pred["retrieved_documents"].append(retrieved_documents_per_conversation)
        processed_y_pred["ground_truth"].append(ground_truth_per_conversation)
        processed_y_pred["conversation_num"].append(conversation_num_per_conversation)
        processed_y_pred["turn_num"].append(turn_num_per_conversation)

    results = {}
    for name in metrics:
        safe_name = _scoring_utilities.get_safe_metric_name(name)

        try:
            metric_class = _scoring_utilities.get_metric_class(name)
            metric = metric_class(y_test, processed_y_pred, rag_evaluation_params,
                                  score_version, use_previous_conversation)
            computed_result = metric.compute()

            # results[name] = computed_result.get(name, None) \
            #     if isinstance(computed_result, dict) else computed_result

            results[name] = computed_result

        except MemoryError:
            raise
        except Exception as e:
            logger.error("Scoring failed for rag evaluation metric {}".format(safe_name))
            log_traceback(e, logger, is_critical=False)
            results[name] = np.nan

    results[CONVERSATION_NUM] = processed_y_pred["conversation_num"]
    results[TURN_NUM] = processed_y_pred["turn_num"]
    return utilities.segregate_scalar_non_scalar(results)


def _score_qa(
        log_activity: Callable[[logging.Logger, str, Optional[str],
                                Optional[Dict[str, Any]]], Iterator[Optional[Any]]],
        log_traceback: Callable[[BaseException, logging.Logger, Optional[str],
                                 Optional[bool], Optional[Any]], None],
        y_test: List[Any],
        y_pred: List[str],
        metrics: List[str],
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
        use_chat_completion_api: Optional = None):
    """
    Compute model evaluation metrics for a QA task.

    y_test should be a list of string references
    y_pred should be a list of string predictions
    tokenizer could be any function that takes input a string, and returns a
    list of tokens

    :param y_test: Actual list of list of references
    :param y_pred: Actual list of predictions
    :param metrics: List of metric names for metrics to calculate.
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
    :param openai_params: Dictionary containing credentials for openai API.
    :param use_chat_completion_api: boolean flag to choose between openAI completion vs chat completion API.
    """
    _validation.validate_qa(y_test, y_pred, metrics, tokenizer, regexes_to_ignore,
                            ignore_case, ignore_punctuation, ignore_numbers)
    _validation.log_qa_debug(y_test, y_pred, tokenizer, regexes_to_ignore,
                             ignore_case, ignore_punctuation, ignore_numbers)

    results = {}
    for name in metrics:
        safe_name = _scoring_utilities.get_safe_metric_name(name)
        try:
            metric_class = _scoring_utilities.get_metric_class(name)
            if name == constants.Metric.GPTGroundedness:
                metric = metric_class(y_pred, tokenizer, contexts, openai_params, regexes_to_ignore,
                                      ignore_case, ignore_punctuation, ignore_numbers,
                                      lang, openai_api_batch_size, use_chat_completion_api)
            else:
                metric = metric_class(y_test, y_pred, tokenizer, regexes_to_ignore,
                                      ignore_case, ignore_punctuation, ignore_numbers,
                                      lang, model_type, idf, rescale_with_baseline, questions,
                                      contexts, openai_api_batch_size, openai_params,
                                      use_chat_completion_api)
            results[name] = metric.compute()
        except MemoryError:
            raise
        except Exception as e:
            logger.error("Scoring failed for QA metric {}".format(safe_name))
            log_traceback(e, logger, is_critical=False)
            if results.get(name, None) is None:
                if utilities.is_scalar(name):
                    results[name] = np.nan
                else:
                    results[name] = [e.__class__.__name__ for _ in range(len(y_pred))]
    return utilities.segregate_scalar_non_scalar(results)


def _score_fill_mask(
        log_activity: Callable[[logging.Logger, str, Optional[str],
                                Optional[Dict[str, Any]]], Iterator[Optional[Any]]],
        log_traceback: Callable[[BaseException, logging.Logger, Optional[str],
                                 Optional[bool], Optional[Any]], None],
        y_test: List[Any],
        y_pred: List[str],
        metrics: List[str],
        model_id: Optional[str],
        batch_size: Optional[int],
        add_start_token: Optional[bool],):
    """
    Compute model evaluation metrics for a LM task.

    y_test should be a list of string references
    y_pred should be a list of string predictions

    :param y_test: Actual list of list of references
    :param y_pred: Actual list of predictions
    :param metrics: List of metric names for metrics to calculate.
    :param metrics: Language Modeling metrics to compute point estimates
    :param model_id: model used for calculating Perplexity.
                        Perplexity can only be calculated for causal language models.
    :param batch_size (int): the batch size to run texts through the model. Defaults to 16.
    :param add_start_token (bool): whether to add the start token to the texts,
        so the perplexity can include the probability of the first word. Defaults to True.
    """
    _validation.validate_fill_mask(y_test, y_pred, metrics, model_id, batch_size,
                                   add_start_token)
    _validation.log_fill_mask_debug(y_test, y_pred, model_id, batch_size,
                                    add_start_token)

    results = {}
    for name in metrics:
        safe_name = _scoring_utilities.get_safe_metric_name(name)
        try:
            metric_class = _scoring_utilities.get_metric_class(name)
            metric = metric_class(y_test, y_pred, model_id,
                                  batch_size, add_start_token)
            results[name] = metric.compute()
        except MemoryError:
            raise
        except Exception as e:
            logger.error("Scoring failed for Fill Mask metric {}".format(safe_name))
            log_traceback(e, logger, is_critical=False)
            results[name] = np.nan
    return utilities.segregate_scalar_non_scalar(results)


def _aggregate_scores(
        log_activity: Callable[[logging.Logger, str, Optional[str],
                                Optional[Dict[str, Any]]], Iterator[Optional[Any]]],
        log_traceback: Callable[[BaseException, logging.Logger, Optional[str],
                                 Optional[bool], Optional[Any]], None],
        scores: List[Dict[str, Dict[str, Any]]],
        metrics: List[str]
) -> Dict[str, Dict[str, Union[float, Dict[str, Any]]]]:
    """
    Compute mean scores across validation folds.

    :param scores: List of results from scoring functions.
    :param metrics: List of metrics to aggregate.
    :return: Dictionary containing the aggregated scores.
    """

    scores = [utilities.amalgamate_scalar_non_scalar(score) for score in scores]

    means = {}  # type: Dict[str, Union[float, Dict[str, Any]]]
    for name in metrics:
        if name not in scores[0]:
            logger.warning("Tried to aggregate metric {}, but {} was not found in scores".format(name, name))
            continue

        split_results = [score[name] for score in scores if name in score]
        _validation.log_failed_splits(split_results, name)
        metric_class = _scoring_utilities.get_metric_class(name)
        try:
            means[name] = metric_class.aggregate(split_results)
        except Exception as e:
            safe_name = _scoring_utilities.get_safe_metric_name(name)
            logger.error("Score aggregation failed for metric {}".format(safe_name))
            log_traceback(e, logger, is_critical=False)
            means[name] = NonScalarMetric.get_error_metric()

        try:
            name_extras = MetricExtrasConstants.MetricExtrasFormat.format(name)
            split_results_extras = [score[name_extras] for score in scores if name_extras in score]

            if len(split_results_extras) > 0:
                means_name_extras = {}  # type: Dict[str, List[float]]

                stats = split_results_extras[0].keys()
                for stat in stats:
                    means_name_extras[stat] = \
                        metric_class.aggregate([score[stat] for score in split_results_extras])

                means[name_extras] = means_name_extras

        except Exception as e:
            safe_name = _scoring_utilities.get_safe_metric_name(name)
            logger.error("Score aggregation failed for metric extras {}".format(safe_name))
            log_traceback(e, logger, is_critical=False)

    for train_type in ALL_TIME:
        train_times = [res[train_type] for res in scores if train_type in res]
        if train_times:
            means[train_type] = float(np.mean(train_times))

    return utilities.segregate_scalar_non_scalar(means)
