import unittest

import tsaugmentation as tsag

from gpforecaster.model.hyperparameter_tuning import optimize_hyperparameters_bayesian


class TestModel(unittest.TestCase):
    def setUp(self):
        self.dataset_name = "m5"
        self.data = tsag.preprocessing.PreprocessDatasets(
            self.dataset_name, freq="W", test_size=10
        ).apply_preprocess()
        self.n = self.data["predict"]["n"]
        self.s = self.data["train"]["s"]

    def test_optimize_hyperparameters_bayesian(self):
        best_hyperparameters = optimize_hyperparameters_bayesian(
            dataset_name=self.dataset_name,
            hierarchical_data=self.data,
            num_trials=3,
            epochs=2,
        )
        self.assertIsNotNone(best_hyperparameters)
