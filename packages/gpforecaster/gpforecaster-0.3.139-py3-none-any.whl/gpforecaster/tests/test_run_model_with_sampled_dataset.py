import unittest

from tsaugmentation.preprocessing.subsample_dataset import CreateGroups

from gpforecaster.model.gpf import GPF
from gpforecaster.visualization import plot_predictions_vs_original


class TestModel(unittest.TestCase):
    def setUp(self):
        self.dataset_name = "prison"
        self.input_dir = "./results/gpf/"
        self.groups = CreateGroups(
            dataset_name=self.dataset_name, sample_perc=0.9, freq="Q"
        ).read_subsampled_groups()
        groups_orig = CreateGroups(
            dataset_name=self.dataset_name, freq="Q"
        ).read_original_groups()
        self.n = self.groups["predict"]["n"]
        self.s = self.groups["train"]["s"]
        self.gpf = GPF(self.dataset_name, self.groups, gp_type="exact90")
        self.gpf_scaled = GPF(
            self.dataset_name,
            self.groups,
            gp_type="exact90",
            scale_x_values=True,
            input_dir=self.input_dir,
        )
        self.groups["predict"] = groups_orig["predict"]

        self.groups_prison_small = CreateGroups(
            dataset_name=self.dataset_name, sample_perc=0.4, freq="Q"
        ).read_subsampled_groups()
        self.gpf_prison_small = GPF(
            self.dataset_name,
            self.groups_prison_small,
            gp_type="exact40",
            input_dir=self.input_dir,
        )
        self.groups_tourism_small = CreateGroups(
            dataset_name=self.dataset_name, sample_perc=0.4, freq="M"
        ).read_subsampled_groups()
        self.gpf_tourism_small = GPF(
            self.dataset_name,
            self.groups_tourism_small,
            gp_type="exact40",
            input_dir=self.input_dir,
        )

    def test_calculate_metrics_dict(self):
        model, like = self.gpf.train(epochs=2)
        preds, preds_scaled = self.gpf.predict(model, like)
        plot_predictions_vs_original(
            dataset=self.dataset_name,
            prediction_mean=preds[0],
            prediction_std=preds[1],
            origin_data=self.gpf.original_data,
            x_complete=self.gpf.complete_x,
            x_original=self.gpf.train_x.numpy(),
            x_test=self.gpf.test_x.numpy(),
            inducing_points=self.gpf.inducing_points,
            n_series_to_plot=8,
            gp_type=self.gpf.gp_type,
        )
        res = self.gpf.metrics(preds[0], preds[1])
        self.assertLess(res["mase"]["bottom"], 20)

    def test_calculate_metrics_dict_x_scaled(self):
        model, like = self.gpf_scaled.train(epochs=2)
        preds, preds_scaled = self.gpf_scaled.predict(model, like)
        plot_predictions_vs_original(
            dataset=self.dataset_name,
            prediction_mean=preds[0],
            prediction_std=preds[1],
            origin_data=self.gpf.original_data,
            x_complete=self.gpf.complete_x,
            x_original=self.gpf.train_x.numpy(),
            x_test=self.gpf.test_x.numpy(),
            inducing_points=self.gpf.inducing_points,
            n_series_to_plot=8,
            gp_type=self.gpf.gp_type,
        )
        res = self.gpf.metrics(preds[0], preds[1])
        self.assertLess(res["mase"]["bottom"], 20)

    def test_subsample_prison_small(self):
        model, like = self.gpf_prison_small.train(
            epochs=2, n_splits=2, no_validation=True, cross_validation=False
        )
        preds, preds_scaled = self.gpf_prison_small.predict(model, like)
        plot_predictions_vs_original(
            dataset=self.dataset_name,
            prediction_mean=preds[0],
            prediction_std=preds[1],
            origin_data=self.gpf_prison_small.original_data,
            x_complete=self.gpf_prison_small.complete_x,
            x_original=self.gpf_prison_small.train_x.numpy(),
            x_test=self.gpf_prison_small.test_x.numpy(),
            inducing_points=self.gpf_prison_small.inducing_points,
            n_series_to_plot=8,
            gp_type=self.gpf_prison_small.gp_type,
        )
        res = self.gpf_prison_small.metrics(preds[0], preds[1])
        self.gpf_prison_small.store_results(
            preds[0], res_measure="mean", res_type="fitpred"
        )
        self.gpf_prison_small.store_results(
            preds[0], res_measure="mean", res_type="pred"
        )
        self.gpf_prison_small.store_results(
            preds[1], res_measure="std", res_type="fitpred"
        )
        self.gpf_prison_small.store_results(
            preds[1], res_measure="std", res_type="pred"
        )

    def test_subsample_tourism_small(self):
        model, like = self.gpf_tourism_small.train(
            epochs=2, n_splits=2, no_validation=True, cross_validation=False
        )
        preds, preds_scaled = self.gpf_tourism_small.predict(model, like)
        plot_predictions_vs_original(
            dataset=self.dataset_name,
            prediction_mean=preds[0],
            prediction_std=preds[1],
            origin_data=self.gpf_tourism_small.original_data,
            x_complete=self.gpf_tourism_small.complete_x,
            x_original=self.gpf_tourism_small.train_x.numpy(),
            x_test=self.gpf_tourism_small.test_x.numpy(),
            inducing_points=self.gpf_tourism_small.inducing_points,
            n_series_to_plot=8,
            gp_type=self.gpf_tourism_small.gp_type,
        )
        res = self.gpf_tourism_small.metrics(preds[0], preds[1])
        self.gpf_prison_small.store_results(
            preds[0], res_measure="mean", res_type="fitpred"
        )
        self.gpf_tourism_small.store_results(
            preds[0], res_measure="mean", res_type="pred"
        )
        self.gpf_tourism_small.store_results(
            preds[1], res_measure="std", res_type="fitpred"
        )
        self.gpf_tourism_small.store_results(
            preds[1], res_measure="std", res_type="pred"
        )
