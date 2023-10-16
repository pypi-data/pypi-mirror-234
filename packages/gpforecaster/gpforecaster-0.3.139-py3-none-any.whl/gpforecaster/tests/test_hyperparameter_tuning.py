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

    def test_optimize_hyperparameters_bayesian(self):
        best_hyperparameters = optimize_hyperparameters_bayesian(
            dataset_name=self.dataset_name,
            hierarchical_data=self.data,
            num_trials=3,
            epochs=2,
        )
        self.assertIsNotNone(best_hyperparameters)

    def test_optimize_hyperparameters_bayesian_svg(self):
        best_hyperparameters = optimize_hyperparameters_bayesian(
            dataset_name=self.dataset_name,
            gp_type='svg',
            hierarchical_data=self.data,
            num_trials=2,
            epochs=2,
        )
        self.assertIsNotNone(best_hyperparameters)

    def test_fixed_hyperparameters(self):
        fixed_hparams = {
            "rbf_kernel_lengthscale": 0.0,
            "scale_rbf_kernel_outputscale": 0.0,
            "periodic_kernel_lengthscale": 0.0,
            "scale_periodic_kernel_outputscale": 0.0,
            "m": 0.0,
            "k": 0.0,
            "b": 0.0,
            "scaler_type": "standard",
            "scale_x_values": "True",
            "random_init": "True",
        }
        best_hyperparameters = optimize_hyperparameters_bayesian(
            dataset_name=self.dataset_name,
            hierarchical_data=self.data,
            num_trials=3,
            epochs=2,
            fixed_hyperparameters=fixed_hparams,
        )
        print(best_hyperparameters)
        self.assertIsNotNone(best_hyperparameters)
        # check if the returned hyperparameters match the fixed ones
        for key, value in fixed_hparams.items():
            self.assertEqual(best_hyperparameters[key], value)
