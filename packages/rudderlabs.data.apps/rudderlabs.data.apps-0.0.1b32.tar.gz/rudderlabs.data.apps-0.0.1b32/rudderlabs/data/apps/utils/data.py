#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Utils for data preprocessing."""

import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder

from ..log import get_logger

logger = get_logger(__name__)


def get_onehot_encoder_names(
    onehot_encoder: OneHotEncoder, col_names: list
) -> list:
    """Assigning new column names for the one-hot encoded columns.

    Args:
        onehot_encoder: OneHotEncoder object.
        col_names: List of column names

    Returns:
        list: List of category column names.
    """
    category_names = []
    for col_id, col in enumerate(col_names):
        for value in onehot_encoder.categories_[col_id]:
            category_names.append(f"{col}_{value}")
    return category_names


class NamedColumns(BaseEstimator, TransformerMixin):
    """
    Based on the df passed in in fit, filter / reformat the df in transform so the columns match
    Fill any missing columns with default_value
    """

    def __init__(self, default_value: int = 0):
        self.cols = None
        self.default_value = default_value

    def fit(self, X: pd.DataFrame, y: pd.Series):
        self.cols = X.columns
        return self

    def transform(self, X: pd.DataFrame):
        ret_df = pd.DataFrame(
            self.default_value, index=X.index, columns=self.cols
        )
        for col in self.cols:
            if col in X.columns:
                ret_df[col] = X[col]
        return ret_df
