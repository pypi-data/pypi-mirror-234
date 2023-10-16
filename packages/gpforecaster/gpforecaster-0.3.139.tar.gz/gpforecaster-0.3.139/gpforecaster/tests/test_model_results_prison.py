import pickle
import unittest

import tsaugmentation as tsag

from gpforecaster.model.gpf import GPF
from gpforecaster.visualization import plot_predictions_vs_original


class TestModel(unittest.TestCase):
    def setUp(self):
        self.dataset_name = "prison"
        self.data = tsag.preprocessing.PreprocessDatasets(
            self.dataset_name, freq="Q"
        ).apply_preprocess()
        self.data_minmax = tsag.preprocessing.PreprocessDatasets(
            self.dataset_name, freq="Q"
        ).apply_preprocess()
        self.data_sparse = tsag.preprocessing.PreprocessDatasets(
            self.dataset_name, freq="Q"
        ).apply_preprocess()
        self.n = self.data["predict"]["n"]
        self.s = self.data["train"]["s"]
        self.res_type = "fitpred"
        self.res_measure = "mean"
        self.input_dir = "./results/gpf/"
        self.gpf = GPF(
            self.dataset_name,
            self.data,
            input_dir=self.input_dir,
            scaler_type="standard",
            scale_x_values=True,
        )
        self.gpf_sparse = GPF(
            self.dataset_name,
            self.data_sparse,
            input_dir=self.input_dir,
            scaler_type="standard",
            scale_x_values=True,
            gp_type="sparse",
        )
        self.gpf_minmax = GPF(
            self.dataset_name,
            self.data_minmax,
            input_dir=self.input_dir,
            scaler_type="minmax",
            scale_x_values=True,
            gp_type="exact",
        )

    def test_train_scaled_no_validation_or_cross(self):
        model, like = self.gpf.train(
            epochs=2,
            cross_validation=False,
            no_validation=True,
        )
        self.gpf.plot_losses()
        preds, preds_scaled = self.gpf.predict(model, like)
        plot_predictions_vs_original(
            dataset=self.dataset_name,
            prediction_mean=preds[0],
            prediction_std=preds[1],
            origin_data=self.gpf.original_data,
            x_original=self.gpf.train_x,
            x_test=self.gpf.test_x,
            x_complete=self.gpf.complete_x,
            inducing_points=self.gpf.inducing_points,
            n_series_to_plot=8,
            gp_type=self.gpf.gp_type,
        )
        self.assertIsNotNone(model)

    def test_train_scaled_no_validation_or_cross_zero_hyper(self):
        hyperparameters = {
            "scaler_type": "standard",
            "scale_x_values": True,
            "random_init": True,
            "lr": 0.01,
            "weight_decay": 1e-4,
            "scheduler_type": "cosine",
            "gamma_rate": 0.8545262009273771,
            "patience": 30,
            "rbf_kernel_lengthscale": 0.0,
            "scale_rbf_kernel_outputscale": 0.0,
            "periodic_kernel_lengthscale": 0.0,
            "scale_periodic_kernel_outputscale": 0.0,
            "m": 0.0,
            "k": 0.0,
            "b": 0.0,
            "like_noise": 0.5,
            "mean_type": "piecewise",
            "learn_like_noise": True,
        }
        model, like = self.gpf.train(
            epochs=2,
            hyperparameters=hyperparameters,
            cross_validation=False,
            no_validation=True,
        )
        self.gpf.plot_losses()
        preds, preds_scaled = self.gpf.predict(model, like)
        plot_predictions_vs_original(
            dataset=self.dataset_name,
            prediction_mean=preds[0],
            prediction_std=preds[1],
            origin_data=self.gpf.original_data,
            x_original=self.gpf.train_x,
            x_test=self.gpf.test_x,
            x_complete=self.gpf.complete_x,
            inducing_points=self.gpf.inducing_points,
            n_series_to_plot=8,
            gp_type=self.gpf.gp_type,
        )
        self.assertIsNotNone(model)

    def test_train_scaled_no_validation_or_cross_zero_hyper_specific_hyperparams(self):
        hyperparameters = {
            "scaler_type": "standard",
            "scale_x_values": True,
            "random_init": True,
            "lr": 0.01,
            "weight_decay": 1e-4,
            "scheduler_type": "cosine",
            "gamma_rate": 0.8545262009273771,
            "patience": 30,
            "rbf_kernel_lengthscale": 0.0,
            "scale_rbf_kernel_outputscale": 0.0,
            "periodic_kernel_lengthscale": 0.0,
            "scale_periodic_kernel_outputscale": 0.0,
            "m": 0.0,
            "k": 0.0,
            "b": 0.0,
            "like_noise": 0.5,
            "mean_type": "zero",
            "learn_like_noise": False,
        }
        model, like = self.gpf.train(
            epochs=11,
            hyperparameters=hyperparameters,
            cross_validation=False,
            no_validation=True,
        )
        self.gpf.plot_losses()
        preds, preds_scaled = self.gpf.predict(model, like)
        plot_predictions_vs_original(
            dataset=self.dataset_name,
            prediction_mean=preds[0],
            prediction_std=preds[1],
            origin_data=self.gpf.original_data,
            x_original=self.gpf.train_x,
            x_test=self.gpf.test_x,
            inducing_points=self.gpf.inducing_points,
            x_complete=self.gpf.complete_x,
            n_series_to_plot=8,
            gp_type=self.gpf.gp_type,
        )
        self.assertIsNotNone(model)

    def test_train_scaled_no_validation_or_cross_minmax(self):
        model, like = self.gpf_minmax.train(
            epochs=2,
            cross_validation=False,
            no_validation=True,
        )
        self.gpf_minmax.plot_losses()
        preds, preds_scaled = self.gpf_minmax.predict(model, like)
        plot_predictions_vs_original(
            dataset=self.dataset_name,
            prediction_mean=preds[0],
            prediction_std=preds[1],
            origin_data=self.gpf_minmax.original_data,
            x_original=self.gpf_minmax.train_x,
            x_test=self.gpf_minmax.test_x,
            x_complete=self.gpf_minmax.complete_x,
            inducing_points=self.gpf_minmax.inducing_points,
            n_series_to_plot=8,
            gp_type=self.gpf_minmax.gp_type,
        )
        self.assertIsNotNone(model)

    def test_train_scaled_no_validation_or_cross_sparse(self):
        model, like = self.gpf_sparse.train(
            epochs=2,
            cross_validation=False,
            no_validation=True,
        )
        self.gpf_sparse.plot_losses()
        preds, preds_scaled = self.gpf_sparse.predict(model, like)
        plot_predictions_vs_original(
            dataset=self.dataset_name,
            prediction_mean=preds[0],
            prediction_std=preds[1],
            origin_data=self.gpf_sparse.original_data,
            x_original=self.gpf_sparse.train_x,
            x_test=self.gpf_sparse.test_x,
            x_complete=self.gpf_sparse.complete_x,
            inducing_points=self.gpf_sparse.inducing_points,
            n_series_to_plot=8,
            gp_type=self.gpf_sparse.gp_type,
        )
        self.assertIsNotNone(model)

    def test_predict_shape(self):
        model, like = self.gpf.train(epochs=2)
        preds, preds_scaled = self.gpf.predict(model, like)
        self.assertTrue(preds[0].shape == (self.n, self.s))

    def test_results_interval(self):
        model, like = self.gpf.train(epochs=2)
        preds, preds_scaled = self.gpf.predict(model, like)
        res = self.gpf.metrics(preds[0], preds[1])
        self.assertLess(res["mase"]["bottom"], 40)

    def test_wall_time(self):
        model, like = self.gpf.train(epochs=2)
        preds, preds_scaled = self.gpf.predict(model, like)
        res = self.gpf.metrics(preds[0], preds[1])
        self.assertLess(res["wall_time"]["wall_time_total"], 100)

    def test_output_results(self):
        model, like = self.gpf.train(epochs=2)
        preds, preds_scaled = self.gpf.predict(model, like)
        res = self.gpf.metrics(preds[0], preds[1])
        self.gpf.store_results(preds[0], res_measure="mean", res_type="fitpred")
        self.gpf.store_results(preds[0], res_measure="mean", res_type="pred")
        self.gpf.store_results(preds[1], res_measure="std", res_type="fitpred")
        self.gpf.store_results(preds[1], res_measure="std", res_type="pred")
        with open(
            f"{self.gpf.input_dir}results_{self.res_type}_{self.res_measure}_gp_{self.gpf.gp_type}_cov_{self.gpf.dataset}_{self.gpf.model_version}.pickle",
            "rb",
        ) as handle:
            output_res = pickle.load(file=handle)
        self.assertTrue(output_res.shape == (48, 32))

    def test_plot_loss_xvalidation(self):
        model, like = self.gpf.train(epochs=2)
        self.gpf.plot_losses()

    def test_plot_loss(self):
        model, like = self.gpf.train(epochs=2, cross_validation=False)
        self.gpf.plot_losses()

    def test_no_validation(self):
        model, like = self.gpf.train(
            epochs=2, cross_validation=False, no_validation=True
        )
        self.gpf.plot_losses()
