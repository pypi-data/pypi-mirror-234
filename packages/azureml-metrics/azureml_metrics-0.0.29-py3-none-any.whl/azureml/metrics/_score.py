# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Computation of AzureML model evaluation metrics."""
import logging
from typing import Any, Dict, Optional, Union, List

import numpy as np
import pandas as pd
import ast

from azureml.metrics import constants
from azureml.metrics.common import utilities
from azureml.metrics.common._score_utils import compute_metrics_classification, compute_metrics_regression, \
    compute_metrics_translation, compute_metrics_ner, compute_metrics_summarization, compute_metrics_qa, \
    compute_metrics_fill_mask, compute_metrics_text_generation, compute_metrics_forecasting, \
    compute_metrics_image_od_is, compute_metrics_chat_completion, compute_metrics_rag_evaluation, \
    compute_metrics_video_mot, \
    compute_metrics_code_generation, \
    get_supported_metrics
from azureml.metrics.text.classification.azureml_classification_metrics import AzureMLClassificationMetrics
from azureml.metrics.common.exceptions import InvalidUserInputException, InvalidOperationException


logger = logging.getLogger(__name__)


def compute_metrics(*,
                    task_type: Optional[constants.Tasks] = None,
                    y_test: Optional[Union[np.ndarray, pd.DataFrame, List]] = None,
                    # Either y_pred or y_pred_proba should be passed for classification
                    y_pred: Optional[Union[np.ndarray, pd.DataFrame, List]] = None,
                    y_pred_proba: Optional[Union[np.ndarray, pd.DataFrame, List]] = None,
                    **kwargs) -> Dict[str, Dict[str, Any]]:
    """Given task type, y_test, y_pred or y_pred_proba compute metrics for the respective task.

        :param task_type: Accepts an argument of type constants.Tasks for which metrics have to be computed.
            Can accept from any of the values constants.Tasks.CLASSIFICATION, constants.Tasks.REGRESSION,
            constants.Tasks.TEXT_CLASSIFICATION, constants.Tasks.TEXT_CLASSIFICATION_MULTILABEL,
            constants.Tasks.TEXT_NER, constants.Tasks.SUMMARIZATION, constants.Tasks.TRANSLATION,
            constants.Tasks.QUESTION_ANSWERING, constants.Tasks.IMAGE_OBJECT_DETECTION,
            constants.Tasks.IMAGE_INSTANCE_SEGMENTATION, constants.Tasks.FORECASTING.
        :param y_test: Ground truths or reference values.
            optional for computing few of language_modeling metrics and gpt related metrics.
        :param y_pred: Prediction values.
        :param y_pred_proba: Predicted probability values.

        Example for multiclass classification:
        --------------------------------------
        from azureml.metrics import compute_metrics, constants
        y_pred = [0, 2, 1, 3]
        y_true = [0, 1, 2, 3]
        compute_metrics(task_type=constants.Tasks.CLASSIFICATION, y_test=y_true,
                           y_pred=y_pred)

        Example for multilabel classification:
        --------------------------------------
        from azureml.metrics import compute_metrics, constants
        y_test = np.array([[1, 1, 0],
                        [0, 1, 0],
                        [0, 1, 1],
                        [1, 0, 1]])
        y_pred_proba = np.array([[0.9, 0.6, 0.4],
                                    [0.3, 0.8, 0.6],
                                    [0.1, 0.9, 0.8],
                                    [0.7, 0.1, 0.6]])
        # class labels should be in same order as probability values
        class_labels = np.array([0, 1, 2])
        result = compute_metrics(task_type=constants.Tasks.CLASSIFICATION, y_test=y_test,
                                    y_pred_proba=y_pred_proba, multilabel=True)

        Example for regression:
        -----------------------
        from azureml.metrics import compute_metrics, constants
        result = compute_metrics(task_type=constants.Tasks.REGRESSION, y_test=[0.1, 0.2],
                                    y_pred=[0.15, 0.2], y_max=0, y_min=1, y_std=2, bin_info=2)

        Example for text-ner:
        ---------------------
        from azureml.metrics import compute_metrics, constants
        y_true = [['O', 'O', 'O', 'B-MISC', 'I-MISC', 'I-MISC', 'O'], ['B-PER', 'I-PER', "O"]]
        y_pred = [['O', 'O', 'B-MISC', 'I-MISC', 'I-MISC', 'I-MISC', 'O'], ['B-PER', 'I-PER', 'O']]
        result = compute_metrics(task_type=constants.Tasks.TEXT_NER, y_test=y_true, y_pred=y_pred)

        Example for translation:
        ------------------------
        from azureml.metrics import compute_metrics, constants
        y_pred = ["hello there general kenobi","foo bar foobar", "blue & red"]
        y_test = [["hello there general kenobi san"], ["foo bar foobar"], ["blue & green"]]
        result = compute_metrics(task_type=constants.Tasks.TRANSLATION, y_test=y_test, y_pred=y_pred)

        Example for summarization:
        --------------------------
        from azureml.metrics import compute_metrics, constants
        y_pred = ["hello there general kenobi","foo bar foobar", "blue & red"]
        y_test = [["hello there general kenobi san"], ["foo bar foobar"], ["blue & green"]]
        result = compute_metrics(task_type=constants.Tasks.SUMMARIZATION, y_test=y_test, y_pred=y_pred)

        Example for question-answering:
        -------------------------------
        from azureml.metrics import compute_metrics, constants
        y_pred = ["hello there general kenobi the 123","foo bar foobar", "ram 234", "sid"]
        y_test = ["hello there general kenobi san", "foo bar foobar", "ram 23", "sid$"]
        result = compute_metrics(task_type=constants.Tasks.QUESTION_ANSWERING, y_test=y_test, y_pred=y_pred)

        from azureml.metrics import compute_metrics, constants
        y_test = ["hello", "red and blue", "movie is good"]
        y_pred = ["hi", "green and blue", "he dances"]
        result=compute_metrics(task_type=constants.Tasks.QUESTION_ANSWERING, y_test=y_test, y_pred=y_pred,
                               model_type="microsoft/deberta-large", idf=True, rescale_with_baseline=True)

        from azureml.metrics import compute_metrics, constants
        openai_params = {'api_version': "<placeholder>",
                         'api_base': "<placeholder>",
                         'api_type': "<placeholder>",
                         'api_key': "<placeholder>"}
        questions = ["To whom did the Virgin Mary allegedly appear in 1858 in Lourdes France?"] * 3
        y_test = ["Saint Bernadette Soubirous"] * 3
        y_pred = ["Virgin Mary allegedly appear in 1858 in Lourdes France to Saint Bernadette Soubirous"] * 3
        result = compute_metrics(task_type=constants.Tasks.QUESTION_ANSWERING, y_test=y_test, y_pred=y_pred,
                                 questions=questions, openai_params=openai_params)

        Example for fill-mask:
        ---------------------
        from azureml.metrics import compute_metrics, constants
        y_pred = ["hi", "green and blue", "he dances"]
        result = compute_metrics(task_type=constants.Tasks.FILL_MASK, y_pred=y_pred,
                        model_id="gpt2")

        Example for text_generation:
        ----------------------------
        from azureml.metrics import compute_metrics, constants
        y_pred = ["hello there general kenobi","foo bar foobar", "blue & red"]
        y_test = [["hello there general kenobi san"], ["foo bar foobar"], ["blue & green"]]
        result = compute_metrics(task_type=constants.Tasks.TEXT_GENERATION, y_test=y_test, y_pred=y_pred)

        Example for code_generation:
        ----------------------------
        from azureml.metrics import compute_metrics, constants
        y_test = ["assert add(2,3)==5"]
        y_pred = [["def add(a, b): return a+b", "def add(a,b): return a*b"]]
        result = compute_metrics(task_type=constants.Tasks.CODE_GENERATION, y_test=y_test, y_pred=y_pred)

        Example for object-detection:
        -------------------------------
        from azureml.metrics import compute_metrics
        y_test = [{
                "boxes": np.array([[160, 120, 320, 240]], dtype=np.float32),
                "classes": np.array([1])
            }]
        image_meta_info = [{
                "areas": [60000],
                "iscrowd": [0],
                "filename": "image_1.jpg",
                "height": 640,
                "width": 480,
                "original_width": 640,
                "original_height": 480,
            }]
        y_pred = [{
                "boxes": np.array([[160, 120, 320, 240]], dtype=np.float32),
                "classes": np.array([1]),
                "scores": np.array([0.75]),
            }]
        result = compute_metrics(task_type=constants.Tasks.IMAGE_OBJECT_DETECTION, y_test=y_test,
                                    y_pred=y_pred,image_meta_info=image_meta_info)

        Example for instance-segmentation:
        -------------------------------
        from azureml.metrics import compute_metrics
        from pycocotools import mask as pycoco_mask
        def _rle_mask_from_bbox(bbox, height, width):
            x1, y1, x2, y2 = bbox
            polygon = [[x1, y1, x2, y1, x2, y2, x1, y2, x1, y1]]
            rle_masks = pycoco_mask.frPyObjects(polygon, height, width)
            return rle_masks[0]

        y_test = [{
                "boxes": np.array([[160, 120, 320, 240]], dtype=np.float32),
                "classes": np.array([1]),
                "masks": [_rle_mask_from_bbox([1, 0, 2, 100], 640, 640)],
            }]
        image_meta_info = [{
                "areas": [60000],
                "iscrowd": [0],
                "filename": "image_1.jpg",
                "height": 640,
                "width": 480,
                "original_width": 640,
                "original_height": 480,
            }]
        y_pred = [{
                "boxes": np.array([[160, 120, 320, 240]], dtype=np.float32),
                "masks": [_rle_mask_from_bbox([1, 0, 2, 100], 640, 640)],
                "classes": np.array([1]),
                "scores": np.array([0.75]),
            }]
        result = compute_metrics(task_type=constants.Tasks.IMAGE_INSTANCE_SEGMENTATION, y_test=y_test,
                                        y_pred=y_pred,image_meta_info=image_meta_info)

        Example for forecasting:
        >>>from azureml.metrics import compute_metrics, constants
        >>>X = pd.DataFrame({
           'date': pd.date_range('2001-01-01', freq='D', periods=42),
           'ts_id': 'a',
           'target': np.random.rand(42)
           })
        >>>X_train = X.iloc[:-10]
        >>>y_train = X_train.pop('target').values
        >>>X_test = X.iloc[-10:]
        >>>y_test = X_test.pop('target').values
        >>>y_pred = np.random.rand(10)
        >>>result = compute_metrics(
            task_type=constants.Tasks.FORECASTING,
            y_test=y_test,
            y_pred=y_pred,
            X_train=X_train,
            y_train=y_train,
            time_column_name='date',
            time_series_id_column_names=['ts_id'],
            X_test=X_test)

        Example for rag-evaluation
        --------------------------
        from azureml.metrics import compute_metrics, constants

        # Expected conversation structure
        # rag_conversations = [
        #     # conversation 0
        #     [
        #         # turn 0
        #         [
        #             dict(user, assitant, retrieved_documents)
        #         ],
        #         # turn 1
        #         [
        #             dict(user, assitant, retrieved_documents)
        #         ],
        #         # turn 2
        #         [
        #             dict(user, assitant, retrieved_documents)
        #         ]
        #     ],
        #     # conversation 1
        #     []
        # ]

        y_pred = [[{"user": {"content": "how are you?"},
                    "assistant": {"content": "I'm doing good. thank you!!"},
                    "retrieved_documents": '{"retrieved_documents": "document1"}'}]]

        rag_evaluation_params = {
            "model_url": GPT4_URL,
            "model_key": GPT4_KEY,
            "is_chat": True,
            "use_chat_completion": False,
        }

        result = compute_metrics(task_type=constants.Tasks.RAG_EVALUATION, y_pred=y_pred,
                                 rag_evaluation_params=rag_evaluation_params, score_version="v1")

        Example for chat completion
        ---------------------------
        from azureml.metrics import compute_metrics, constants

        y_test = [
            [
                    {"role": "user", "content": "What is the tallest building in the world?"},
                    {
                        "role": "assistant",
                        "content": "Burj Khalifa",
                    },
                    {"role": "user", "content": "and in Africa?"},
                    {
                        "role": "assistant",
                        "content": "In Africa, the tallest building is the Carlton Centre, located in Johannesburg,",
                    },
                    {"role": "user", "content": "and in Europe?"},
        ]]

        y_pred = [
            [
                    {"role": "user", "content": "What is the tallest building in the world?"},
                    {
                        "role": "assistant",
                        "content": "As of 2021, the Burj Khalifa in Dubai, United Arab Emirates is the tallest "
                                   "building in"
                                   " the world, standing at a height of 828 meters (2,722 feet). It was completed in"
                                   " 2010 and has 163 floors. The Burj Khalifa is not only the tallest building in the"
                                   " world but also holds several other records, such as the highest occupied floor, "
                                   " highest outdoor observation deck, elevator with the longest travel distance, and "
                                   " the tallest freestanding structure in the world.",
                    },
                    {"role": "user", "content": "and in Africa?"},
                    {
                        "role": "assistant",
                        "content": "In Africa, the tallest building is the Carlton Centre, located in Johannesburg, "
                                   "South Africa. It stands at a height of 50 floors and 223 meters (730 feet). The"
                                   " CarltonDefault Centre was completed in 1973 and was the tallest building in "
                                   "Africa for many years until the construction of the Leonardo, a 55-story "
                                   "skyscraper in Sandton, Johannesburg, which was completed in 2019 and stands at a"
                                   " height of 230 meters (755 feet). Other notable tall buildings in Africa include "
                                   "the Ponte City Apartments in Johannesburg, the John Hancock Center in Lagos, "
                                   "Nigeria, and the Alpha II Building in Abidjan, Ivory Coast",
                    },
                    {"role": "user", "content": "and in Europe?"},
            ]]

        result = compute_metrics(task_type=constants.Tasks.CHAT_COMPLETION, y_pred=y_pred, y_test=y_test)

        Example for code-generation:
        ---------------------------
        from azureml.metrics import compute_metrics, constants
        y_test = [["def add(a, b): return a+b"], ["def multiply(a, b): return a*b"]]
        y_pred = [["def add(a, b): return a+b", "def add(a,b): return a*b"], ["def multiply(a, b): return a+b",
                   "def multiply(a,b): return a*b"]]
        test_cases = ["assert add(2,3)==5", "assert add(2,3)==5"]
        result = compute_metrics(task_type=constants.Tasks.CODE_GENERATION,
                                 y_test=y_test, y_pred=y_pred,
                                 test_cases=test_cases,
                                 no_of_candidates=[1, 2])

    """
    # validation of compute required_metrics
    validate_compute_metrics(task_type, y_test, y_pred, y_pred_proba)

    if task_type is None:
        computed_metrics = compute_supported_metrics(y_test, y_pred, y_pred_proba, kwargs)
    else:
        computed_metrics = compute_metrics_on_task_type(task_type, y_test, y_pred, y_pred_proba, kwargs)

    return computed_metrics


def compute_supported_metrics(y_test, y_pred, y_pred_proba, kwargs):
    required_metrics = kwargs.pop("metrics", None)
    multilabel = kwargs.pop("multilabel", False)
    # If required_metrics is none or if required_metrics value is not a list parameter.
    if required_metrics is None or (not isinstance(required_metrics, list)):
        # TODO : Add a sample docstring response
        safe_message = "Please send task_type or metrics parameter with metrics to be computed in a list."
        raise InvalidUserInputException(safe_message, target="compute_metrics",
                                        reference_code="azureml.required_metrics.compute_metrics",
                                        safe_message=safe_message)
    task_type_metrics_map = {
        constants.Tasks.REGRESSION: constants.Metric.REGRESSION_SET,
        constants.Tasks.FORECASTING:
            constants.Metric.SCALAR_REGRESSION_SET | constants.Metric.FORECAST_SET,
        constants.Tasks.TEXT_NER: constants.Metric.NER_SET,
        constants.Tasks.TRANSLATION: constants.Metric.TRANSLATION_SET,
        constants.Tasks.SUMMARIZATION: constants.Metric.SUMMARIZATION_SET,
        constants.Tasks.QUESTION_ANSWERING: constants.Metric.QA_SET,
        constants.Tasks.FILL_MASK: constants.Metric.FILL_MASK_SET,
        constants.Tasks.TEXT_GENERATION: constants.Metric.TEXT_GENERATION_SET,
        constants.Tasks.IMAGE_INSTANCE_SEGMENTATION: constants.Metric.IMAGE_INSTANCE_SEGMENTATION_SET,
        constants.Tasks.IMAGE_OBJECT_DETECTION: constants.Metric.IMAGE_OBJECT_DETECTION_SET,
        constants.Tasks.CHAT_COMPLETION: constants.Metric.CHAT_COMPLETION_SET,
        constants.Tasks.RAG_EVALUATION: constants.Metric.RAG_EVALUATION_SET,
        constants.Tasks.CODE_GENERATION: constants.Metric.CODE_GENERATION_SET,
        constants.Tasks.VIDEO_MULTI_OBJECT_TRACKING: constants.Metric.VIDEO_MULTI_OBJECT_TRACKING_SET,
    }
    if multilabel is True:
        task_type_metrics_map.update({
            constants.Tasks.TEXT_CLASSIFICATION_MULTILABEL: constants.Metric.CLASSIFICATION_SET,
            constants.Tasks.IMAGE_CLASSIFICATION_MULTILABEL: constants.Metric.CLASSIFICATION_SET_MULTILABEL,
            constants.Tasks.IMAGE_MULTI_LABEL_CLASSIFICATION: constants.Metric.CLASSIFICATION_SET_MULTILABEL,
        })
    else:
        task_type_metrics_map.update({
            constants.Tasks.CLASSIFICATION: constants.Metric.CLASSIFICATION_SET,
            constants.Tasks.TEXT_CLASSIFICATION: constants.Metric.CLASSIFICATION_SET,
            constants.Tasks.IMAGE_CLASSIFICATION: constants.Metric.CLASSIFICATION_SET,
        })

    # iterate over the metric -- collect the task_type and corresponding required_metrics in a dict
    required_task_type_metrics_map = {task_type: [] for task_type in task_type_metrics_map.keys()}
    # collecting all required metrics
    computed_metrics_list = []
    for required_metric in required_metrics:
        metric_found = False
        # TODO: If a single metric is applicable in multiple tasks -- choose based on input data type
        for task_type, supported_metrics in task_type_metrics_map.items():
            # TODO: if metric is supported and validation is completed
            # TODO : compute the metric for all the tasks based on input data validation
            # add break statement once the metric is found if needed.
            if required_metric in supported_metrics:
                metric_found = True
                required_task_type_metrics_map[task_type].append(required_metric)

        if metric_found is False:
            logger.warning("Skipping {} as it is not implemented yet.".format(required_metric))
    # Iterate over required metrics and compute them based on task type
    for task_type, required_metrics in required_task_type_metrics_map.items():
        if len(required_metrics) > 0:
            kwargs["metrics"] = required_metrics
            try:
                caluculated_metrics = compute_metrics_on_task_type(task_type, y_test, y_pred, y_pred_proba, kwargs)
                computed_metrics_list.append(caluculated_metrics)

            except InvalidOperationException as e:
                logger.warning("Skipping the computation of {} for {} task due to the "
                               "following exception : {}".format(required_metrics, task_type,
                                                                 e.safe_message))

    computed_metrics = utilities.concatenate_calculated_metrics(computed_metrics_list)
    return computed_metrics


def validate_compute_metrics(task_type, y_test, y_pred, y_pred_proba):
    """Method to validate y_test and y_pred input data format."""

    if y_pred is None and y_pred_proba is None:
        pred_proba_msg = "Either y_pred or y_pred_proba" if task_type != constants.Tasks.REGRESSION else "y_pred"
        raise Exception("{} should exist.".format(pred_proba_msg))

    if isinstance(y_test, pd.DataFrame) or isinstance(y_pred, pd.DataFrame):
        if (hasattr(y_test, "columns") and len(y_test.columns) != 1) or \
                (hasattr(y_pred, "columns") and len(y_pred.columns) != 1):
            exception_message = "y_test and y_pred should have only one column in the dataframe to compute metrics."
            raise Exception(exception_message)


def validate_y_test(task_type, y_test, kwargs):
    """Validation for special metrics which can be computed when y_test is None."""
    if y_test is None:
        if task_type in [constants.Tasks.CHAT_COMPLETION] and kwargs.get("openai_params") is not None:
            utilities.get_supported_metrics(kwargs, constants.Metric.CHAT_COMPLETION_SET)

        elif task_type in [constants.Tasks.FILL_MASK, constants.Tasks.TEXT_GENERATION,
                           constants.Tasks.CHAT_COMPLETION]:
            utilities.get_supported_metrics(kwargs, constants.Metric.FILL_MASK_SPECIAL_SET)

        elif task_type in [constants.Tasks.RAG_EVALUATION]:
            utilities.get_supported_metrics(kwargs, constants.Metric.RAG_EVALUATION_SET)

        elif task_type in [constants.Tasks.CODE_GENERATION]:
            utilities.get_supported_metrics(kwargs, constants.Metric.CODE_GENERATION_SPECIAL_SET)

        elif task_type in [constants.Tasks.QUESTION_ANSWERING]:
            utilities.get_supported_metrics(kwargs, constants.Metric.QA_SPECIAL_SET)

        else:
            raise Exception("y_test argument is needed for compute_metrics")


def compute_metrics_on_task_type(task_type, y_test, y_pred, y_pred_proba, kwargs):
    """Computes the metrics based on provided task_type"""
    validate_y_test(task_type, y_test, kwargs)

    task_type_compute_metrics_function_map = {
        constants.Tasks.CLASSIFICATION: compute_metrics_classification,
        constants.Tasks.TEXT_CLASSIFICATION: compute_metrics_classification,
        constants.Tasks.TEXT_CLASSIFICATION_MULTILABEL: compute_metrics_classification,
        constants.Tasks.REGRESSION: compute_metrics_regression,
        constants.Tasks.FORECASTING: compute_metrics_forecasting,
        constants.Tasks.TEXT_NER: compute_metrics_ner,
        constants.Tasks.TRANSLATION: compute_metrics_translation,
        constants.Tasks.SUMMARIZATION: compute_metrics_summarization,
        constants.Tasks.QUESTION_ANSWERING: compute_metrics_qa,
        constants.Tasks.FILL_MASK: compute_metrics_fill_mask,
        constants.Tasks.TEXT_GENERATION: compute_metrics_text_generation,
        constants.Tasks.CHAT_COMPLETION: compute_metrics_chat_completion,
        constants.Tasks.RAG_EVALUATION: compute_metrics_rag_evaluation,
        constants.Tasks.CODE_GENERATION: compute_metrics_code_generation,
        constants.Tasks.IMAGE_INSTANCE_SEGMENTATION: compute_metrics_image_od_is,
        constants.Tasks.IMAGE_OBJECT_DETECTION: compute_metrics_image_od_is,
        constants.Tasks.IMAGE_CLASSIFICATION: compute_metrics_classification,
        constants.Tasks.IMAGE_CLASSIFICATION_MULTILABEL: compute_metrics_classification,
        constants.Tasks.IMAGE_MULTI_LABEL_CLASSIFICATION: compute_metrics_classification,
        constants.Tasks.VIDEO_MULTI_OBJECT_TRACKING: compute_metrics_video_mot,
    }

    compute_metrics_function = task_type_compute_metrics_function_map.get(task_type, None)

    if compute_metrics_function is None:
        supported_tasks = list_tasks()
        raise Exception(f"Invalid task type. Please choose among the following task types : {supported_tasks}")

    classification_task_types = \
        [constants.Tasks.CLASSIFICATION, constants.Tasks.TEXT_CLASSIFICATION,
         constants.Tasks.TEXT_CLASSIFICATION_MULTILABEL, constants.Tasks.IMAGE_CLASSIFICATION,
         constants.Tasks.IMAGE_CLASSIFICATION_MULTILABEL,
         constants.Tasks.IMAGE_MULTI_LABEL_CLASSIFICATION]

    if task_type in classification_task_types:
        computed_metrics = compute_metrics_function(task_type, y_test, y_pred, y_pred_proba, kwargs)

    else:
        computed_metrics = compute_metrics_function(task_type, y_test, y_pred, kwargs)

    return computed_metrics


def score(*,
          task_type: constants.Tasks,
          model: Any,
          X_test: Any,
          y_test: Union[np.ndarray, pd.DataFrame, List],
          **kwargs) -> Dict[str, Dict[str, Any]]:
    """Given task type, model, y_test, y_pred or y_pred_proba compute predictions and the respective metrics.

        :param task_type: Accepts an argument of type constants.Tasks for which metrics have to be computed.
            Can accept from any of the values constants.Tasks.CLASSIFICATION, constants.Tasks.REGRESSION,
            constants.Tasks.TEXT_CLASSIFICATION, constants.Tasks.TEXT_CLASSIFICATION_MULTILABEL,
            constants.Tasks.TEXT_NER, constants.Tasks.FORECASTING.
        :param model: Any model which has a callable predict method that generates predictions.
        :param X_test: Test data which is sent to the model to compute predictions.
        :param y_test: Ground truths or references.
    """
    # Step 1: Generate predictions using model
    # Step 2: Extract whether predict proba is required, compute and add to kwargs if yes
    # Step 3: Call compute metrics method and pass appropriate kwargs to compute and fetch metrics

    if not (hasattr(model, "predict") and callable(getattr(model, 'predict'))):
        raise Exception("Model should have callable predict method.")

    try:
        if hasattr(model, "forecast") and callable(getattr(model, 'forecast')):
            # In the forecast data we are not guaranteed to have the same
            # dimension of output data as the input so we have to preaggregate
            # the data here.
            if 'X_train' in kwargs and 'y_train' in kwargs:
                kwargs['X_train'], kwargs['y_train'] = model.preaggregate_data_set(
                    kwargs['X_train'], kwargs['y_train'], is_training_set=True)
            X_test_agg, y_test = model.preaggregate_data_set(X_test, y_test)
            y_pred, _ = model.forecast(X_test)
            X_test = X_test_agg
            # Take forecasting-specific parameters from the model.
            kwargs["time_series_id_column_names"] = model.grain_column_names
            kwargs["time_column_name"] = model.time_column_name
        else:
            y_pred = model.predict(X_test)
            y_pred = utilities.check_and_convert_to_np(y_pred)

        multilabel = kwargs.get("multilabel", False)
        if multilabel or (task_type in [constants.Tasks.TEXT_CLASSIFICATION_MULTILABEL,
                                        constants.Tasks.TEXT_NER]):
            y_pred = [ast.literal_eval(label) for label in y_pred]
    except Exception as e:
        exception_msg = "Error occurred while calling predict method on the model."
        raise Exception(exception_msg + str(e))

    compute_probs = kwargs.get("compute_probs", False)
    if task_type in [constants.Tasks.CLASSIFICATION, constants.Tasks.REGRESSION] and \
            kwargs.get("enable_metric_confidence", False):
        compute_probs = True
    elif task_type == constants.Tasks.FORECASTING:
        kwargs['X_test'] = X_test
    if compute_probs:
        if not (hasattr(model, "predict_proba") and callable(getattr(model, 'predict_proba'))):
            raise Exception("Model should have callable predict_proba method when compute_probs is set to True.")

        try:
            y_pred_proba = model.predict_proba(X_test)
            kwargs["y_pred_proba"] = y_pred_proba
        except Exception as e:
            exception_msg = "Error occurred while calling predict_proba method on the model."
            raise Exception(exception_msg + str(e))

    metrics = compute_metrics(task_type=task_type,
                              y_test=y_test,
                              y_pred=y_pred,
                              **kwargs)

    return metrics


def list_metrics(task_type: constants.Tasks,
                 multilabel: Optional[bool] = False) -> List[str]:
    """Get the list of supported metrics for provided task type.

        :param task_type: Accepts an argument of type constants.Tasks for which metrics have to be computed.
            Can accept from any of the values from constants.Tasks Ex: constants.Tasks.CLASSIFICATION,
            constants.Tasks.REGRESSION, constants.Tasks.TEXT_CLASSIFICATION,
            constants.Tasks.TEXT_CLASSIFICATION_MULTILABEL,
            constants.Tasks.TEXT_NER.
        :param multilabel: Accepts a boolean argument which indicates multilabel classification.

        :return: List of supported metrics based on task type.

        Example for multiclass classification:
        --------------------------------------
        >>>from azureml.metrics import list_metrics, constants
        >>>list_metrics(task_type=constants.Tasks.CLASSIFICATION)

        Example for multilabel classification:
        --------------------------------------
        >>>from azureml.metrics import list_metrics, constants
        >>>list_metrics(task_type=constants.Tasks.CLASSIFICATION, multilabel=True)

        Example for multiclass text classification:
        -------------------------------------------
        >>>from azureml.metrics import list_metrics, constants
        >>>list_metrics(task_type=constants.Tasks.CLASSIFICATION)

        Example for multilabel text classification:
        -------------------------------------------
        >>>from azureml.metrics import list_metrics, constants
        >>>list_metrics(task_type=constants.Tasks.TEXT_CLASSIFICATION_MULTILABEL)

        Example for text named entity recognition:
        ------------------------------------------
        >>>from azureml.metrics import list_metrics, constants
        >>>list_metrics(task_type=constants.Tasks.TEXT_NER)

        Example for translation:
        ------------------------
        >>>from azureml.metrics import list_metrics, constants
        >>>list_metrics(task_type=constants.Tasks.TRANSLATION)

        Example for summarization:
        --------------------------
        >>>from azureml.metrics import list_metrics, constants
        >>>list_metrics(task_type=constants.Tasks.SUMMARIZATION)

        Example for question answering:
        -------------------------------
        >>>from azureml.metrics import list_metrics, constants
        >>>list_metrics(task_type=constants.Tasks.QUESTION_ANSWERING)

        Example for text generation:
        -------------------------------
        >>>from azureml.metrics import list_metrics, constants
        >>>list_metrics(task_type=constants.Tasks.TEXT_GENERATION)

        Example for language modeling:
        -------------------------------
        >>>from azureml.metrics import list_metrics, constants
        >>>list_metrics(task_type=constants.Tasks.FILL_MASK)

        Example for object detection:
        --------------------------
        >>>from azureml.metrics import list_metrics, constants
        >>>list_metrics(task_type=constants.Tasks.IMAGE_OBJECT_DETECTION)

        Example for instance segmentation:
        -------------------------------
        >>>from azureml.metrics import list_metrics, constants
        >>>list_metrics(task_type=constants.Tasks.IMAGE_INSTANCE_SEGMENTATION)
    """
    result = get_supported_metrics(task_type)

    if result is None:
        return f"Metrics are not implemented for provided task type : {task_type}."
    elif result == AzureMLClassificationMetrics:
        multilabel_tasks = [constants.Tasks.TEXT_CLASSIFICATION_MULTILABEL,
                            constants.Tasks.IMAGE_CLASSIFICATION_MULTILABEL,
                            constants.Tasks.IMAGE_MULTI_LABEL_CLASSIFICATION]
        if task_type in multilabel_tasks:
            multilabel = True
        metrics = result.list_metrics(multilabel=multilabel)
    else:
        metrics = result.list_metrics()

    return metrics


def list_tasks() -> List[str]:
    """Get the list of supported task types.

       Example:
       -------
       >>> from azureml.metrics import list_tasks
       >>> supported_tasks = list_tasks()
    """
    supported_tasks = constants.TASK_TYPES
    return supported_tasks
