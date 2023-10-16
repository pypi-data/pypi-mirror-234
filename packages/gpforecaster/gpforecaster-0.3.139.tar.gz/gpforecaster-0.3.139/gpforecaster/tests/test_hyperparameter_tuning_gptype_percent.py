import unittest

import tsaugmentation as tsag

from gpforecaster.model.hyperparameter_tuning import optimize_hyperparameters_bayesian


class TestModel(unittest.TestCase):
    def setUp(self):
        self.dataset_name = "prison"
        self.data = tsag.preprocessing.PreprocessDatasets(
            self.dataset_name, freq="Q"
        ).apply_preprocess()
        self.n = self.data["predict"]["n"]
        self.s = self.data["train"]["s"]

    def test_optimize_hyperparameters_bayesian_gptype(self):
        best_hyperparameters = optimize_hyperparameters_bayesian(
            gp_type="svg",
            dataset_name=self.dataset_name,
            hierarchical_data=self.data,
            num_trials=2,
            epochs=2
        )
        self.assertIsNotNone(best_hyperparameters)

    def test_optimize_hyperparameters_bayesian_percent(self):
        best_hyperparameters = optimize_hyperparameters_bayesian(
            gp_type="exact90",
            dataset_name=self.dataset_name,
            hierarchical_data=self.data,
            num_trials=2,
            epochs=2
        )
        self.assertIsNotNone(best_hyperparameters)
