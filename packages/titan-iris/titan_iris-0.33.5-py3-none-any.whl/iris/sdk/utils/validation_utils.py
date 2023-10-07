"""This file contains the dataset validation functions for the Iris package."""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import os
from pathlib import Path
import pandas as pd
import ast


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                   Validation Utils                                                   #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


# Returns the filenames of valid files, if no valid file is found, None is returned
# [train_filename, val_filename]
def check_filenames(src, train_split_name=None, val_split_name=None):
    """Gets the filenames for the training and validation datasets.

    Args:
        src (str): Directory of the dataset
        train_split_name (str): Filename of the training dataset (optional)
        val_split_name (str): Filename of the validation dataset (optional)

    Returns: [train_filename: str or None, val_filename: str or None]

    """
    train_filename = None
    val_filename = None
    # Catches if you accidentally put a tilde in quotes:
    if src[0] == "~":
        src = os.path.expanduser(src)
    # If path does not exist
    if not Path(src).is_dir():
        print("Path not found")
        return [None, None]

    namelist = os.listdir(src)

    # Train file check
    if train_split_name:
        if train_split_name in namelist:
            train_filename = train_split_name
    else:
        for file in namelist:
            if "train" in file and file.endswith(".csv"):
                train_filename = file

    # Validation file check
    if val_split_name:
        if val_split_name in namelist:
            val_filename = val_split_name

    else:
        for file in namelist:
            if "val" in file and file.endswith(".csv"):
                val_filename = file

    return [train_filename, val_filename]


def get_df(directory, train_file, validation_file):
    """Gets the dataframes for the training and validation datasets.

    Args:
        directory (str): Directory of the dataset
        train_file (str): Filename of the training dataset
        validation_file (str): Filename of the validation dataset

    Returns: [df_train: pandas.DataFrame or None, df_validation: pandas.DataFrame or None]

    """
    try:
        # Read datasets using pandas and returns dataframes
        df_train = pd.read_csv(os.path.join(directory, train_file))
        df_validation = pd.read_csv(os.path.join(directory, validation_file))
        if set(df_train.columns) != set(df_validation.columns):
            print("Columns in training and validation datasets do not match")
            return [None, None]

    except pd.errors.EmptyDataError:
        print("Empty CSV file")
        return [None, None]
    except pd.errors.ParserError:
        print("Error parsing CSV file")
        return [None, None]
    except PermissionError:
        print("Permission denied when reading file")
        return [None, None]
    except MemoryError:
        print("Insufficient memory to load file")
        return [None, None]
    return [df_train, df_validation]


def get_rows(df_train, df_validation):
    """Gets the number of rows in the training and validation datasets.

    Args:
        df_train (pandas.DataFrame): Training dataset
        df_validation (pandas.DataFrame): Validation dataset

    Returns: [train_rows: int or None, val_rows: int or None]

    """
    try:
        train_rows = len(df_train.index)
        val_rows = len(df_validation.index)
    except AttributeError:
        print("Invalid dataframe")
        return [None, None]
    return [train_rows, val_rows]


def get_columns(df_train, df_validation):
    """Gets the number of columns in the training and validation datasets.

    Args:
        df_train (pandas.DataFrame): Training dataset
        df_validation (pandas.DataFrame): Validation dataset

    Returns: [train_columns: int or None, val_columns: int or None]

    """
    try:
        train_columns = list(df_train.columns.values)
    except AttributeError:
        print("Invalid dataframe")
        return [None, None]
    return train_columns


# Outputs for dataset validation functions for each task
# [isValid: Boolean, infoMessage: String]
def valid_for_question_answering(df_train, df_validation):
    """Checks if the dataset is valid for question answering.

    Args:
        df_train (pandas.DataFrame): Training dataset
        df_validation (pandas.DataFrame): Validation dataset

    Returns: [isValid: bool, message: str]

    """
    # Check if mandatory columns are present
    if "context" not in df_train.columns or "context" not in df_validation.columns:
        return [False, "Context column does not exist in dataset"]
    if "question" not in df_train.columns or "question" not in df_validation.columns:
        return [False, "Question column does not exist in dataset"]
    if "answers" not in df_train.columns or "answers" not in df_validation.columns:
        return [False, "Answers column does not exist in dataset"]

    for answer_str in df_train["answers"]:
        try:
            # Parse the string into dictionary
            answer = ast.literal_eval(answer_str)
        except (SyntaxError, ValueError):
            return [False, "Error parsing answers column"]
        # Check if 'text' and 'answer_start' keys are in the dictionary
        if not isinstance(answer, dict):
            return [False, "Answers column is not in dictionary format"]
        if "text" not in answer:
            return [False, "text key does not exist in answers column"]
        if "answer_start" not in answer:
            return [False, "answer_start key does not exist in answers column"]
        # Check if 'text' and 'answer_start' values are lists
        if not isinstance(answer["text"], list):
            return [False, "text value is not a list"]
        if not isinstance(answer["answer_start"], list):
            return [False, "answer_start value is not a list"]

    for answer_str in df_validation["answers"]:
        try:
            # Parse the string into dictionary
            answer = ast.literal_eval(answer_str)
        except (SyntaxError, ValueError):
            return [False, "Error parsing answers column"]
        # Check if 'text' and 'answer_start' keys are in the dictionary
        if not isinstance(answer, dict):
            return [False, "Answers column is not in dictionary format"]
        if "text" not in answer:
            return [False, "text key does not exist in answers column"]
        if "answer_start" not in answer:
            return [False, "answer_start key does not exist in answers column"]
        # Check if 'text' and 'answer_start' values are lists
        if not isinstance(answer["text"], list):
            return [False, "text value is not a list"]
        if not isinstance(answer["answer_start"], list):
            return [False, "answer_start value is not a list"]
    return [True, "Dataset is valid"]


def valid_for_sequence_classification(df_train, df_validation):
    """Checks if the dataset is valid for sequence classification.

    Args:
        df_train (pandas.DataFrame): Training dataset
        df_validation (pandas.DataFrame): Validation dataset

    Returns: [isValid: bool, message: str]

    """
    # Label column is mandatory
    if "label" not in df_train.columns or "label" not in df_validation.columns:
        return [False, "Label column does not exist in dataset"]
    # Check if label column is of type int64
    if df_train["label"].dtype != "int64" or df_validation["label"].dtype != "int64":
        return [False, "Label column contains non-integer values"]

    min_label = min(df_train["label"].min(), df_validation["label"].min())
    max_label = max(df_train["label"].max(), df_validation["label"].max())
    unique_labels = pd.concat([df_train, df_validation])["label"].nunique()

    # Negative labels
    if min_label < 0:
        return [False, "Label column contains negative values"]
    # Labels do not start from 0
    if min_label > 0:
        return [False, "Minimum label is not 0"]
    # Labels are not consecutive
    if max_label - min_label + 1 != unique_labels:
        return [False, "Label column contains gaps in values"]

    # Check if there is at least one column that is a string
    if len(df_train.select_dtypes(include=["object"]).columns) < 1:
        return [False, "Dataset does not contain any columns that are strings"]

    # Suggested text-fields
    text_fields = df_train.select_dtypes(include=["object"]).columns.tolist()
    suggested_text_fields = "Available text fields: " + (", ").join(text_fields) + ". "

    # Suggested number of labels
    num_labels = max_label - min_label + 1
    suggested_num_labels = "Suggested number of labels: " + str(num_labels)

    return [True, suggested_text_fields + suggested_num_labels]


def valid_for_conditional_language_modelling(df_train, df_validation):
    """Checks if the dataset is valid for conditional language modelling.

    Args:
        df_train (pandas.DataFrame): Training dataset
        df_validation (pandas.DataFrame): Validation dataset

    Returns: [isValid: bool, message: str]

    """
    # Check if there are at least two columns that are not int64
    if len(df_train.select_dtypes(include=["object"]).columns) < 2:
        return [False, "Dataset does not contain at least two columns that are strings"]
    if len(df_validation.select_dtypes(include=["object"]).columns) < 2:
        return [False, "Dataset does not contain at least two columns that are strings"]
    text_fields = df_train.select_dtypes(include=["object"]).columns.tolist()
    suggested_text_fields = "Valid text fields: " + ", ".join(text_fields)
    suggested_text_fields += ". Specify two text fields for conditional language modelling."
    return [True, suggested_text_fields]


def valid_for_unconditional_language_modelling(df_train, df_validation):
    """Checks if the dataset is valid for unconditional language modelling.

    Args:
        df_train (pandas.DataFrame): Training dataset
        df_validation (pandas.DataFrame): Validation dataset

    Returns: [isValid: bool, message: str]

    """
    # Check if there is at least a column that is not int64
    if len(df_train.select_dtypes(include=["object"]).columns) < 1:
        return [False, "Dataset does not contain at least a column that is a string"]
    if len(df_validation.select_dtypes(include=["object"]).columns) < 1:
        return [False, "Dataset does not contain at least a column that is a string"]
    text_fields = df_train.select_dtypes(include=["object"]).columns.tolist()
    suggested_text_fields = "Valid text fields: " + ", ".join(text_fields)
    suggested_text_fields += ". Specify one text field for unconditional language modelling."
    return [True, suggested_text_fields]
