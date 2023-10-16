import unittest
import tsaugmentation as tsag
from gpforecaster.model.gpf import GPF
import shutil


class TestModel(unittest.TestCase):

    def setUp(self):
        self.preproc = tsag.preprocessing.PreprocessDatasets('tourism', test_size=304, freq='M')
        self.data = self.preproc._tourism()
        self.n = self.data['predict']['n']
        self.s = self.data['train']['s']
        self.gpf = GPF(dataset='tourism', groups=self.data)

    def test_results_tourism(self):
        hyperparameters = {
            "random_init": False,
            "mean_type": "piecewise",
            "lr": 0.009780855468469227,
            "weight_decay": 0.0008766086393281662,
            "scheduler_type": "none",
            "gamma_rate": 0.6025559024359668,
            "patience": 35,
            "rbf_kernel_lengthscale": 0.01439444726438651,
            "scale_rbf_kernel_outputscale": 1.9689838416839822,
            "periodic_kernel_lengthscale": 0.01,
            "scale_periodic_kernel_outputscale": 1.1430250042319041,
            "m": 0.07332075308223542,
            "k": 0.0001,
            "b": 0.024003264600885563,
            "like_noise": 0.9603120312078957,
            "learn_like_noise": True,
        }

        hyperparameters_init = {
            "scaler_type": "standard",
            "scale_x_values": True,
        }

        # Load dataset
        dataset_name = "tourism"
        data = tsag.preprocessing.PreprocessDatasets(
            dataset_name, freq="M", test_size=304
        ).apply_preprocess()

        # Initialize GP Forecaster
        gpf = GPF(
            dataset_name,
            data,
            hyperparameters_init["scaler_type"],
            hyperparameters_init["scale_x_values"],
        )

        # Training the model
        model, likelihood = gpf.train(
            epochs=2,
            hyperparameters=hyperparameters,
            cross_validation=False,
            no_validation=True,
            n_splits=2,
            early_stopping=True,
        )


    def test_results_mean_and_prediction_interval(self):
        model, like = self.gpf.train(epochs=2)
        preds, preds_scaled = self.gpf.predict(model, like)
        res = self.gpf.metrics(preds[0], preds[1])

        # Test shape of results
        self.assertTrue(res['mase']['bottom_ind'].shape == (self.s, ))
        self.assertTrue(res['CRPS']['bottom_ind'].shape == (self.s, ))
        self.assertTrue(res['rmse']['bottom_ind'].shape == (self.s, ))

    def test_results_mean_and_prediction_interval_without_storing_results(self):
        self.gpf = GPF(dataset='tourism', groups=self.data)
        model, like = self.gpf.train(epochs=2)
        preds, preds_scaled = self.gpf.predict(model, like)
        res = self.gpf.metrics(preds[0], preds[1])

        # Test shape of results
        self.assertTrue(res['mase']['bottom_ind'].shape == (self.s, ))
        self.assertTrue(res['CRPS']['bottom_ind'].shape == (self.s, ))
        self.assertTrue(res['rmse']['bottom_ind'].shape == (self.s, ))

        # Test shape of predictions
        # Test number of objects predicted and stored
        self.assertTrue(len(res) == 4)

