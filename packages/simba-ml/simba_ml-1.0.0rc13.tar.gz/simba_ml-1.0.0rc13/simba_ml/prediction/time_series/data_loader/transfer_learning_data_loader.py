"""This module provides the dataloader."""
import os
from typing import Tuple

import pandas as pd
import numpy as np
from numpy import typing as npt

from simba_ml.prediction.time_series.config.transfer_learning_pipeline import (
    data_config,
)
from simba_ml.prediction import preprocessing
from simba_ml.prediction.time_series.data_loader import window_generator, splits
from simba_ml.prediction import export


class TransferLearningDataLoader:
    """Loads and preprocesses the data.

    Attributes:
        X_test: the input of the test data
        y_test: the labels for the test data
        train_validation_sets: list of validations sets, one for each ratio of
            synthethic to observed data
    """

    config: data_config.DataConfig
    __X_test: npt.NDArray[np.float64] | None = None
    __y_test: npt.NDArray[np.float64] | None = None
    __train_observed: list[npt.NDArray[np.float64]] | None = None
    __train_synthetic: list[npt.NDArray[np.float64]] | None = None

    def __init__(self, config: data_config.DataConfig) -> None:
        """Inits the DataLoader.

        Args:
            config: the data configuration.
        """
        self.config = config

    def load_data(self) -> Tuple[list[pd.DataFrame], list[pd.DataFrame]]:
        """Loads the data.

        Returns:
            A list of dataframes.
        """
        synthetic = (
            []
            if self.config.synthetic is None
            else preprocessing.read_dataframes_from_csvs(
                os.getcwd() + self.config.synthetic
            )
        )
        observed = (
            []
            if self.config.observed is None
            else preprocessing.read_dataframes_from_csvs(
                os.getcwd() + self.config.observed
            )
        )
        return synthetic, observed

    def prepare_data(self) -> None:
        """This function preprocesses the data."""
        if self.__X_test is not None:  # pragma: no cover
            return  # pragma: no cover
        synthethic_data, observed_data = self.load_data()
        observed_train, observed_test = splits.train_test_split(
            data=observed_data,
            test_split=self.config.test_split,
            input_length=self.config.time_series.input_length,
            split_axis=self.config.split_axis,
        )
        self.__train_synthetic = synthethic_data
        self.__train_observed = observed_train
        self.__X_test, self.__y_test = window_generator.create_window_dataset(
            observed_test, self.config.time_series
        )

    # sourcery skip: snake-case-functions
    @property
    def X_test(self) -> npt.NDArray[np.float64]:
        """The input of the test dataset.

        Returns:
            The input of the test dataset.
        """
        if self.__X_test is None:
            self.prepare_data()
        if self.config.export_path is not None and self.__X_test is not None:
            export.export_batches(
                data=self.__X_test,
                export_path=self.config.export_path,
                features=self.config.time_series.input_features,
                file_name="X_test",
            )
        return self.X_test if self.__X_test is None else self.__X_test

    @property
    def y_test(self) -> npt.NDArray[np.float64]:
        """The output of the test dataset.

        Returns:
            The output of the test dataset.
        """
        if self.__y_test is None:
            self.prepare_data()
            return self.y_test
        return self.__y_test

    @property
    def train_observed(
        self,
    ) -> list[npt.NDArray[np.float64]]:
        """Lists of train sets.

        One set for each ratio.

        Returns:
            A dict containing the train sets.
        """
        if not self.__train_observed:
            self.prepare_data()
            return self.train_observed
        return self.__train_observed

    @property
    def train_synthetic(
        self,
    ) -> list[npt.NDArray[np.float64]]:
        """Lists of train sets.

        One set for each ratio.

        Returns:
            A dict containing the train sets.
        """
        if not self.__train_synthetic:
            self.prepare_data()
            return self.train_synthetic
        return self.__train_synthetic
