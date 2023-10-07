# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Metrics constants."""
import sys
from enum import Enum

import numpy as np


class TrainingResultsType:
    """Defines potential results from runners class."""

    # Metrics
    TRAIN_METRICS = "train"
    VALIDATION_METRICS = "validation"
    TEST_METRICS = "test"
    TRAIN_FROM_FULL_METRICS = "train from full"
    TEST_FROM_FULL_METRICS = "test from full"
    CV_METRICS = "CV"
    CV_MEAN_METRICS = "CV mean"

    # Other useful things
    TRAIN_TIME = "train time"
    FIT_TIME = "fit_time"
    PREDICT_TIME = "predict_time"
    BLOB_TIME = "blob_time"
    ALL_TIME = {TRAIN_TIME, FIT_TIME, PREDICT_TIME}
    TRAIN_PERCENT = "train_percent"
    MODELS = "models"

    # Status:
    TRAIN_VALIDATE_STATUS = "train validate status"
    TRAIN_FULL_STATUS = "train full status"
    CV_STATUS = "CV status"


class MetricExtrasConstants:
    """Define internal values of Confidence Intervals."""

    UPPER_95_PERCENTILE = "upper_ci_95"
    LOWER_95_PERCENTILE = "lower_ci_95"
    VALUE = "value"

    # Confidence Interval metric name format
    MetricExtrasSuffix = "_extras"
    MetricExtrasFormat = "{}" + MetricExtrasSuffix

    # Aggregation logic extra suffix
    MeanExtrasPrefix = "mean_"
    MeanExtrasFormat = MeanExtrasPrefix + "{}"
    MeanExtrasDictFormat = MeanExtrasPrefix + "{}_{}"


class RetryConstants:
    """Define constants to be used in retry logic."""
    MAX_ATTEMPTS = 3
    DELAY_TIME = 10


class Metric:
    """Defines all metrics supported by classification and regression."""

    # Scalar & non scalar segregation key constants
    Metrics = "metrics"  # Scalar
    Artifacts = "artifacts"  # Non-Scalar

    # Classification
    AUCBinary = "AUC_binary"
    AUCMacro = "AUC_macro"
    AUCMicro = "AUC_micro"
    AUCWeighted = "AUC_weighted"
    Accuracy = "accuracy"
    WeightedAccuracy = "weighted_accuracy"
    BalancedAccuracy = "balanced_accuracy"
    NormMacroRecall = "norm_macro_recall"
    LogLoss = "log_loss"
    F1Binary = "f1_score_binary"
    F1Micro = "f1_score_micro"
    F1Macro = "f1_score_macro"
    F1Weighted = "f1_score_weighted"
    PrecisionBinary = "precision_score_binary"
    PrecisionMicro = "precision_score_micro"
    PrecisionMacro = "precision_score_macro"
    PrecisionWeighted = "precision_score_weighted"
    RecallBinary = "recall_score_binary"
    RecallMicro = "recall_score_micro"
    RecallMacro = "recall_score_macro"
    RecallWeighted = "recall_score_weighted"
    AvgPrecisionBinary = "average_precision_score_binary"
    AvgPrecisionMicro = "average_precision_score_micro"
    AvgPrecisionMacro = "average_precision_score_macro"
    AvgPrecisionWeighted = "average_precision_score_weighted"
    AccuracyTable = "accuracy_table"
    ConfusionMatrix = "confusion_matrix"
    MatthewsCorrelation = "matthews_correlation"

    # Multilabel classification
    IOU = "iou"
    IOUMicro = "iou_micro"
    IOUMacro = "iou_macro"
    IOUWeighted = "iou_weighted"
    IOUClasswise = "iou_classwise"

    # Regression
    ExplainedVariance = "explained_variance"
    R2Score = "r2_score"
    Spearman = "spearman_correlation"
    MAPE = "mean_absolute_percentage_error"
    SMAPE = "symmetric_mean_absolute_percentage_error"
    MeanAbsError = "mean_absolute_error"
    MedianAbsError = "median_absolute_error"
    RMSE = "root_mean_squared_error"
    RMSLE = "root_mean_squared_log_error"
    NormMeanAbsError = "normalized_mean_absolute_error"
    NormMedianAbsError = "normalized_median_absolute_error"
    NormRMSE = "normalized_root_mean_squared_error"
    NormRMSLE = "normalized_root_mean_squared_log_error"
    Residuals = "residuals"
    PredictedTrue = "predicted_true"

    # Forecast
    ForecastMAPE = 'forecast_mean_absolute_percentage_error'
    ForecastSMAPE = 'forecast_symmetric_mean_absolute_percentage_error'
    ForecastResiduals = 'forecast_residuals'
    ForecastTable = 'forecast_table'
    ForecastTsIDDistributionTable = "forecast_time_series_id_distribution_table"

    # Sequence to Sequence Metrics
    # Seq2Seq Translation
    TranslationBleu_1 = "bleu_1"
    TranslationBleu_2 = "bleu_2"
    TranslationBleu_3 = "bleu_3"
    TranslationBleu_4 = "bleu_4"

    # Seq2Seq Summarization
    SummarizationRouge1 = "rouge1"
    SummarizationRouge2 = "rouge2"
    SummarizationRougeL = "rougeL"
    SummarizationRougeLsum = "rougeLsum"

    # QA
    QAExactMatch = "exact_match"
    QAF1Score = "f1_score"

    # Text Similarity metrics for Question Answering
    BERTScore = "bertscore"
    GPTSimilarity = "gpt_similarity"
    GPTCoherence = "gpt_coherence"
    GPTRelevance = "gpt_relevance"
    GPTGroundedness = "gpt_groundedness"
    GPTFluency = "gpt_fluency"

    # RAG Evaluation metrics
    GenerationScore = "generation_score"
    RetrievalScore = "retrieval_score"
    GroundingScore = "grounding_score"

    # Chat Completion metrics
    ConversationGroundingScore = "conversation_groundedness_score"

    # Code Generation metrics
    CodeGenerationPassRateScore = "code_eval"  # Pass@k

    # Fill Masking Metrics
    FMPerplexity = "perplexities"

    # Image object detection and instance segmentation
    MEAN_AVERAGE_PRECISION = "mean_average_precision"
    AVERAGE_PRECISION = "average_precision"
    PRECISION = "precision"
    RECALL = "recall"
    PER_LABEL_METRICS = "per_label_metrics"
    IMAGE_LEVEL_BINARY_CLASSIFIER_METRICS = "image_level_binary_classsifier_metrics"
    CONFUSION_MATRICES_PER_SCORE_THRESHOLD = "confusion_matrices_per_score_threshold"

    # Video object tracking
    IDF1 = "IDF1"
    MOTA = "MOTA"
    MOTP = "MOTP"
    IDSW = "IDSw"
    PRCN = "Prcn"
    Rcll = "Rcll"
    FP = "FP"
    FN = "FN"
    FM = "FM"
    ML = "ML"
    MT = "MT"
    PT = "PT"

    SCALAR_CLASSIFICATION_SET = {
        AUCBinary,
        AUCMacro,
        AUCMicro,
        AUCWeighted,
        Accuracy,
        WeightedAccuracy,
        NormMacroRecall,
        BalancedAccuracy,
        LogLoss,
        F1Binary,
        F1Micro,
        F1Macro,
        F1Weighted,
        PrecisionBinary,
        PrecisionMicro,
        PrecisionMacro,
        PrecisionWeighted,
        RecallBinary,
        RecallMicro,
        RecallMacro,
        RecallWeighted,
        AvgPrecisionBinary,
        AvgPrecisionMicro,
        AvgPrecisionMacro,
        AvgPrecisionWeighted,
        MatthewsCorrelation,
    }

    SCALAR_CLASSIFICATION_SET_MULTILABEL = {
        AUCBinary,
        AUCMacro,
        AUCMicro,
        AUCWeighted,
        Accuracy,
        NormMacroRecall,
        BalancedAccuracy,
        IOU,
        IOUMacro,
        IOUMicro,
        IOUWeighted,
        LogLoss,
        F1Binary,
        F1Micro,
        F1Macro,
        F1Weighted,
        PrecisionBinary,
        PrecisionMicro,
        PrecisionMacro,
        PrecisionWeighted,
        RecallBinary,
        RecallMicro,
        RecallMacro,
        RecallWeighted,
        AvgPrecisionBinary,
        AvgPrecisionMicro,
        AvgPrecisionMacro,
        AvgPrecisionWeighted,
    }

    CLASSIFICATION_PROB_REQUIRED_SET = {
        AUCBinary,
        AUCMacro,
        AUCMicro,
        AUCWeighted,
        AvgPrecisionBinary,
        AvgPrecisionMacro,
        AvgPrecisionMicro,
        AvgPrecisionWeighted,
        LogLoss,
        AccuracyTable,
        NormMacroRecall,
    }

    NONSCALAR_CLASSIFICATION_SET = {AccuracyTable, ConfusionMatrix}

    CLASSIFICATION_BINARY_SET = {
        AUCBinary,
        F1Binary,
        PrecisionBinary,
        RecallBinary,
        AvgPrecisionBinary,
    }

    CLASSIFICATION_SET = SCALAR_CLASSIFICATION_SET | NONSCALAR_CLASSIFICATION_SET

    CLASSIFICATION_SET_MULTILABEL = (
        SCALAR_CLASSIFICATION_SET_MULTILABEL | NONSCALAR_CLASSIFICATION_SET
    )

    SCALAR_REGRESSION_SET = {
        ExplainedVariance,
        R2Score,
        Spearman,
        MAPE,
        MeanAbsError,
        MedianAbsError,
        RMSE,
        RMSLE,
        NormMeanAbsError,
        NormMedianAbsError,
        NormRMSE,
        NormRMSLE,
    }

    NONSCALAR_REGRESSION_SET = {Residuals, PredictedTrue}

    REGRESSION_SET = SCALAR_REGRESSION_SET | NONSCALAR_REGRESSION_SET

    CLASSIFICATION_PRIMARY_SET = {
        Accuracy,
        AUCWeighted,
        NormMacroRecall,
        AvgPrecisionWeighted,
        PrecisionWeighted,
    }

    CLASSIFICATION_BALANCED_SET = {
        # this is for metrics where we would recommend using class_weights
        BalancedAccuracy,
        AUCMacro,
        NormMacroRecall,
        AvgPrecisionMacro,
        PrecisionMacro,
        F1Macro,
        RecallMacro,
    }

    REGRESSION_PRIMARY_SET = {Spearman, NormRMSE, R2Score, NormMeanAbsError}

    IMAGE_CLASSIFICATION_PRIMARY_SET = {Accuracy}

    IMAGE_CLASSIFICATION_MULTILABEL_PRIMARY_SET = {IOU}

    IMAGE_OBJECT_DETECTION_PRIMARY_SET = {MEAN_AVERAGE_PRECISION}

    IMAGE_OBJECT_DETECTION_SET = {
        MEAN_AVERAGE_PRECISION, RECALL, PRECISION, PER_LABEL_METRICS,
        IMAGE_LEVEL_BINARY_CLASSIFIER_METRICS, CONFUSION_MATRICES_PER_SCORE_THRESHOLD
    }

    IMAGE_INSTANCE_SEGMENTATION_SET = {
        MEAN_AVERAGE_PRECISION, RECALL, PRECISION, PER_LABEL_METRICS
    }

    VIDEO_MULTI_OBJECT_TRACKING_SET = {
        IDF1, MOTA, MOTP, IDSW, PRCN, Rcll,
        FP, FN, FM, ML, MT, PT
    }

    SAMPLE_WEIGHTS_UNSUPPORTED_SET = {
        WeightedAccuracy,
        Spearman,
        MedianAbsError,
        NormMedianAbsError,
    }

    TEXT_CLASSIFICATION_PRIMARY_SET = {Accuracy, AUCWeighted, PrecisionWeighted}

    TEXT_CLASSIFICATION_MULTILABEL_PRIMARY_SET = {Accuracy}

    TEXT_NER_PRIMARY_SET = {Accuracy}

    NER_SET = {
        Accuracy,
        F1Macro,
        F1Micro,
        F1Weighted,
        PrecisionMicro,
        PrecisionMacro,
        PrecisionWeighted,
        RecallMicro,
        RecallMacro,
        RecallWeighted,
    }

    NONSCALAR_FORECAST_SET = {
        ForecastMAPE, ForecastResiduals,
        ForecastTable, ForecastTsIDDistributionTable
    }

    FORECAST_SET = (NONSCALAR_FORECAST_SET)

    # The set of non scalar metrics allowed even if the
    # training set was not provided.
    FORECASTING_NONSCALAR_SET_NO_TRAINING = {
        ForecastTsIDDistributionTable
    }

    # Metrics set for Sequence to Sequence Tasks
    SCALAR_TRANSLATION_SET = {
        TranslationBleu_1,
        TranslationBleu_2,
        TranslationBleu_3,
        TranslationBleu_4,
    }

    TRANSLATION_SET = SCALAR_TRANSLATION_SET

    TRANSLATION_NGRAM_MAP = {
        TranslationBleu_1: 1,
        TranslationBleu_2: 2,
        TranslationBleu_3: 3,
        TranslationBleu_4: 4,
    }

    SCALAR_SUMMARIZATION_SET = {
        SummarizationRouge1,
        SummarizationRouge2,
        SummarizationRougeL,
        SummarizationRougeLsum,
    }

    SUMMARIZATION_SET = SCALAR_SUMMARIZATION_SET

    SCALAR_QA_SET = {QAExactMatch, QAF1Score}

    NONSCALAR_QA_SET = {
        BERTScore,
        GPTSimilarity,
        GPTCoherence,
        GPTGroundedness,
        GPTFluency,
        GPTRelevance,
    }

    SCALAR_CODE_GENERATION_SET = {CodeGenerationPassRateScore}

    QA_SET = SCALAR_QA_SET | NONSCALAR_QA_SET

    # QA metrics that don't need groundtruths.
    QA_SPECIAL_SET = {GPTCoherence, GPTGroundedness, GPTFluency, GPTRelevance}

    QA_GPT_METRICS_SET = {GPTCoherence, GPTGroundedness, GPTFluency, GPTRelevance, GPTSimilarity}

    # Fill Masking Metrics
    SCALAR_FILL_MASK_SET = set()
    NONSCALAR_FILL_MASK_SET = {FMPerplexity}

    # Fill Masking metrics that do not need groundtruths
    FILL_MASK_SPECIAL_SET = {FMPerplexity}

    FILL_MASK_SET = SCALAR_FILL_MASK_SET | NONSCALAR_FILL_MASK_SET

    # Text generation metrics
    SCALAR_TEXT_GENERATION_SET = SCALAR_SUMMARIZATION_SET | SCALAR_TRANSLATION_SET
    NONSCALAR_TEXT_GENERATION_SET = NONSCALAR_FILL_MASK_SET
    TEXT_GENERATION_SET = SCALAR_TEXT_GENERATION_SET | NONSCALAR_TEXT_GENERATION_SET

    # Code Generation Metrics
    CODE_GENERATION_SET = SCALAR_CODE_GENERATION_SET | SCALAR_TEXT_GENERATION_SET
    CODE_GENERATION_SPECIAL_SET = {CodeGenerationPassRateScore}

    # Chat completion metrics
    CONVERSATION_RAI_SET = {ConversationGroundingScore}
    # TODO: Enable F1 Score and Exact Match metrics for chat completion
    SCALAR_CHAT_COMPLETION_SET = SCALAR_TEXT_GENERATION_SET
    NONSCALAR_CHAT_COMPLETION_SET = NONSCALAR_FILL_MASK_SET | CONVERSATION_RAI_SET
    CHAT_COMPLETION_SET = NONSCALAR_CHAT_COMPLETION_SET | SCALAR_CHAT_COMPLETION_SET
    CHAT_COMPLETION_NONGPT_SET = SCALAR_CHAT_COMPLETION_SET | NONSCALAR_FILL_MASK_SET

    # RAG evaluation metrics
    NON_SCALAR_RAG_EVALUATION_SET = {
        GenerationScore,
        RetrievalScore,
        GroundingScore,
    }
    RAG_EVALUATION_SET = NON_SCALAR_RAG_EVALUATION_SET

    SCALAR_SEQ2SEQ_SET = (
        SCALAR_TRANSLATION_SET | SCALAR_SUMMARIZATION_SET | SCALAR_QA_SET | SCALAR_FILL_MASK_SET
        | SCALAR_TEXT_GENERATION_SET | SCALAR_CHAT_COMPLETION_SET
    )

    FULL_SET = CLASSIFICATION_SET | REGRESSION_SET | IMAGE_OBJECT_DETECTION_SET
    NONSCALAR_FULL_SET = (
        NONSCALAR_CLASSIFICATION_SET | NONSCALAR_REGRESSION_SET | NONSCALAR_QA_SET
        | NON_SCALAR_RAG_EVALUATION_SET | NONSCALAR_TEXT_GENERATION_SET
        | NONSCALAR_CHAT_COMPLETION_SET
    )
    SCALAR_FULL_SET = SCALAR_CLASSIFICATION_SET | SCALAR_REGRESSION_SET

    SCALAR_FULL_SET_TIME = SCALAR_FULL_SET | TrainingResultsType.ALL_TIME

    # TODO: These types will be removed when the artifact-backed
    # metrics are defined with protobuf
    # Do not use these constants except in artifact-backed metrics
    SCHEMA_TYPE_ACCURACY_TABLE = "accuracy_table"
    SCHEMA_TYPE_CONFUSION_MATRIX = "confusion_matrix"
    SCHEMA_TYPE_RESIDUALS = "residuals"
    SCHEMA_TYPE_PREDICTIONS = "predictions"
    SCHEMA_TYPE_MAPE = "mape_table"
    SCHEMA_TYPE_SMAPE = "smape_table"

    # Metrics that need to be aggregated
    NON_AGGREGATED_METRICS = {FMPerplexity, BERTScore} | QA_GPT_METRICS_SET


class Tasks:
    """Defines types of machine learning tasks supported by automated ML."""

    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    FORECASTING = "forecasting"

    # Sequence to Sequence Tasks
    TRANSLATION = "translation"
    SUMMARIZATION = "summarization"
    QUESTION_ANSWERING = "qa"
    FILL_MASK = "fill-mask"
    TEXT_GENERATION = "text-generation"

    # Chat Completion task type
    CHAT_COMPLETION = "chat-completion"

    # RAG Evaluation task type
    RAG_EVALUATION = "rag-evaluation"

    # Code Generation
    CODE_GENERATION = "code-generation"

    IMAGE_CLASSIFICATION = 'image-classification'
    IMAGE_CLASSIFICATION_MULTILABEL = 'image-classification-multilabel'
    IMAGE_MULTI_LABEL_CLASSIFICATION = 'image-multi-labeling'  # for temporary backward-compatibility
    IMAGE_OBJECT_DETECTION = 'image-object-detection'
    IMAGE_INSTANCE_SEGMENTATION = 'image-instance-segmentation'
    _ALL_IMAGE_CLASSIFICATION = [IMAGE_CLASSIFICATION, IMAGE_CLASSIFICATION_MULTILABEL,
                                 IMAGE_MULTI_LABEL_CLASSIFICATION]

    _ALL_IMAGE_OBJECT_DETECTION = [IMAGE_OBJECT_DETECTION, IMAGE_INSTANCE_SEGMENTATION]
    _ALL_IMAGE = [
        IMAGE_CLASSIFICATION,
        IMAGE_CLASSIFICATION_MULTILABEL,
        IMAGE_MULTI_LABEL_CLASSIFICATION,
        IMAGE_OBJECT_DETECTION,
        IMAGE_INSTANCE_SEGMENTATION,
    ]
    VIDEO_MULTI_OBJECT_TRACKING = "video-multi-object-tracking"

    TEXT_CLASSIFICATION = "text-classification"
    TEXT_CLASSIFICATION_MULTILABEL = "text-classification-multilabel"
    TEXT_NER = "text-ner"

    _ALL_CLASSIFICATION_TASKS = \
        [CLASSIFICATION, TEXT_CLASSIFICATION,
         TEXT_CLASSIFICATION_MULTILABEL, IMAGE_CLASSIFICATION,
         IMAGE_CLASSIFICATION_MULTILABEL,
         IMAGE_MULTI_LABEL_CLASSIFICATION]

    _ALL_TEXT = [TEXT_CLASSIFICATION, TEXT_CLASSIFICATION_MULTILABEL, TEXT_NER]
    _ALL_DNN = _ALL_IMAGE + _ALL_TEXT
    _ALL = _ALL_IMAGE + _ALL_TEXT


class ImageTask(Enum):
    """Available Image task types."""

    IMAGE_CLASSIFICATION = Tasks.IMAGE_CLASSIFICATION
    IMAGE_CLASSIFICATION_MULTILABEL = Tasks.IMAGE_CLASSIFICATION_MULTILABEL
    IMAGE_OBJECT_DETECTION = Tasks.IMAGE_OBJECT_DETECTION
    IMAGE_INSTANCE_SEGMENTATION = Tasks.IMAGE_INSTANCE_SEGMENTATION
    VIDEO_MULTI_OBJECT_TRACKING = Tasks.VIDEO_MULTI_OBJECT_TRACKING


class SubTaskType(Enum):
    """Available Sub-task types of Main tasks."""
    TEXT_GENERATION_SUBTASK_CODE = "code"


# Task Types
CLASSIFICATION = "classification"
REGRESSION = "regression"
FORECASTING = "forecasting"
TRANSLATION = "translation"
SUMMARIZATION = "summarization"
QUESTION_ANSWERING = "qa"
FILL_MASK = "fill-mask"
TEXT_GENERATION = "text-generation"
CHAT_COMPLETION = "chat-completion"
RAG_EVALUATION = "rag-evaluation"
IMAGE_CLASSIFICATION = "image-classification"
IMAGE_CLASSIFICATION_MULTILABEL = "image-classification-multilabel"
IMAGE_MULTI_LABEL_CLASSIFICATION = "image-multi-labeling"
IMAGE_OBJECT_DETECTION = "image-object-detection"
IMAGE_INSTANCE_SEGMENTATION = "image-instance-segmentation"
VIDEO_MULTI_OBJECT_TRACKING = "video-multi-object-tracking"
TEXT_CLASSIFICATION = "text-classification"
TEXT_CLASSIFICATION_MULTILABEL = "text-classification-multilabel"
TEXT_NER = "text-ner"
CODE_GENERATION = "code-generation"


TASK_TYPES = {
    # Tabular task types
    CLASSIFICATION,
    REGRESSION,
    FORECASTING,
    # Image/vision task types
    IMAGE_CLASSIFICATION,
    IMAGE_CLASSIFICATION_MULTILABEL,
    IMAGE_MULTI_LABEL_CLASSIFICATION,
    IMAGE_OBJECT_DETECTION,
    IMAGE_INSTANCE_SEGMENTATION,
    # Text task types
    TEXT_CLASSIFICATION,
    TEXT_CLASSIFICATION_MULTILABEL,
    TEXT_NER,
    TRANSLATION,
    SUMMARIZATION,
    QUESTION_ANSWERING,
    FILL_MASK,
    TEXT_GENERATION,
    CHAT_COMPLETION,
    RAG_EVALUATION,
    CODE_GENERATION
}

# Classification Metrics

ACCURACY = "accuracy"
WEIGHTED_ACCURACY = "weighted_accuracy"
BALANCED_ACCURACY = "balanced_accuracy"
NORM_MACRO_RECALL = "norm_macro_recall"
LOG_LOSS = "log_loss"
AUC_BINARY = "AUC_binary"
AUC_MACRO = "AUC_macro"
AUC_MICRO = "AUC_micro"
AUC_WEIGHTED = "AUC_weighted"
F1_BINARY = "f1_score_binary"
F1_MACRO = "f1_score_macro"
F1_MICRO = "f1_score_micro"
F1_WEIGHTED = "f1_score_weighted"
PRECISION_BINARY = "precision_score_binary"
PRECISION_MACRO = "precision_score_macro"
PRECISION_MICRO = "precision_score_micro"
PRECISION_WEIGHTED = "precision_score_weighted"
RECALL_BINARY = "recall_score_binary"
RECALL_MACRO = "recall_score_macro"
RECALL_MICRO = "recall_score_micro"
RECALL_WEIGHTED = "recall_score_weighted"
AVERAGE_PRECISION_BINARY = "average_precision_score_binary"
AVERAGE_PRECISION_MACRO = "average_precision_score_macro"
AVERAGE_PRECISION_MICRO = "average_precision_score_micro"
AVERAGE_PRECISION_WEIGHTED = "average_precision_score_weighted"
MATTHEWS_CORRELATION = "matthews_correlation"
ACCURACY_TABLE = "accuracy_table"
CONFUSION_MATRIX = "confusion_matrix"
CLASSIFICATION_REPORT = "classification_report"
# multilabel metrics
IOU = "iou"
IOU_MICRO = "iou_micro"
IOU_MACRO = "iou_macro"
IOU_WEIGHTED = "iou_weighted"
IOU_CLASSWISE = "iou_classwise"
# classwise metrics
PRECISION_CLASSWISE = "precision_score_classwise"
RECALL_CLASSWISE = "recall_score_classwise"
F1_CLASSWISE = "f1_score_classwise"
AUC_CLASSWISE = "AUC_classwise"
AVERAGE_PRECISION_CLASSWISE = "average_precision_score_classwise"
# QA
QAExactMatch = "exact_match"
QAF1Score = "f1_score"

# Text Similarity metrics for Question Answering
BERTScore = "bertscore"
GPTSimilarity = "gpt_similarity"
GPTCoherence = "gpt_coherence"
GPTRelevance = "gpt_relevance"
GPTGroundedness = "gpt_groundedness"
GPTFluency = "gpt_fluency"

# RAG Evaluation metrics
GenerationScore = "generation_score"
RetrievalScore = "retrieval_score"
GroundingScore = "grounding_score"

# Code Generation
CODE_GENERATION = "code-generation"

CLASSIFICATION_SCALAR_SET = {
    ACCURACY,
    WEIGHTED_ACCURACY,
    BALANCED_ACCURACY,
    NORM_MACRO_RECALL,
    LOG_LOSS,
    AUC_BINARY,
    AUC_MACRO,
    AUC_MICRO,
    AUC_WEIGHTED,
    F1_BINARY,
    F1_MACRO,
    F1_MICRO,
    F1_WEIGHTED,
    PRECISION_BINARY,
    PRECISION_MACRO,
    PRECISION_MICRO,
    PRECISION_WEIGHTED,
    RECALL_BINARY,
    RECALL_MACRO,
    RECALL_MICRO,
    RECALL_WEIGHTED,
    AVERAGE_PRECISION_BINARY,
    AVERAGE_PRECISION_MACRO,
    AVERAGE_PRECISION_MICRO,
    AVERAGE_PRECISION_WEIGHTED,
    MATTHEWS_CORRELATION,
}

CLASSIFICATION_PROB_REQUIRED_SET = {
    AUC_BINARY,
    AUC_MACRO,
    AUC_MICRO,
    AUC_WEIGHTED,
    AVERAGE_PRECISION_BINARY,
    AVERAGE_PRECISION_MACRO,
    AVERAGE_PRECISION_MICRO,
    AVERAGE_PRECISION_WEIGHTED,
}

CLASSIFICATION_BINARY_SET = {
    AUC_BINARY,
    F1_BINARY,
    PRECISION_BINARY,
    RECALL_BINARY,
    AVERAGE_PRECISION_BINARY,
}

CLASSIFICATION_MULTILABEL_SET = {IOU, IOU_MICRO, IOU_MACRO, IOU_WEIGHTED}

CLASSIFICATION_NLP_MULTILABEL_SET = {
    ACCURACY,
    BALANCED_ACCURACY,
    NORM_MACRO_RECALL,
    LOG_LOSS,
    AUC_MACRO,
    AUC_MICRO,
    AUC_WEIGHTED,
    F1_MACRO,
    F1_MICRO,
    F1_WEIGHTED,
    PRECISION_MACRO,
    PRECISION_MICRO,
    PRECISION_WEIGHTED,
    RECALL_MACRO,
    RECALL_MICRO,
    RECALL_WEIGHTED,
    AVERAGE_PRECISION_MACRO,
    AVERAGE_PRECISION_MICRO,
    AVERAGE_PRECISION_WEIGHTED,
}

CLASSIFICATION_NLP_NER_SET = {
    ACCURACY,
    F1_MACRO,
    F1_MICRO,
    F1_WEIGHTED,
    PRECISION_MACRO,
    PRECISION_MICRO,
    PRECISION_WEIGHTED,
    RECALL_MACRO,
    RECALL_MICRO,
    RECALL_WEIGHTED,
}

CLASSIFICATION_CLASSWISE_SET = {
    PRECISION_CLASSWISE,
    RECALL_CLASSWISE,
    F1_CLASSWISE,
    IOU_CLASSWISE,
    AVERAGE_PRECISION_CLASSWISE,
    AUC_CLASSWISE,
}

CLASSIFICATION_NONSCALAR_SET = {ACCURACY_TABLE, CONFUSION_MATRIX, CLASSIFICATION_REPORT}

CLASSIFICATION_SET = (
    CLASSIFICATION_SCALAR_SET
    | CLASSIFICATION_NONSCALAR_SET
    | CLASSIFICATION_CLASSWISE_SET
    | CLASSIFICATION_MULTILABEL_SET
)

UNSUPPORTED_CLASSIFICATION_TABULAR_SET = (
    CLASSIFICATION_CLASSWISE_SET
    | CLASSIFICATION_MULTILABEL_SET
    | {CLASSIFICATION_REPORT}
)

CLASSIFICATION_PRIMARY_SET = {
    ACCURACY,
    AUC_WEIGHTED,
    NORM_MACRO_RECALL,
    AVERAGE_PRECISION_WEIGHTED,
    PRECISION_WEIGHTED,
}

CLASSIFICATION_BALANCED_SET = {
    # Metrics for which class_weights are recommended
    BALANCED_ACCURACY,
    AUC_MACRO,
    NORM_MACRO_RECALL,
    AVERAGE_PRECISION_WEIGHTED,
    PRECISION_MACRO,
    F1_MACRO,
    RECALL_MACRO,
}

# Regression Metrics

EXPLAINED_VARIANCE = "explained_variance"
R2_SCORE = "r2_score"
SPEARMAN = "spearman_correlation"
MAPE = "mean_absolute_percentage_error"
MEAN_ABS_ERROR = "mean_absolute_error"
NORM_MEAN_ABS_ERROR = "normalized_mean_absolute_error"
MEDIAN_ABS_ERROR = "median_absolute_error"
NORM_MEDIAN_ABS_ERROR = "normalized_median_absolute_error"
RMSE = "root_mean_squared_error"
NORM_RMSE = "normalized_root_mean_squared_error"
RMSLE = "root_mean_squared_log_error"
NORM_RMSLE = "normalized_root_mean_squared_log_error"
RESIDUALS = "residuals"
PREDICTED_TRUE = "predicted_true"

# Fill Mask Metric
FMPerplexity = "perplexities"

REGRESSION_SCALAR_SET = {
    EXPLAINED_VARIANCE,
    R2_SCORE,
    SPEARMAN,
    MAPE,
    MEAN_ABS_ERROR,
    NORM_MEAN_ABS_ERROR,
    MEDIAN_ABS_ERROR,
    NORM_MEDIAN_ABS_ERROR,
    RMSE,
    NORM_RMSE,
    RMSLE,
    NORM_RMSLE,
}

REGRESSION_NORMALIZED_SET = {
    NORM_MEAN_ABS_ERROR,
    NORM_MEDIAN_ABS_ERROR,
    NORM_RMSE,
    NORM_RMSLE,
}

REGRESSION_NONSCALAR_SET = {RESIDUALS, PREDICTED_TRUE}

REGRESSION_SET = REGRESSION_SCALAR_SET | REGRESSION_NONSCALAR_SET

REGRESSION_PRIMARY_SET = {R2_SCORE, SPEARMAN, NORM_RMSE, NORM_MEAN_ABS_ERROR}

# Forecasting metrics

FORECASTING_MAPE = 'forecast_mean_absolute_percentage_error'
FORECASTING_RESIDUALS = 'forecast_residuals'
FORECASTING_TABLE = 'forecast_table'
FORECASTING_TS_ID_DISTRIBUTION_TABLE = "forecast_time_series_id_distribution_table"

FORECASTING_NONSCALAR_SET = {
    FORECASTING_MAPE,
    FORECASTING_RESIDUALS,
    FORECASTING_TABLE,
    FORECASTING_TS_ID_DISTRIBUTION_TABLE
}


FORECASTING_SET = FORECASTING_NONSCALAR_SET

# Image Classification Metrics

IMAGE_CLASSIFICATION_SET = {ACCURACY}

IMAGE_CLASSIFICATION_MULTILABEL_CLASSIFICATION_SET = {IOU}

# Image Object Detection Metrics
MEAN_AVERAGE_PRECISION = "mean_average_precision"
AVERAGE_PRECISION = "average_precision"
PRECISION = "precision"
RECALL = "recall"
PER_LABEL_METRICS = "per_label_metrics"
IMAGE_LEVEL_BINARY_CLASSIFIER_METRICS = "image_level_binary_classsifier_metrics"
CONFUSION_MATRICES_PER_SCORE_THRESHOLD = "confusion_matrices_per_score_threshold"

IMAGE_OBJECT_DETECTION_SCALAR_SET = {
    MEAN_AVERAGE_PRECISION, RECALL, PRECISION
}

IMAGE_OBJECT_DETECTION_CLASSWISE_SET = {PER_LABEL_METRICS}

IMAGE_OBJECT_DETECTION_NONSCALAR_SET = {
    IMAGE_LEVEL_BINARY_CLASSIFIER_METRICS, CONFUSION_MATRICES_PER_SCORE_THRESHOLD
}

IMAGE_OBJECT_DETECTION_SET = (
    IMAGE_OBJECT_DETECTION_SCALAR_SET | IMAGE_OBJECT_DETECTION_CLASSWISE_SET | IMAGE_OBJECT_DETECTION_NONSCALAR_SET
)

IMAGE_INSTANCE_SEGMENTATION_SCALAR_SET = {
    MEAN_AVERAGE_PRECISION, RECALL, PRECISION
}

IMAGE_INSTANCE_SEGMENTATION_CLASSWISE_SET = {PER_LABEL_METRICS}

IMAGE_INSTANCE_SEGMENTATION_SET = (IMAGE_INSTANCE_SEGMENTATION_SCALAR_SET | IMAGE_INSTANCE_SEGMENTATION_CLASSWISE_SET)

# Video object tracking
IDF1 = "IDF1"
MOTA = "MOTA"
MOTP = "MOTP"
IDSW = "IDSw"
PRCN = "Prcn"
RCll = "Rcll"
FP = "FP"
FN = "FN"
FM = "FM"
ML = "ML"
MT = "MT"
PT = "PT"

VIDEO_MULTI_OBJECT_TRACKING_SCALAR_SET = {
    MOTA, MOTP, IDF1, PRCN, RCll
}

VIDEO_MULTI_OBJECT_TRACKING_NONSCALAR_SET = {
    IDSW, FP, FN, FM, ML, MT, PT
}

VIDEO_MULTI_OBJECT_TRACKING_SET = (
    VIDEO_MULTI_OBJECT_TRACKING_SCALAR_SET | VIDEO_MULTI_OBJECT_TRACKING_NONSCALAR_SET
)

# Text Classification Metrics

TEXT_CLASSIFICATION_SET = {
    ACCURACY,
    AUC_WEIGHTED,
    PRECISION_MICRO,
    PRECISION_WEIGHTED,
}

# Text Classification Multilabel Metrics

TEXT_CLASSIFICATION_MULTILABEL_SET = {
    ACCURACY,
    F1_MACRO,
    F1_MICRO,
}

# Text NER Metrics

TEXT_NER_SET = {
    ACCURACY,
    F1_MACRO,
    F1_MICRO,
    F1_WEIGHTED,
    PRECISION_MACRO,
    PRECISION_MICRO,
    PRECISION_WEIGHTED,
    RECALL_MACRO,
    RECALL_MICRO,
    RECALL_WEIGHTED,
}


QA_NONSCALAR_SET = {
    BERTScore,
    GPTSimilarity,
    GPTCoherence,
    GPTGroundedness,
    GPTFluency,
    GPTRelevance,
}

FILL_MASK_NONSCALAR_SET = {FMPerplexity}

RAG_EVALUATION_NONSCALAR_SET = {
    GroundingScore,
    RetrievalScore,
    GenerationScore,
}

# All Metrics

FULL_SET = (
    CLASSIFICATION_SET
    | REGRESSION_SET
    | IMAGE_OBJECT_DETECTION_SET
    | IMAGE_INSTANCE_SEGMENTATION_SET
    | FORECASTING_NONSCALAR_SET
    | Metric.TRANSLATION_SET
    | Metric.SUMMARIZATION_SET
    | Metric.QA_SET
    | Metric.FILL_MASK_SET
    | Metric.TEXT_GENERATION_SET
    | Metric.CHAT_COMPLETION_SET
    | Metric.RAG_EVALUATION_SET
    | Metric.CODE_GENERATION_SET
)

FULL_CLASSWISE_SET = (
    CLASSIFICATION_CLASSWISE_SET | IMAGE_OBJECT_DETECTION_CLASSWISE_SET | IMAGE_INSTANCE_SEGMENTATION_CLASSWISE_SET
)

FULL_NONSCALAR_SET = (
    CLASSIFICATION_NONSCALAR_SET
    | REGRESSION_NONSCALAR_SET
    | FILL_MASK_NONSCALAR_SET
    | FORECASTING_NONSCALAR_SET
    | IMAGE_OBJECT_DETECTION_NONSCALAR_SET
    | VIDEO_MULTI_OBJECT_TRACKING_NONSCALAR_SET
    | QA_NONSCALAR_SET
    | RAG_EVALUATION_NONSCALAR_SET
    | Metric.CONVERSATION_RAI_SET
)

FULL_SCALAR_SET = (
    CLASSIFICATION_SCALAR_SET
    | REGRESSION_SCALAR_SET
    | Metric.SCALAR_CODE_GENERATION_SET
    | IMAGE_OBJECT_DETECTION_SCALAR_SET
    | IMAGE_INSTANCE_SEGMENTATION_SCALAR_SET
    | VIDEO_MULTI_OBJECT_TRACKING_SCALAR_SET
)

METRICS_TASK_MAP = {
    CLASSIFICATION: CLASSIFICATION_SET,
    REGRESSION: REGRESSION_SET,
    FORECASTING: FORECASTING_SET,
    IMAGE_CLASSIFICATION: IMAGE_CLASSIFICATION_SET,
    IMAGE_CLASSIFICATION_MULTILABEL: IMAGE_CLASSIFICATION_MULTILABEL_CLASSIFICATION_SET,
    IMAGE_MULTI_LABEL_CLASSIFICATION: IMAGE_CLASSIFICATION_MULTILABEL_CLASSIFICATION_SET,
    IMAGE_OBJECT_DETECTION: IMAGE_OBJECT_DETECTION_SET,
    IMAGE_INSTANCE_SEGMENTATION: IMAGE_INSTANCE_SEGMENTATION_SET,
    TEXT_CLASSIFICATION: TEXT_CLASSIFICATION_SET,
    TEXT_CLASSIFICATION_MULTILABEL: TEXT_CLASSIFICATION_MULTILABEL_SET,
    TEXT_NER: TEXT_NER_SET,
    TRANSLATION: Metric.TRANSLATION_SET,
    SUMMARIZATION: Metric.SUMMARIZATION_SET,
    QUESTION_ANSWERING: Metric.QA_SET,
    FILL_MASK: Metric.FILL_MASK_SET,
    TEXT_GENERATION: Metric.TEXT_GENERATION_SET,
    CHAT_COMPLETION: Metric.CHAT_COMPLETION_SET,
    RAG_EVALUATION: Metric.RAG_EVALUATION_SET,
    CODE_GENERATION: Metric.CODE_GENERATION_SET,
}

SAMPLE_WEIGHTS_UNSUPPORTED_SET = {
    SPEARMAN,
    WEIGHTED_ACCURACY,
    MEDIAN_ABS_ERROR,
    NORM_MEDIAN_ABS_ERROR,
}

# Time Metrics

TRAIN_TIME = "train time"
FIT_TIME = "fit_time"
PREDICT_TIME = "predict_time"

ALL_TIME = {TRAIN_TIME, FIT_TIME, PREDICT_TIME}

FULL_SCALAR_SET_TIME = FULL_SCALAR_SET | ALL_TIME

# Schema Types

# These types will be removed when the artifact-backed
# metrics are defined with protobuf
# Do not use these constants except in artifact-backed metrics
SCHEMA_TYPE_ACCURACY_TABLE = "accuracy_table"
SCHEMA_TYPE_FORECAST_HORIZON_TABLE = "forecast_horizon_table"
SCHEMA_TYPE_CONFUSION_MATRIX = "confusion_matrix"
SCHEMA_TYPE_CLASSIFICATION_REPORT = "classification_report"
SCHEMA_TYPE_RESIDUALS = "residuals"
SCHEMA_TYPE_PREDICTIONS = "predictions"
SCHEMA_TYPE_MAPE = "mape_table"
SCHEMA_TYPE_DISTRIBUTION_TABLE = "forecast_time_series_id_distribution_table"

# Ranges

SCORE_UPPER_BOUND = sys.float_info.max

MULTILABEL_PREDICTION_THRESHOLD = 0.5

CLASSIFICATION_RANGES = {
    ACCURACY: (0.0, 1.0),
    WEIGHTED_ACCURACY: (0.0, 1.0),
    NORM_MACRO_RECALL: (0.0, 1.0),
    BALANCED_ACCURACY: (0.0, 1.0),
    LOG_LOSS: (0.0, SCORE_UPPER_BOUND),
    AUC_BINARY: (0.0, 1.0),
    AUC_MACRO: (0.0, 1.0),
    AUC_MICRO: (0.0, 1.0),
    AUC_WEIGHTED: (0.0, 1.0),
    F1_BINARY: (0.0, 1.0),
    F1_MACRO: (0.0, 1.0),
    F1_MICRO: (0.0, 1.0),
    F1_WEIGHTED: (0.0, 1.0),
    PRECISION_BINARY: (0.0, 1.0),
    PRECISION_MACRO: (0.0, 1.0),
    PRECISION_MICRO: (0.0, 1.0),
    PRECISION_WEIGHTED: (0.0, 1.0),
    RECALL_BINARY: (0.0, 1.0),
    RECALL_MACRO: (0.0, 1.0),
    RECALL_MICRO: (0.0, 1.0),
    RECALL_WEIGHTED: (0.0, 1.0),
    AVERAGE_PRECISION_BINARY: (0.0, 1.0),
    AVERAGE_PRECISION_MACRO: (0.0, 1.0),
    AVERAGE_PRECISION_MICRO: (0.0, 1.0),
    AVERAGE_PRECISION_WEIGHTED: (0.0, 1.0),
    ACCURACY_TABLE: (np.nan, np.nan),
    CONFUSION_MATRIX: (np.nan, np.nan),
    MATTHEWS_CORRELATION: (-1.0, 1.0),
    IOU: (0.0, 1.0),
    IOU_MICRO: (0.0, 1.0),
    IOU_MACRO: (0.0, 1.0),
    IOU_WEIGHTED: (0.0, 1.0),
    CLASSIFICATION_REPORT: (np.nan, np.nan),
    PRECISION_CLASSWISE: (np.nan, np.nan),
    RECALL_CLASSWISE: (np.nan, np.nan),
    F1_CLASSWISE: (np.nan, np.nan),
    IOU_CLASSWISE: (np.nan, np.nan),
    AVERAGE_PRECISION_CLASSWISE: (np.nan, np.nan),
    AUC_CLASSWISE: (np.nan, np.nan),
}

REGRESSION_RANGES = {
    EXPLAINED_VARIANCE: (-SCORE_UPPER_BOUND, 1.0),
    R2_SCORE: (-1.0, 1.0),  # Clipped at -1 for Miro
    SPEARMAN: (-1.0, 1.0),
    MEAN_ABS_ERROR: (0.0, SCORE_UPPER_BOUND),
    NORM_MEAN_ABS_ERROR: (0.0, 1),  # Intentionally clipped at 1 for Miro
    MEDIAN_ABS_ERROR: (0.0, SCORE_UPPER_BOUND),
    NORM_MEDIAN_ABS_ERROR: (0.0, 1),  # Intentionally clipped at 1 for Miro
    RMSE: (0.0, SCORE_UPPER_BOUND),
    NORM_RMSE: (0.0, 1),  # Intentionally clipped at 1 for Miro
    RMSLE: (0.0, SCORE_UPPER_BOUND),
    NORM_RMSLE: (0.0, 1),  # Intentionally clipped at 1 for Miro
    MAPE: (0.0, SCORE_UPPER_BOUND),
    RESIDUALS: (np.nan, np.nan),
    PREDICTED_TRUE: (np.nan, np.nan),
}

RANGES_TASK_MAP = {
    CLASSIFICATION: CLASSIFICATION_RANGES,
    REGRESSION: REGRESSION_RANGES,
}

# Objectives

MAXIMIZE = "maximize"
MINIMIZE = "minimize"
NA = "NA"

OBJECTIVES = {MAXIMIZE, MINIMIZE, NA}

CLASSIFICATION_OBJECTIVES = {
    ACCURACY: MAXIMIZE,
    WEIGHTED_ACCURACY: MAXIMIZE,
    NORM_MACRO_RECALL: MAXIMIZE,
    BALANCED_ACCURACY: MAXIMIZE,
    LOG_LOSS: MINIMIZE,
    AUC_BINARY: MAXIMIZE,
    AUC_MACRO: MAXIMIZE,
    AUC_MICRO: MAXIMIZE,
    AUC_WEIGHTED: MAXIMIZE,
    F1_BINARY: MAXIMIZE,
    F1_MACRO: MAXIMIZE,
    F1_MICRO: MAXIMIZE,
    F1_WEIGHTED: MAXIMIZE,
    PRECISION_BINARY: MAXIMIZE,
    PRECISION_MACRO: MAXIMIZE,
    PRECISION_MICRO: MAXIMIZE,
    PRECISION_WEIGHTED: MAXIMIZE,
    RECALL_BINARY: MAXIMIZE,
    RECALL_MACRO: MAXIMIZE,
    RECALL_MICRO: MAXIMIZE,
    RECALL_WEIGHTED: MAXIMIZE,
    AVERAGE_PRECISION_BINARY: MAXIMIZE,
    AVERAGE_PRECISION_MACRO: MAXIMIZE,
    AVERAGE_PRECISION_MICRO: MAXIMIZE,
    AVERAGE_PRECISION_WEIGHTED: MAXIMIZE,
    ACCURACY_TABLE: NA,
    CONFUSION_MATRIX: NA,
    TRAIN_TIME: MINIMIZE,
    MATTHEWS_CORRELATION: MAXIMIZE,
    IOU: MAXIMIZE,
    IOU_MICRO: MAXIMIZE,
    IOU_MACRO: MAXIMIZE,
    IOU_WEIGHTED: MAXIMIZE,
    CLASSIFICATION_REPORT: NA,
    PRECISION_CLASSWISE: NA,
    RECALL_CLASSWISE: NA,
    F1_CLASSWISE: NA,
    IOU_CLASSWISE: NA,
    AVERAGE_PRECISION_CLASSWISE: NA,
    AUC_CLASSWISE: NA,
}

REGRESSION_OBJECTIVES = {
    EXPLAINED_VARIANCE: MAXIMIZE,
    R2_SCORE: MAXIMIZE,
    SPEARMAN: MAXIMIZE,
    MEAN_ABS_ERROR: MINIMIZE,
    NORM_MEAN_ABS_ERROR: MINIMIZE,
    MEDIAN_ABS_ERROR: MINIMIZE,
    NORM_MEDIAN_ABS_ERROR: MINIMIZE,
    RMSE: MINIMIZE,
    NORM_RMSE: MINIMIZE,
    RMSLE: MINIMIZE,
    NORM_RMSLE: MINIMIZE,
    MAPE: MINIMIZE,
    RESIDUALS: NA,
    PREDICTED_TRUE: NA,
    TRAIN_TIME: MINIMIZE,
}

# Note: using the same objectives as regression as both of them are having same metrics
FORECASTING_OBJECTIVES = REGRESSION_OBJECTIVES

IMAGE_CLASSIFICATION_OBJECTIVES = {
    ACCURACY: MAXIMIZE,
}

IMAGE_CLASSIFICATION_MULTILABEL_OBJECTIVES = {
    IOU: MAXIMIZE,
}

IMAGE_OBJECT_DETECTION_OBJECTIVES = {
    MEAN_AVERAGE_PRECISION: MAXIMIZE,
}

TEXT_CLASSIFICATION_OBJECTIVES = {
    ACCURACY: MAXIMIZE,
    AUC_WEIGHTED: MAXIMIZE,
    PRECISION_MICRO: MAXIMIZE,
    PRECISION_WEIGHTED: MAXIMIZE,
}

TEXT_CLASSIFICATION_MULTILABEL_OBJECTIVES = {
    ACCURACY: MAXIMIZE,
    F1_MACRO: MAXIMIZE,
    F1_MICRO: MAXIMIZE,
}

TEXT_NER_OBJECTIVES = {
    ACCURACY: MAXIMIZE,
    F1_MICRO: MAXIMIZE,
    PRECISION_MICRO: MAXIMIZE,
    RECALL_MICRO: MAXIMIZE,
}

TRANSLATION_OBJECTIVES = {
    Metric.TranslationBleu_1: MAXIMIZE,
    Metric.TranslationBleu_2: MAXIMIZE,
    Metric.TranslationBleu_3: MAXIMIZE,
    Metric.TranslationBleu_4: MAXIMIZE,
}

SUMMARIZATION_OBJECTIVES = {
    Metric.SummarizationRouge1: MAXIMIZE,
    Metric.SummarizationRouge2: MAXIMIZE,
    Metric.SummarizationRougeL: MAXIMIZE,
    Metric.SummarizationRougeLsum: MAXIMIZE,
}

QUESTION_ANSWERING_OBJECTIVES = {
    Metric.QAExactMatch: MAXIMIZE,
    Metric.QAF1Score: MAXIMIZE,
    Metric.BERTScore: MAXIMIZE,
    Metric.GPTSimilarity: MAXIMIZE,
    Metric.GPTCoherence: MAXIMIZE,
    Metric.GPTGroundedness: MAXIMIZE,
    Metric.GPTFluency: MAXIMIZE,
    Metric.GPTRelevance: MAXIMIZE,
}

FILL_MASK_OBJECTIVES = {
    Metric.FMPerplexity: MINIMIZE,
}

TEXT_GENERATION_OBJECTIVES = {
    Metric.SummarizationRouge1: MAXIMIZE,
    Metric.SummarizationRouge2: MAXIMIZE,
    Metric.SummarizationRougeL: MAXIMIZE,
    Metric.SummarizationRougeLsum: MAXIMIZE,

    Metric.TranslationBleu_1: MAXIMIZE,
    Metric.TranslationBleu_2: MAXIMIZE,
    Metric.TranslationBleu_3: MAXIMIZE,
    Metric.TranslationBleu_4: MAXIMIZE,
}

CHAT_COMPLETION_OBJECTIVES = {
    Metric.SummarizationRouge1: MAXIMIZE,
    Metric.SummarizationRouge2: MAXIMIZE,
    Metric.SummarizationRougeL: MAXIMIZE,
    Metric.SummarizationRougeLsum: MAXIMIZE,

    Metric.TranslationBleu_1: MAXIMIZE,
    Metric.TranslationBleu_2: MAXIMIZE,
    Metric.TranslationBleu_3: MAXIMIZE,
    Metric.TranslationBleu_4: MAXIMIZE,

    Metric.QAExactMatch: MAXIMIZE,
    Metric.QAF1Score: MAXIMIZE,
}

RAG_EVALUATION_OBJECTIVES = {
    Metric.GroundingScore: MAXIMIZE,
    Metric.RetrievalScore: MAXIMIZE,
    Metric.GenerationScore: MAXIMIZE,
}

CODE_GENERATION_OBJECTIVES = {
    Metric.CodeGenerationPassRateScore: MAXIMIZE
}

FULL_OBJECTIVES = {
    **CLASSIFICATION_OBJECTIVES,
    **REGRESSION_OBJECTIVES,
    **FORECASTING_OBJECTIVES,
    **IMAGE_CLASSIFICATION_OBJECTIVES,
    **IMAGE_CLASSIFICATION_MULTILABEL_OBJECTIVES,
    **IMAGE_OBJECT_DETECTION_OBJECTIVES,
    **TEXT_CLASSIFICATION_MULTILABEL_OBJECTIVES,
    **TEXT_CLASSIFICATION_OBJECTIVES,
    **TEXT_NER_OBJECTIVES,
    **TRANSLATION_OBJECTIVES,
    **SUMMARIZATION_OBJECTIVES,
    **QUESTION_ANSWERING_OBJECTIVES,
    **FILL_MASK_OBJECTIVES,
    **TEXT_GENERATION_OBJECTIVES,
    **CHAT_COMPLETION_OBJECTIVES,
    **RAG_EVALUATION_OBJECTIVES,
    **CODE_GENERATION_OBJECTIVES,
}

OBJECTIVES_TASK_MAP = {
    CLASSIFICATION: CLASSIFICATION_OBJECTIVES,
    REGRESSION: REGRESSION_OBJECTIVES,
    FORECASTING: FORECASTING_OBJECTIVES,
    IMAGE_CLASSIFICATION: IMAGE_CLASSIFICATION_OBJECTIVES,
    IMAGE_CLASSIFICATION_MULTILABEL: IMAGE_CLASSIFICATION_MULTILABEL_OBJECTIVES,
    IMAGE_MULTI_LABEL_CLASSIFICATION: IMAGE_CLASSIFICATION_MULTILABEL_OBJECTIVES,
    IMAGE_OBJECT_DETECTION: IMAGE_OBJECT_DETECTION_OBJECTIVES,
    IMAGE_INSTANCE_SEGMENTATION: IMAGE_OBJECT_DETECTION_OBJECTIVES,
    TEXT_CLASSIFICATION: TEXT_CLASSIFICATION_OBJECTIVES,
    TEXT_CLASSIFICATION_MULTILABEL: TEXT_CLASSIFICATION_MULTILABEL_OBJECTIVES,
    TEXT_NER: TEXT_NER_OBJECTIVES,
    TRANSLATION: TRANSLATION_OBJECTIVES,
    SUMMARIZATION: SUMMARIZATION_OBJECTIVES,
    QUESTION_ANSWERING: QUESTION_ANSWERING_OBJECTIVES,
    FILL_MASK: FILL_MASK_OBJECTIVES,
    TEXT_GENERATION: TEXT_GENERATION_OBJECTIVES,
    CHAT_COMPLETION: CHAT_COMPLETION_OBJECTIVES,
    RAG_EVALUATION: RAG_EVALUATION_OBJECTIVES,
    CODE_GENERATION: CODE_GENERATION_OBJECTIVES,
}

# Pipeline constants

DEFAULT_PIPELINE_SCORE = float("NaN")

# Metric restrictions

MINIMUM_METRIC_NAME_LENGTH = 3  # This is an arbitrary limit for validation.
MAXIMUM_METRIC_NAME_LENGTH = (
    50  # Check Run History restrictions before extending this limit.
)


class TelemetryConstants:
    """Define telemetry constants."""

    COMPONENT_NAME = "automl"

    # Spans that are shared across different child run types
    # Formatting for span name: <Component_Name>.<Span_Name> e.g. automl.Training
    SPAN_FORMATTING = "{}.{}"
    # RunInitialization: Initialize common variables across remote wrappers
    RUN_INITIALIZATION = "RunInitialization"
    RUN_INITIALIZATION_USER_FACING = "Initializing AutoML run"
    # DataFetch: Setup and Featurization data fetching
    DATA_PREPARATION = "DataPrep"
    DATA_PREPARATION_USER_FACING = "Preparing input data"
    # LoadCachedData: Training and Model Explain load data from cache
    LOAD_CACHED_DATA = "LoadCachedData"
    LOAD_CACHED_DATA_USER_FACING = "Loading cached data"

    # Spans specific to Setup Run
    FEATURIZATION_STRATEGY = "FeaturizationStrategy"
    FEATURIZATION_STRATEGY_USER_FACING = "Deciding featurization actions"
    DATA_VALIDATION = "DataValidation"
    DATA_VALIDATION_USER_FACING = "Validating input data"

    # Spans specific to Featurization
    FEATURIZATION = "Featurization"
    FEATURIZATION_USER_FACING = "Featurizing data"

    # Spans specific to Training
    LOAD_ONNX_CONVERTER = "LoadOnnxConverter"
    LOAD_ONNX_CONVERTER_USER_FACING = "Loading ONNX converter"
    RUN_TRAINING = "RunE2ETraining"
    RUN_TRAINING_USER_FACING = "Running E2E training"
    TRAINING = "Training"
    TRAINING_USER_FACING = "Training model"
    VALIDATION = "Validation"
    VALIDATION_USER_FACING = "Validating model quality"
    METRIC_AND_SAVE_MODEL_NAME = "SaveModelArtifacts"
    METRIC_AND_SAVE_MODEL_USER_FACING = "Uploading run output metadata"
    ONNX_CONVERSION = "OnnxConversion"
    ONNX_CONVERSION_USER_FACING = "Converting to ONNX model"
    LOG_METRICS = "LogMetrics"
    LOG_METRICS_USER_FACING = "Logging run metrics"

    # Spans specific to Training
    BATCH_TRAINING = "BatchTraining"
    BATCH_TRAINING_USER_FACING = "Training model in batch"

    # Spans specific to Model Explain
    MODEL_EXPLANATION = "ModelExplanation"
    MODEL_EXPLANATION_USER_FACING = "Running model explainability"

    # Local Managed
    ScriptRunFinalizing = "ScriptRunFinalizing"
    ScriptRunStarting = "ScriptRunStarting"

    # Spans specific to Confidence Interval
    COMPUTE_CONFIDENCE_METRICS = "ComputeConfidenceMetrics"
    BOOTSTRAP_STEPS = "BootstrapSteps"

    # TODO: refactor / organize below and use compatible telemetry constants for activity logger and RH tracing
    COMPUTE_METRICS_NAME = "ComputeMetrics"
    DOWNLOAD_ENSEMBLING_MODELS = "DownloadEnsemblingModels"
    DOWNLOAD_MODEL = "DownloadModel"
    FAILURE = "Failure"
    FIT_ITERATION_NAME = "FitIteration"
    GET_BEST_CHILD = "GetBestChild"
    GET_CHILDREN = "GetChildren"
    GET_OUTPUT = "GetOutput"
    GET_PIPELINE_NAME = "GetPipeline"
    OUTPUT_NAME = "Output"
    PACKAGES_CHECK = "PackagesCheck"
    PRE_PROCESS_NAME = "PreProcess"
    PREDICT_NAME = "Predict"
    REGISTER_MODEL = "RegisterModel"
    REMOTE_INFERENCE = "RemoteInference"
    RUN_CV_MEAN_NAME = "RunCVMean"
    RUN_CV_NAME = "RunCV"
    RUN_ENSEMBLING_NAME = "RunEnsembling"
    RUN_NAME = "Run"
    RUN_PIPELINE_NAME = "RunPipeline"
    RUN_TRAIN_FULL_NAME = "TrainFull"
    RUN_TRAIN_VALID_NAME = "TrainValid"
    SUCCESS = "Success"
    TIME_FIT_ENSEMBLE_NAME = "TimeFitEnsemble"
    TIME_FIT_INPUT = "TimeFitInput"
    TIME_FIT_NAME = "TimeFit"


class _TimeSeriesInternal:
    """Define the time series constants"""

    DUMMY_GRAIN_COLUMN = '_automl_dummy_grain_col'
    DUMMY_TARGET_COLUMN = '_automl_target_col'
    HORIZON_NAME = 'horizon_origin'
    FORECAST_ORIGIN_COLUMN_NAME = '_automl_forecast_origin'


class ChatCompletionConstants:
    """Define chatcompletion metric constants"""

    CONVERSATION_NUMBER = "conversation_number"
    TURN_NUMBER = "turn_number"
    # rag_evaluation constants
    SCORE_PER_TURN = "score_per_turn"
    SCORE_PER_CONVERSATION = "score_per_conversation"
    REASON = "reason"
    # chat completion persona strings
    USER_PERSONA = "user"
    ASSISTANT_PERSONA = "assistant"


class CodeGenerationConstants:
    """constants needed for code generation metrics"""
    CODE_GENERATION_PREFIX = "pass@"
