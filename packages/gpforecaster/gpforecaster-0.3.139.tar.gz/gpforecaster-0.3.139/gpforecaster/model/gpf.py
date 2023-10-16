from datetime import timedelta
import os
import time
import psutil
from typing import Dict, Union, Tuple, Optional, Any

import numpy as np
import torch
import gpytorch
import pickle
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from copy import deepcopy

from gpytorch.models import IndependentModelList
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from gpytorch.likelihoods import GaussianLikelihood
from gpytorch.likelihoods import LikelihoodList
from gpytorch.mlls import SumMarginalLogLikelihood
from gpytorch.kernels import (
    ScaleKernel,
    RBFKernel,
    PeriodicKernel,
)
from sktime.performance_metrics.forecasting import MeanAbsoluteScaledError
from sklearn.model_selection import TimeSeriesSplit

from gpforecaster import __version__
from gpforecaster.utils.logger import Logger
from gpforecaster.model.gp import ExactGPModel, SparseGPModel, SvgGPModel
from gpforecaster.model.mlls import SumVariationalELBO
from gpforecaster.model.mean_functions import (
    PiecewiseLinearMean,
    ConstantMean,
    ZeroMean,
)
from gpforecaster.results.calculate_metrics import CalculateResultsBottomUp


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class GPF:
    """
    A class for training and forecasting hierarchical time series datasets with Gaussian Process models.

    Parameters:
        dataset: Name of the dataset.
        groups: Dictionary containing the train and predict groups.
        input_dir: Directory where input files are stored
        n_samples: Number of samples to draw from the posterior distribution
        store_prediction_samples: Whether to store the prediction samples
        store_prediction_points: Whether to store the prediction points.
        log_dir: Directory where log files are stored. Default is '.'.
        inducing_points_perc: Percentage of inducing points to use.
        gp_type: Type of GP: exact, sparse, etc

    Attributes:
        dataset (str): Name of the dataset.
        groups (dict): Dictionary containing the train and predict groups.
        input_dir (str): Directory where input files are stored.
        timer_start (float): Start time of the training process.
        wall_time_train (float): Wall time for training.
        wall_time_predict (float): Wall time for prediction.
        wall_time_total (float): Total wall time.
        n_samples (int): Number of samples to draw from the posterior distribution.
        store_prediction_samples (bool): Whether to store the prediction samples.
        store_prediction_points (bool): Whether to store the prediction points.
        train_x (torch.Tensor): Tensor with the training data input.
        train_y (torch.Tensor): Tensor with the training data output.
        test_x (torch.Tensor): Tensor with the test data input.
        test_y (torch.Tensor): Tensor with the test data output.
        original_data (np.ndarray): Orignal dataset
        original_data_transformed (np.ndarray): Orignal dataset transformed
        n_train (int): Number of training samples
        n_test (int): Number of testing samples
        s (int): Number of time series
        losses (list): List of losses during training.
        val_losses (list): List of validation losses during training.
        model_version (str): Version of the model.
        logger_train (Logger): Logger for the training process.
        logger_metrics (Logger): Logger for the metrics.
    """

    def __init__(
        self,
        dataset: str,
        groups: dict,
        input_dir: str = "./",
        n_samples: int = 500,
        store_prediction_samples: bool = False,
        store_prediction_points: bool = False,
        log_dir: str = ".",
        device: str = "cpu",
        inducing_points_perc: float = 0.75,
        gp_type: str = "exact",
        scaler_type: str = "standard",
        scale_x_values: bool = False,
        random_inducing_points: bool = True,
    ):
        self.dataset = dataset
        self.groups = deepcopy(groups)
        self.input_dir = input_dir
        self.scaler_type = scaler_type
        self.scale_x_values = scale_x_values
        self.timer_start = time.time()
        self.wall_time_train = None
        self.wall_time_predict = None
        self.wall_time_total = None
        if isinstance(self.groups["predict"]["x_values"], torch.Tensor):
            self.last_x = max(self.groups["predict"]["x_values"].cpu()) + 1
        else:
            self.last_x = max(self.groups["predict"]["x_values"]) + 1
        self.complete_x = None
        self.original_data = self.groups["predict"]["data_matrix"]
        self.device = torch.device(device)

        if self.scaler_type == "minmax":
            self.scaler = MinMaxScaler()
        else:
            self.scaler = StandardScaler()

        self.scaler_x_values = StandardScaler()

        self._preprocess()
        self.n_samples = n_samples
        self.store_prediction_samples = store_prediction_samples
        self.store_prediction_points = store_prediction_points

        self._create_directory_if_not_exists("model_weights")

        self.train_x = self.groups["train"]["x_values"]
        self.train_y = self.groups["train"]["data"].to(torch.float32).to(self.device)

        self.test_x = self.groups["predict"]["x_values"][-self.groups["h"] :]
        self.test_y = (
            self.groups["predict"]["data_matrix"][-self.groups["h"] :]
            .to(torch.float32)
            .to(self.device)
        )

        self.original_data_transformed = self.groups["predict"]["data_matrix"]

        self.n_train = self.groups["train"]["n"]
        self.n_predict = self.groups["predict"]["n"]
        self.s = self.groups["train"]["s"]

        self.gp_type = gp_type
        if random_inducing_points:
            self.inducing_points = torch.rand(
                int(inducing_points_perc * self.n_train)
            ).reshape(-1, 1)
        elif self.scale_x_values:
            self.inducing_points = self._convert_and_transform_data(
                torch.rand(
                    int(inducing_points_perc * self.n_train), dtype=torch.float32
                )
                * self.n_train,
                self.scaler_x_values,
                fit=False,
            )
        else:
            self.inducing_points = (
                torch.rand(
                    int(inducing_points_perc * self.n_train), dtype=torch.float32
                )
                * self.n_train
            ).to(self.device)

        self.losses = []
        self.val_losses = []
        self.test_losses = []
        self.avg_loss = []
        self.avg_val_loss = []
        self.avg_test_loss = []
        self.mll = None

        self.changepoints = None

        self.val_loss_ma_window = []  # Moving Average window for validation loss
        self.ma_window_size = 10  # Size of the window

        self.mase = MeanAbsoluteScaledError(multioutput="raw_values")
        self.seasonality = self.groups["seasonality"]
        self.scaled_seasonality = self.seasonality

        self.model_version = __version__

        self.logger_train = Logger(
            "train", dataset=self.dataset, to_file=True, log_dir=log_dir
        )
        self.logger_train.info(f"GP Type: {self.gp_type}")
        self.logger_predict = Logger(
            "predict", dataset=self.dataset, to_file=True, log_dir=log_dir
        )
        self.logger_metrics = Logger(
            "metrics", dataset=self.dataset, to_file=True, log_dir=log_dir
        )

    def _convert_and_transform_data(
        self,
        data: Union[np.ndarray, torch.Tensor, list],
        scaler: Union[StandardScaler, MinMaxScaler, None],
        fit: bool = False,
    ) -> torch.Tensor:
        """
        Convert the input data to a numpy array (if required), fit and/or transform it using the provided scaler,
        and return the transformed data as a tensor on the specified device.
        """
        if isinstance(data, (np.ndarray, list)):
            data_np = np.array(data)
        elif isinstance(data, torch.Tensor):
            data_np = data.cpu().numpy()
        else:
            raise TypeError("Unsupported data type for conversion.")

        if data_np.ndim == 1:
            data_np = data_np.reshape(-1, 1)

        if scaler is not None:
            if fit:
                scaler.fit(data_np)
            data_np = scaler.transform(data_np)

        return torch.from_numpy(data_np).to(torch.float32).to(self.device)

    def _preprocess(
        self,
    ):
        """
        Preprocess the input data by fitting and transforming it using scalers.
        The transformed data is converted to tensors and stored on the specified device.
        """

        def to_device(tensor, device):
            if tensor.device != device:
                return tensor.to(device)
            return tensor

        complete_x = torch.from_numpy(np.arange(self.last_x)).to(dtype=torch.float32)

        for key in ["train", "predict"]:
            if self.scale_x_values:
                self.groups[key]["x_values"] = self._convert_and_transform_data(
                    self.groups[key]["x_values"],
                    self.scaler_x_values,
                    fit=(key == "train"),
                )
            else:
                tensor = self._convert_and_transform_data(
                    self.groups[key]["x_values"], None, fit=False
                )
                self.groups[key]["x_values"] = to_device(tensor, self.device)

        if self.scale_x_values:
            original_period = self.groups["seasonality"]
            original_values = np.array([0, original_period])
            transformed_values = self.scaler_x_values.transform(
                original_values.reshape(-1, 1)
            )
            self.scaled_seasonality = transformed_values[1] - transformed_values[0]
            self.complete_x = to_device(
                tensor=self._convert_and_transform_data(
                    complete_x, self.scaler_x_values, fit=False
                ),
                device=self.device,
            )
        else:
            self.complete_x = to_device(tensor=complete_x, device=self.device)

        self.groups["train"]["data"] = self._convert_and_transform_data(
            self.groups["train"]["data"], self.scaler, fit=True
        )
        self.groups["predict"]["data_matrix"] = self._convert_and_transform_data(
            self.groups["predict"]["data_matrix"], self.scaler, fit=False
        )

    def hierarchical_data_summary(self, bottom_series=None, test_data=False):
        groups_names = list(self.groups["train"]["groups_names"].keys())
        if bottom_series is None:
            if test_data:
                bottom_series = self.test_y
                n_samples = self.groups["h"]
            else:
                bottom_series = self.groups["train"]["data"]
                n_samples = self.groups["train"]["n"]
        else:
            n_samples = bottom_series.shape[0]

        summary = {
            "total": torch.sum(
                torch.tensor(bottom_series, dtype=torch.float32, device=self.device),
                dim=1,
            ),
            "groups": {},
            "group_ele": {},
            "bottom": torch.tensor(
                bottom_series, dtype=torch.float32, device=self.device
            ),
        }

        for group in groups_names:
            n_elements_group = self.groups["train"]["groups_names"][group].shape[0]
            group_elements = self.groups["train"]["groups_names"][group]
            groups_idx = self.groups["train"]["groups_idx"][group]

            data_g = (
                torch.zeros((n_samples, n_elements_group))
                .to(torch.float32)
                .to(self.device)
            )

            for group_idx, element_name in enumerate(group_elements):
                group_element_active = torch.tensor(
                    np.where(groups_idx == group_idx, 1, 0).reshape((1, -1)),
                    dtype=torch.float32,
                    device=self.device,
                )
                data_g[:, group_idx] = (
                    torch.sum(group_element_active * summary["bottom"], dim=1)
                    .to(torch.float32)
                    .to(self.device)
                )

                if element_name not in summary["group_ele"]:
                    summary["group_ele"][element_name] = (
                        torch.sum(group_element_active * summary["bottom"], dim=1)
                        .to(torch.float32)
                        .to(self.device)
                    )

            summary["groups"][group] = (
                torch.sum(data_g, dim=1).to(torch.float32).to(self.device)
            )

        return summary

    def concatenate_arrays(self, nested_dict):
        total = nested_dict["total"]
        group_arrays = [
            group_array.to(self.device)
            for group_array in nested_dict["groups"].values()
        ]
        group_ele_arrays = [
            group_ele_array.to(self.device)
            for group_ele_array in nested_dict["group_ele"].values()
        ]
        bottom_arrays = [series.to(self.device) for series in nested_dict["bottom"].T]

        concatenated_array = torch.column_stack(
            [total] + group_arrays + group_ele_arrays + bottom_arrays
        ).to(self.device)

        concatenated_array_upper = torch.column_stack(
            [total] + group_arrays + group_ele_arrays
        ).to(self.device)

        concatenated_array_bottom = torch.column_stack(bottom_arrays).to(self.device)

        return concatenated_array, concatenated_array_upper, concatenated_array_bottom

    def split_train_val(self, data, num_val):
        val_size = num_val
        train_data = data[:-val_size]
        val_data = data[-val_size:]
        return train_data.to(self.device), val_data.to(self.device)

    def _build_mixtures(self):
        """
        Build the mixtures matrix.

        Returns:
            known_mixtures (np.ndarray): The mixtures matrix.
            n_groups (int): number of groups.

        Example:
                Group1     |   Group2
            GP1, GP2, GP3  | GP1, GP2
            0  , 1  , 1    | 0  , 1
            1  , 0  , 0    | 1  , 0
            0  , 1, , 1    | 0  , 1
            1  , 0  , 1    | 1  , 0
        """
        idxs = []
        for k, val in self.groups["train"]["groups_idx"].items():
            idxs.append(val)

        idxs_t = np.array(idxs).T

        n_groups = np.sum(
            np.fromiter(self.groups["train"]["groups_n"].values(), dtype="int32")
        )
        known_mixtures = np.zeros((self.groups["train"]["s"], n_groups))
        k = 0
        for j in range(self.groups["train"]["g_number"]):
            for i in range(np.max(idxs_t[:, j]) + 1):
                idx_to_1 = np.where(idxs_t[:, j] == i)
                known_mixtures[:, k][idx_to_1] = 1
                k += 1

        top_level = np.ones((known_mixtures.shape[0], 1))
        known_mixtures = np.concatenate((known_mixtures, top_level), axis=1)
        n_groups += 1

        return known_mixtures, n_groups

    def _build_cov_matrices(
        self,
        random_init: bool,
        rbf_kernel_lengthscale,
        scale_rbf_kernel_outputscale,
        periodic_kernel_lengthscale,
        scale_periodic_kernel_outputscale,
    ):
        """
        Build the covariance matrices.

        Parameters:
            mixtures (np.ndarray): The mixtures matrix.

        Returns:
            covs (list): List of covariance functions.
            known_mixtures (np.ndarray): The mixtures matrix.
            n_groups (int): number of groups.
        """
        known_mixtures, n_groups = self._build_mixtures()
        covs = []
        for i in range(1, n_groups + 1):
            if random_init:
                # RBF kernel
                rbf_kernel = RBFKernel()
                scale_rbf_kernel = ScaleKernel(rbf_kernel)

                # Periodic Kernel
                periodic_kernel = PeriodicKernel()
                periodic_kernel.period_length = torch.tensor([self.scaled_seasonality])
                scale_periodic_kernel = ScaleKernel(periodic_kernel)
            else:
                # RBF kernel
                rbf_kernel = RBFKernel()
                rbf_kernel.lengthscale = rbf_kernel_lengthscale
                scale_rbf_kernel = ScaleKernel(rbf_kernel)
                scale_rbf_kernel.outputscale = scale_rbf_kernel_outputscale

                # Periodic Kernel
                periodic_kernel = PeriodicKernel()
                periodic_kernel.period_length = torch.tensor([self.scaled_seasonality])
                periodic_kernel.lengthscale = periodic_kernel_lengthscale
                scale_periodic_kernel = ScaleKernel(periodic_kernel)
                scale_periodic_kernel.outputscale = scale_periodic_kernel_outputscale

            # Cov Matrix
            cov = scale_rbf_kernel + scale_periodic_kernel
            covs.append(cov)

        return covs, known_mixtures, n_groups

    def _apply_mixture_cov_matrices(
        self,
        random_init: bool,
        rbf_kernel_lengthscale,
        scale_rbf_kernel_outputscale,
        periodic_kernel_lengthscale,
        scale_periodic_kernel_outputscale,
    ):
        """
        Apply the mixture covariance matrices and create the final list of covariance functions.

        Returns:
            mixed_covs (cov): The list of mixture covariance functions.
        """
        covs, known_mixtures, n_groups = self._build_cov_matrices(
            random_init,
            rbf_kernel_lengthscale=rbf_kernel_lengthscale,
            scale_rbf_kernel_outputscale=scale_rbf_kernel_outputscale,
            periodic_kernel_lengthscale=periodic_kernel_lengthscale,
            scale_periodic_kernel_outputscale=scale_periodic_kernel_outputscale,
        )

        # apply mixtures to covariances
        selected_covs = []
        mixed_covs = []
        for i in range(self.groups["train"]["s"]):
            mixture_weights = known_mixtures[i]
            for w_ix in range(n_groups):
                w = mixture_weights[w_ix]
                if w == 1.0:
                    selected_covs.append(covs[w_ix])
            mixed_cov = selected_covs[0]
            for cov in range(1, len(selected_covs)):
                mixed_cov += selected_covs[
                    cov
                ]  # because GP(cov1 + cov2) = GP(cov1) + GP(cov2)
            mixed_covs.append(mixed_cov)
            selected_covs = []

        return mixed_covs

    def _build_model(
        self,
        x: torch.Tensor,
        y: torch.Tensor,
        rbf_kernel_lengthscale,
        scale_rbf_kernel_outputscale,
        periodic_kernel_lengthscale,
        scale_periodic_kernel_outputscale,
        hyperparameters,
    ) -> Tuple[list[GaussianLikelihood], list[ExactGPModel]]:
        """
        Build the model.

        Parameters:
            x: Measures
            y: Observations.

        Returns:
            likelihood_list: List of GP models.
            model_list: List of likelihoods.
        """

        mixed_covs = self._apply_mixture_cov_matrices(
            hyperparameters["random_init"],
            rbf_kernel_lengthscale=rbf_kernel_lengthscale,
            scale_rbf_kernel_outputscale=scale_rbf_kernel_outputscale,
            periodic_kernel_lengthscale=periodic_kernel_lengthscale,
            scale_periodic_kernel_outputscale=scale_periodic_kernel_outputscale,
        )

        k = torch.tensor([[hyperparameters["k"]]])
        m = torch.tensor([[hyperparameters["m"]]])
        b = torch.tensor([hyperparameters["b"]])

        like_noise = torch.tensor([hyperparameters["like_noise"]])

        model_list = []
        likelihood_list = []
        for i in range(self.groups["train"]["s"]):
            likelihood = GaussianLikelihood()
            likelihood.noise = like_noise
            if not hyperparameters["learn_like_noise"]:
                likelihood.noise_covar.raw_noise.requires_grad_(False)
            likelihood_list.append(likelihood)
            if hyperparameters["mean_type"] == "constant":
                mean_func = ConstantMean(
                    constant=hyperparameters.get("mean_constant", 0.0)
                )
            elif hyperparameters["mean_type"] == "zero":
                mean_func = ZeroMean()
            else:
                mean_func = PiecewiseLinearMean(
                    changepoints=self.changepoints,
                    device=self.device,
                    m=m,
                    k=k,
                    b=b,
                    random_init=hyperparameters["random_init"],
                )
            if self.gp_type.startswith("exact"):
                model_list.append(
                    ExactGPModel(
                        train_x=x,
                        train_y=y[:, i],
                        likelihood=likelihood_list[i],
                        cov=mixed_covs[i],
                        mean_module=mean_func,
                    )
                )
            elif self.gp_type == "sparse":
                model_list.append(
                    SparseGPModel(
                        train_x=x,
                        train_y=y[:, i],
                        likelihood=likelihood_list[i],
                        cov=mixed_covs[i],
                        mean_module=mean_func,
                        inducing_points=self.inducing_points,
                    )
                )
            elif self.gp_type == "svg":
                model_list.append(
                    SvgGPModel(
                        train_x=x,
                        train_y=y[:, i],
                        likelihood=likelihood_list[i],
                        cov=mixed_covs[i],
                        mean_module=mean_func,
                        inducing_points=self.inducing_points,
                    )
                )

        return likelihood_list, model_list

    def early_stopping(self, val_losses, patience: int):
        if not val_losses:
            return False

        losses = list(val_losses)
        losses.reverse()
        non_decreasing = 0
        for x, y in zip(losses, losses[1:]):
            if np.round(x, 3) >= np.round(y, 3):
                non_decreasing += 1
            else:
                break
        return non_decreasing >= patience, non_decreasing

    @staticmethod
    def _create_scheduler(
        scheduler_type: str, optimizer: torch.optim.Optimizer, epochs: int, gamma: float
    ) -> Optional[Any]:
        """
        Creates a scheduler for the learning rate of an optimizer.

        Parameters
            scheduler_type: The type of scheduler to use. One of 'step', 'exponential', 'cosine', or 'none'.
            optimizer: The optimizer for which to create the scheduler.
            epochs: The number of epochs to train the model.

        Returns
            Optional
                The created scheduler, or None if `scheduler_type` is 'none'.
        """
        if scheduler_type == "step":
            scheduler = torch.optim.lr_scheduler.StepLR(
                optimizer, step_size=10, gamma=gamma
            )
        elif scheduler_type == "exponential":
            scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=gamma)
        elif scheduler_type == "cosine":
            scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
                optimizer, T_max=epochs
            )
        else:
            scheduler = None
        return scheduler

    @staticmethod
    def _create_standard_optimizer(
        model, lr: float, weight_decay: float
    ) -> torch.optim.Adam:
        optimizer = torch.optim.Adam(
            model.parameters(), lr=lr, weight_decay=weight_decay
        )  # Includes GaussianLikelihood parameters
        return optimizer

    def _train_loop_iteration(
        self,
        epoch: int,
        model,
        likelihood,
        train_y,
        train_y_upper,
        train_y_bottom,
        val_x,
        val_y,
        val_y_upper,
        val_y_bottom,
        test_x,
        test_y,
        test_y_upper,
        test_y_bottom,
        mll: gpytorch.mlls.MarginalLogLikelihood,
        standard_optimizer: Optional[torch.optim.Adam] = None,
        scheduler: Optional[Any] = None,
        early_stopping: bool = True,
    ) -> Tuple[
        float,
        Optional[float],
        Optional[float],
        Tuple[float, float, float],
        Tuple[float, float, float],
        dict,
    ]:
        """
        Perform a single iteration of the training loop.

        Parameters:
            epoch: The current epoch number.
            model: The model to be trained.
            likelihood: The likelihood function for the model.
            mll: The marginal log-likelihood function.
            standard_optimizer: The optimizer used for training. Defaults to None.
            scheduler: The learning rate scheduler. Defaults to None.
            early_stopping: Perform early stopping. Defaults to True.
            early_stopping: Perform early stopping. Defaults to True.
            early_stopping: Perform early stopping. Defaults to True.

        Returns:
            Tuple[float, Optional[float]]: Tuple containing the current loss value and validation loss value (if applicable).
        """
        standard_optimizer.zero_grad()

        output = model(*model.train_inputs)
        loss = -mll(output, model.train_targets)

        val_loss = None
        test_loss = None
        val_loss_all = None
        test_loss_all = None

        if early_stopping:
            model.eval()
            likelihood.eval()
            ((val_loss, test_loss), val_loss_all, test_loss_all) = self.validate(
                model=model,
                val_x=val_x,
                val_y=val_y,
                val_y_upper=val_y_upper,
                val_y_bottom=val_y_bottom,
                train_y=train_y,
                train_y_upper=train_y_upper,
                train_y_bottom=train_y_bottom,
                test_x=test_x,
                test_y=test_y,
                test_y_upper=test_y_upper,
                test_y_bottom=test_y_bottom,
                likelihood=likelihood,
            )

            model.train()
            likelihood.train()

        loss.backward()
        standard_optimizer.step()

        if scheduler:
            scheduler.step()

        if epoch % 30 == 0:
            self._log_memory()

        return (
            loss.item(),
            val_loss,
            test_loss,
            val_loss_all,
            test_loss_all,
            model.state_dict(),
        )

    def _log_memory(self):
        process = psutil.Process(os.getpid())
        mem = process.memory_info().rss / (1024**3)
        self.logger_train.info(f"train used {mem:.3f} GB of RAM")

    def train(
        self,
        hyperparameters: Dict = None,
        epochs: int = 10,
        early_stopping: bool = True,
        cross_validation: bool = True,
        no_validation: bool = False,
        verbose: bool = True,
        n_splits: int = 3,
    ) -> Tuple[Optional[IndependentModelList], Optional[LikelihoodList]]:
        """
        Train the model.

        Parameters:
            lr: Learning rate.
            epochs: Number of epochs
            early_stopping: Perform early stopping
            cross_validation: Perform cross-validation
            patience: Parameter to early stopping
            verbose: Print outputs when training
            n_splits: Number of splits for cross-validation

        Returns:
            tuple: Tuple containing the trained model and the likelihood.
        """
        if not hyperparameters:
            hyperparameters = {
                "scaler_type": "standard",
                "scale_x_values": True,
                "random_init": False,
                "lr": 0.01,
                "weight_decay": 1e-4,
                "scheduler_type": "cosine",
                "gamma_rate": 0.8545262009273771,
                "patience": 30,
                "rbf_kernel_lengthscale": 0.051934857223072153,
                "scale_rbf_kernel_outputscale": 1.50,
                "periodic_kernel_lengthscale": 0.027828803959297085,
                "scale_periodic_kernel_outputscale": 1.7230943943604067,
                "m": 0.14000406873481058,
                "k": 0.06077252898238386,
                "b": 0.04238281999573798,
                "like_noise": 0.5,
                "mean_type": "piecewise",
                "learn_like_noise": True,
            }

        n_changepoints = 4
        train_x_cpu = self.train_x.cpu().numpy()
        changepoints = np.linspace(
            min(train_x_cpu), max(train_x_cpu), n_changepoints + 2
        )[1:-1].reshape(
            -1,
        )
        self.changepoints = torch.tensor(
            changepoints, dtype=torch.float32, device=self.device
        )

        rbf_kernel_lengthscale = torch.tensor(
            [hyperparameters["rbf_kernel_lengthscale"]]
        )
        scale_rbf_kernel_outputscale = torch.tensor(
            [hyperparameters["scale_rbf_kernel_outputscale"]]
        )
        periodic_kernel_lengthscale = torch.tensor(
            [hyperparameters["periodic_kernel_lengthscale"]]
        )
        scale_periodic_kernel_outputscale = torch.tensor(
            [hyperparameters["scale_periodic_kernel_outputscale"]]
        )

        hierarchical_data = self.hierarchical_data_summary()
        (
            concatenated_hierarchical_data,
            concatenated_hierarchical_data_upper,
            concatenated_hierarchical_data_bottom,
        ) = self.concatenate_arrays(hierarchical_data)

        if cross_validation:
            tscv = TimeSeriesSplit(n_splits=n_splits, test_size=self.groups["h"])
        else:
            # Just split once for training and validation
            tscv = TimeSeriesSplit(n_splits=2, test_size=self.groups["h"])
        self.val_losses = []
        self.losses = []
        self.test_losses = []

        model = None

        print(
            f"\nStarting training for: \n"
            f"GP type: {self.gp_type}\n"
            f"Dataset: {self.dataset}\n"
        )

        val_losses_upper = []
        val_losses_bottom = []
        test_losses_upper = []
        test_losses_bottom = []
        # Cross-validation loop
        for fold_idx, (train_indices, val_indices) in enumerate(
            tscv.split(self.train_x)
        ):
            # If not cross-validation and because min number of folds for tscv is 2
            # we skip the first one
            if not cross_validation and fold_idx == 0:
                continue
            print(f"\nStarting training for Fold {fold_idx + 1}...\n")
            if no_validation:
                # Possibility to use the whole training dataset to train since
                # there is no real risk of overfitting
                train_x = self.train_x
                train_y = self.train_y
                train_y_split = concatenated_hierarchical_data
                train_y_split_upper = concatenated_hierarchical_data_upper
                train_y_split_bottom = concatenated_hierarchical_data_bottom
            else:
                train_x = self.train_x[train_indices]
                train_y = self.train_y[train_indices]
                train_y_split = concatenated_hierarchical_data[train_indices]
                train_y_split_upper = concatenated_hierarchical_data_upper[
                    train_indices
                ]
                train_y_split_bottom = concatenated_hierarchical_data_bottom[
                    train_indices
                ]

            val_x = self.train_x[val_indices]
            val_y = concatenated_hierarchical_data[val_indices]
            val_y_upper = concatenated_hierarchical_data_upper[val_indices]
            val_y_bottom = concatenated_hierarchical_data_bottom[val_indices]
            test_x = self.test_x
            hierarchical_data_test = self.hierarchical_data_summary(test_data=True)
            (
                test_y,
                test_y_upper,
                test_y_bottom,
            ) = self.concatenate_arrays(hierarchical_data_test)

            likelihood_list, model_list = self._build_model(
                x=train_x,
                y=train_y,
                rbf_kernel_lengthscale=rbf_kernel_lengthscale,
                scale_rbf_kernel_outputscale=scale_rbf_kernel_outputscale,
                periodic_kernel_lengthscale=periodic_kernel_lengthscale,
                scale_periodic_kernel_outputscale=scale_periodic_kernel_outputscale,
                hyperparameters=hyperparameters,
            )

            model = IndependentModelList(*model_list).to(self.device)
            likelihood = LikelihoodList(*likelihood_list).to(self.device)

            self._initialize_mll(model, likelihood)
            model.train()
            likelihood.train()

            optimizer = self._create_standard_optimizer(
                model, hyperparameters["lr"], hyperparameters["weight_decay"]
            )
            scheduler = self._create_scheduler(
                hyperparameters["scheduler_type"],
                optimizer,
                epochs,
                hyperparameters["gamma_rate"],
            )

            fold_losses = []
            fold_val_losses = []
            fold_test_losses = []

            best_val_loss = float("inf")
            best_state_dict = None

            fold_val_losses_all = []
            fold_test_losses_all = []

            for epoch in range(epochs):
                (
                    loss,
                    val_loss,
                    test_loss,
                    val_loss_all,
                    test_loss_all,
                    state_dict,
                ) = self._train_loop_iteration(
                    epoch,
                    model,
                    likelihood,
                    val_x=val_x,
                    val_y=val_y,
                    val_y_upper=val_y_upper,
                    val_y_bottom=val_y_bottom,
                    test_x=test_x,
                    test_y=test_y,
                    test_y_upper=test_y_upper,
                    test_y_bottom=test_y_bottom,
                    train_y=train_y_split,
                    train_y_upper=train_y_split_upper,
                    train_y_bottom=train_y_split_bottom,
                    mll=self.mll,
                    standard_optimizer=optimizer,
                    scheduler=scheduler,
                    early_stopping=early_stopping,
                )

                # Storing losses per epoch per fold
                fold_losses.append(loss)
                if val_loss is not None:
                    fold_val_losses.append(val_loss)
                    fold_val_losses_all.append(val_loss_all)
                    fold_test_losses.append(test_loss)
                    fold_test_losses_all.append(test_loss_all)

                if verbose:
                    print(
                        f"Fold {fold_idx + 1} - Iter {epoch} - "
                        f"Loss: {np.round(loss, 3)}, "
                        f"Validation Loss: {np.round(val_loss, 3) if val_loss is not None else 'N/A'}, "
                        f"Test Loss: {np.round(test_loss, 3) if test_loss is not None else 'N/A'}\n"
                        f"\tVal Loss:"
                        f" Weighted: {np.round(val_loss_all[0], 3) if val_loss_all[0] is not None else 'N/A'}"
                        f", Upper : {np.round(val_loss_all[1], 3) if val_loss_all[1] is not None else 'N/A'}"
                        f", Bottom : {np.round(val_loss_all[2], 3) if val_loss_all[2] is not None else 'N/A'}\n"
                        f"\tTest Loss:"
                        f" Weighted: {np.round(test_loss_all[0], 3) if test_loss_all[0] is not None else 'N/A'}"
                        f", Upper : {np.round(test_loss_all[1], 3) if test_loss_all[1] is not None else 'N/A'}"
                        f", Bottom : {np.round(test_loss_all[2], 3) if test_loss_all[2] is not None else 'N/A'}\n"
                    )
                else:
                    print(
                        f"Fold {fold_idx + 1} - Iter {epoch} - "
                        f"Loss: {np.round(loss, 3)}, "
                        f"Validation Loss: {np.round(val_loss, 3) if val_loss is not None else 'N/A'}, "
                        f"Test Loss: {np.round(test_loss, 3) if test_loss is not None else 'N/A'}"
                    )

                es, non_decreasing = self.early_stopping(
                    fold_val_losses, patience=hyperparameters["patience"]
                )

                if early_stopping and val_loss is not None and es:
                    print(
                        f"EarlyStopping counter: {non_decreasing} out of {hyperparameters['patience']}"
                    )
                    break

                # model checkpoint
                if val_loss is not None and val_loss < best_val_loss:
                    best_val_loss = val_loss
                    best_state_dict = state_dict
                    torch.save(
                        best_state_dict,
                        f"./model_weights/best_model_weights_fold_{fold_idx}_"
                        f"{self.gp_type}_{self.dataset}_{self.model_version}.pth",
                    )

            val_losses_upper.append(
                [
                    losses_all[1]
                    for losses_all in fold_val_losses_all
                    if losses_all is not None
                ]
            )
            val_losses_bottom.append(
                [
                    losses_all[2]
                    for losses_all in fold_val_losses_all
                    if losses_all is not None
                ]
            )
            test_losses_upper.append(
                [
                    losses_all[1]
                    for losses_all in fold_test_losses_all
                    if losses_all is not None
                ]
            )
            test_losses_bottom.append(
                [
                    losses_all[2]
                    for losses_all in fold_test_losses_all
                    if losses_all is not None
                ]
            )

            self.losses.append(fold_losses)
            self.val_losses.append(fold_val_losses)
            self.test_losses.append(fold_test_losses)

            self._log_training_information(epoch, loss, val_loss, test_loss)

        # Computing average losses over folds, note that we are getting the min
        # validation loss for each fold and the corresponding loss and test_loss
        self.avg_loss = (
            [
                self.losses[i][np.argmin(self.val_losses[i])]
                for i in range(len(self.losses))
            ]
            if self.val_losses
            else None
        )
        self.avg_val_loss = (
            [np.round(min(fold), 3) for fold in self.val_losses]
            if self.val_losses
            else None
        )
        self.avg_val_loss_idx = (
            [np.round(np.argmin(fold), 3) for fold in self.val_losses]
            if self.val_losses
            else None
        )
        self.avg_test_loss = (
            [
                np.round(self.test_losses[i][np.argmin(self.val_losses[i])], 3)
                for i in range(len(self.test_losses))
            ]
            if self.test_losses and self.val_losses
            else None
        )
        min_test_loss = (
            [np.round(min(fold), 3) for fold in self.test_losses]
            if self.test_losses
            else None
        )

        avg_val_loss_upper = (
            [np.round(min(fold), 3) for fold in val_losses_upper]
            if val_losses_upper
            else None
        )
        avg_val_loss_bottom = (
            [np.round(min(fold), 3) for fold in val_losses_bottom]
            if val_losses_bottom
            else None
        )

        avg_test_loss_upper = (
            [
                np.round(test_losses_upper[i][np.argmin(val_losses_upper[i])], 3)
                for i in range(len(test_losses_upper))
            ]
            if test_losses_upper and val_losses_upper
            else None
        )
        avg_test_loss_bottom = (
            [
                np.round(test_losses_bottom[i][np.argmin(val_losses_bottom[i])], 3)
                for i in range(len(test_losses_bottom))
            ]
            if test_losses_bottom and val_losses_bottom
            else None
        )

        print(
            f"\n ----------//---------- \n"
            f"Average training loss: {self.avg_loss}, \n"
            f"Average validation loss: {self.avg_val_loss}, \n"
            f"Average validation loss (upper): {avg_val_loss_upper}, \n"
            f"Average validation loss (bottom): {avg_val_loss_bottom}, \n"
            f"Average test loss: {self.avg_test_loss}, \n"
            f"Average test loss (upper): {avg_test_loss_upper}, \n"
            f"Average test loss (bottom): {avg_test_loss_bottom}, \n"
        )

        if best_state_dict is not None:
            model.load_state_dict(best_state_dict)

        return model, likelihood

    def _initialize_mll(self, model, likelihood) -> None:
        if self.gp_type == "svg":
            self.mll = SumVariationalELBO(
                likelihood, model, num_data=self.train_y.size(0)
            )
        else:
            self.mll = SumMarginalLogLikelihood(likelihood, model)

    def _log_training_information(
        self,
        epoch: int,
        loss: float,
        val_loss: Optional[float],
        test_loss: Optional[float],
    ) -> None:
        wall_time_train = time.time() - self.timer_start
        training_duration = timedelta(seconds=int(wall_time_train))

        self._log_memory()

        log_message = (
            f"Epoch {epoch} - "
            f"Duration: {str(training_duration)} - "
            f"Training Loss: {loss:.2f}"
        )

        if val_loss is not None:
            log_message += f" - Validation Loss: {val_loss:.2f}"
            log_message += f" - Test Loss: {test_loss:.2f}"

        self.logger_train.info(log_message)

    def compute_loss_upper_bottom_weighted(
        self,
        concatenated_pred_upper,
        y_upper,
        train_y_upper,
        concatenated_pred_bottom,
        y_bottom,
        train_y_bottom,
        sp,
    ):
        loss_upper = self.mase(
            y_pred=self.to_cpu(concatenated_pred_upper),
            y_true=self.to_cpu(y_upper),
            y_train=self.to_cpu(train_y_upper),
            sp=sp,
        ).mean()

        loss_bottom = self.mase(
            y_pred=self.to_cpu(concatenated_pred_bottom),
            y_true=self.to_cpu(y_bottom),
            y_train=self.to_cpu(train_y_bottom),
            sp=sp,
        ).mean()

        loss_weighted = 0.5 * loss_upper + 0.5 * loss_bottom

        return loss_weighted, loss_upper.item(), loss_bottom.item()

    def validate(
        self,
        model: IndependentModelList,
        val_x,
        val_y,
        val_y_upper,
        val_y_bottom,
        test_x,
        test_y,
        test_y_upper,
        test_y_bottom,
        train_y,
        train_y_upper,
        train_y_bottom,
        likelihood,
    ) -> Tuple[
        Tuple[float, float], Tuple[float, float, float], Tuple[float, float, float]
    ]:
        """
        Validate the model.

        Returns:
            tuple: The negative log likelihood of the model on the validation set
                   and MASE on the test set.
        """
        with torch.no_grad(), gpytorch.settings.fast_pred_var():
            # Validation
            val_output = likelihood(
                *model(*[val_x for i in range(self.groups["predict"]["s"])])
            )
            val_pred = (
                torch.zeros((val_x.shape[0], self.s)).to(torch.float32).to(self.device)
            )
            for ts in range(self.s):
                val_pred[:, ts] = val_output[ts].mean

            hierarchical_pred = self.hierarchical_data_summary(val_pred)
            (
                concatenated_pred,
                concatenated_pred_upper,
                concatenated_pred_bottom,
            ) = self.concatenate_arrays(hierarchical_pred)

            concatenated_pred = concatenated_pred.cpu().numpy()
            concatenated_pred_upper = concatenated_pred_upper.cpu().numpy()
            concatenated_pred_bottom = concatenated_pred_bottom.cpu().numpy()
            train_y = train_y.cpu().numpy()

            if train_y.shape[0] < self.seasonality:
                sp = 1  # non-seasonal case, use a lag of 1
            else:
                sp = self.seasonality
            (
                val_loss_weighted,
                val_loss_upper,
                val_loss_bottom,
            ) = self.compute_loss_upper_bottom_weighted(
                concatenated_pred_upper=concatenated_pred_upper,
                y_upper=val_y_upper,
                train_y_upper=train_y_upper,
                concatenated_pred_bottom=concatenated_pred_bottom,
                y_bottom=val_y_bottom,
                train_y_bottom=train_y_bottom,
                sp=sp,
            )

            # Moving average loss
            self.val_loss_ma_window.append(val_loss_weighted)
            if len(self.val_loss_ma_window) > self.ma_window_size:
                self.val_loss_ma_window.pop(
                    0
                )  # remove the oldest loss if window is full
            val_loss_ma = sum(self.val_loss_ma_window) / len(self.val_loss_ma_window)

            # Testing
            test_output = likelihood(
                *model(*[test_x for i in range(self.groups["predict"]["s"])])
            )
            test_pred = (
                torch.zeros((test_x.shape[0], self.s)).to(torch.float32).to(self.device)
            )
            for ts in range(self.s):
                test_pred[:, ts] = test_output[ts].mean

            hierarchical_pred_test = self.hierarchical_data_summary(test_pred)
            (
                concatenated_pred_test,
                concatenated_pred_test_upper,
                concatenated_pred_test_bottom,
            ) = self.concatenate_arrays(hierarchical_pred_test)

            (
                test_loss_weighted,
                test_loss_upper,
                test_loss_bottom,
            ) = self.compute_loss_upper_bottom_weighted(
                concatenated_pred_test_upper,
                test_y_upper,
                train_y_upper,
                concatenated_pred_test_bottom,
                test_y_bottom,
                train_y_bottom,
                sp,
            )

        return (
            (val_loss_ma, test_loss_weighted),
            (val_loss_weighted, val_loss_upper, val_loss_bottom),
            (
                test_loss_weighted,
                test_loss_upper,
                test_loss_bottom,
            ),
        )

    @staticmethod
    def _create_directory_if_not_exists(directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

    def plot_losses(self, start_idx: int = 5):
        self._create_directory_if_not_exists("plots")

        n_iterations, val_losses_interp, test_losses_interp = self._prepare_loss_data()

        # assuming self.losses and val_losses_interp are lists of lists, where each sub-list corresponds to a fold
        for i, (n_iter, losses, val_losses, test_losses) in enumerate(
            zip(n_iterations, self.losses, val_losses_interp, test_losses_interp)
        ):
            self._plot_loss_data(
                n_iter[start_idx:],
                losses[start_idx:],
                val_losses[start_idx:],
                test_losses[start_idx:],
            )
            self._customize_plot(i + 1)

            timestamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime())
            plt.savefig(
                f"./plots/gpf_{__version__}_loss_{self.dataset}_fold_{i + 1}_{timestamp}.pdf",
                format="pdf",
                bbox_inches="tight",
            )
            plt.show()

    def _prepare_loss_data(self):
        val_losses_interp = []
        test_losses_interp = []
        n_iterations = []
        for idx, (val_losses_fold, test_losses_fold) in enumerate(
            zip(self.val_losses, self.test_losses)
        ):  # Loop over each fold
            n_iterations_total = np.arange(len(self.losses[idx]))
            val_interval = round(len(self.losses[idx]) / len(self.val_losses[idx]))
            val_indices = np.arange(0, len(self.losses[idx]), val_interval)
            interp_func = interp1d(
                val_indices,
                val_losses_fold,
                kind="linear",
                fill_value="extrapolate",
            )
            val_losses_interp.append(interp_func(n_iterations_total))

            interp_func = interp1d(
                val_indices,
                test_losses_fold,
                kind="linear",
                fill_value="extrapolate",
            )
            test_losses_interp.append(interp_func(n_iterations_total))

            n_iterations.append(n_iterations_total)

        return n_iterations, val_losses_interp, test_losses_interp

    @staticmethod
    def _plot_loss_data(
        n_iterations, train_losses, val_losses_interp, test_losses_interp
    ):
        plt.plot(n_iterations, train_losses, label="Training Loss")
        plt.plot(n_iterations, val_losses_interp, marker="^", label="Validation Loss")
        plt.plot(n_iterations, test_losses_interp, marker="*", label="Test Loss")

    @staticmethod
    def _customize_plot(fold_num: int):
        plt.title(f"Training, Validation and Test Losses for Fold {fold_num}")
        plt.xlabel("Iteration")
        plt.ylabel("Loss")
        plt.legend()

    @staticmethod
    def to_cpu(data):
        if torch.is_tensor(data) and data.is_cuda:
            return data.cpu().numpy()
        elif torch.is_tensor(data):
            return data.numpy()
        return data

    def predict(
        self,
        model: IndependentModelList,
        likelihood: LikelihoodList,
    ) -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:
        """
        Make predictions with the model.

        Parameters:
            model: The GP model.
            likelihood: The likelihood function.
            track_mem: Track and log RAM usage

        Returns:
            numpy.ndarray: Array of shape (n_samples, n_prediction_points, n_groups)
                containing the prediction samples.
        """
        timer_start = time.time()

        model.eval()
        likelihood.eval()

        with torch.no_grad(), gpytorch.settings.fast_pred_var():
            predictions = likelihood(
                *model(*[self.complete_x for _ in range(self.groups["predict"]["s"])])
            )
            self._log_memory()

        pred_mean_scaled = np.zeros((len(self.complete_x), self.s))
        pred_std_scaled = np.zeros((len(self.complete_x), self.s))
        for ts in range(self.s):
            pred_mean_scaled[:, ts] = predictions[ts].mean.cpu().detach().numpy()
            pred_std_scaled[:, ts] = np.sqrt(
                predictions[ts].variance.cpu().detach().numpy()
            )

        # transform back the data
        pred_mean = self.scaler.inverse_transform(pred_mean_scaled)
        pred_std = None

        if self.scale_x_values:
            self.train_x = self.scaler_x_values.inverse_transform(
                self.to_cpu(self.train_x)
            )
            self.complete_x = self.scaler_x_values.inverse_transform(
                self.to_cpu(self.complete_x)
            )
            self.train_y = self.scaler.inverse_transform(self.to_cpu(self.train_y))
            self.test_x = self.scaler_x_values.inverse_transform(
                self.to_cpu(self.test_x)
            )
            self.test_y = self.scaler.inverse_transform(self.to_cpu(self.test_y))
            self.inducing_points = self.scaler_x_values.inverse_transform(
                self.to_cpu(self.inducing_points)
            )

        if isinstance(self.scaler, StandardScaler):
            pred_std = pred_std_scaled * self.scaler.scale_
        elif isinstance(self.scaler, MinMaxScaler):
            # For MinMaxScaler, no straightforward way to convert scaled standard deviation
            scale_factor = self.scaler.data_max_ - self.scaler.data_min_
            pred_std = pred_std_scaled * scale_factor

        self.wall_time_predict = time.time() - timer_start
        return (pred_mean, pred_std), (pred_mean_scaled, pred_std_scaled)

    @staticmethod
    def _validate_param(param, valid_values):
        if param not in valid_values:
            raise ValueError(f"{param} is not a valid value")

    def store_results(
        self,
        res: np.ndarray,
        res_type: str,
        res_measure: str,
        track_mem: bool = True,
    ):
        """
        Store results

        Parameters:
            res: np array with the results with shape (n,s) - note that n depends of the res_type
            res_type: defines the type of results, could be 'fit_pred' to receive fitted values plus
                predictions or 'pred' to only store predictions
            res_measure: defines the measure to store, could be 'mean' or 'std'

        Returns:
            numpy.ndarray: Array of shape (n_samples, n_prediction_points, n_groups)
                containing the prediction samples.
        """
        """
        Store results, res_type should be used to define the type of results,
        could be 'fit_pred' to receive fitted values plus predictions or 'pred'
        to only store predictions
        """
        self._validate_param(res_type, ["fitpred", "pred"])
        self._validate_param(res_measure, ["mean", "std"])
        with open(
            f"{self.input_dir}results_{res_type}_{res_measure}_gp_{self.gp_type}_cov_{self.dataset}_{self.model_version}.pickle",
            "wb",
        ) as handle:
            if track_mem:
                process = psutil.Process(os.getpid())
                mem = process.memory_info().rss / (1024**3)
                self.logger_metrics.info(f"Storing results used {mem:.3f} GB of RAM")
            pickle.dump(res, handle, pickle.HIGHEST_PROTOCOL)

    def store_metrics(
        self,
        res: Dict[str, Dict[str, Union[float, np.ndarray]]],
        track_mem: bool = True,
    ):
        with open(
            f"{self.input_dir}metrics_gp_{self.gp_type}_cov_{self.dataset}_{self.model_version}.pickle",
            "wb",
        ) as handle:
            if track_mem:
                process = psutil.Process(os.getpid())
                mem = process.memory_info().rss / (1024**3)
                self.logger_metrics.info(
                    f"Storing error metrics used {mem:.3f} GB of RAM"
                )
            pickle.dump(res, handle, pickle.HIGHEST_PROTOCOL)

    def metrics(
        self,
        pred_mean: np.ndarray,
        pred_std: np.ndarray,
        track_mem: bool = True,
    ) -> Dict[str, Dict[str, Union[float, np.ndarray]]]:
        """
        Calculate evaluation metrics for the predictions.

        Parameters:
            pred_mean: Array of shape (n_prediction_points, n_series)
                containing the prediction samples.
            pred_std: Array of shape (n_prediction_points, n_series)
                containing the prediction samples.
            track_mem: Track and log RAM usage

        Returns:
            dict: Dictionary with the evaluation metrics. The keys are the metric names,
                and the values are dictionaries with the results for each group.
        """
        calc_results = CalculateResultsBottomUp(
            predictions_mean=pred_mean,
            predictions_std=pred_std,
            groups=self.groups,
            dataset=self.dataset,
        )
        res = calc_results.calculate_metrics()
        if track_mem:
            process = psutil.Process(os.getpid())
            mem = process.memory_info().rss / (1024**3)
            self.logger_metrics.info(
                f"calculating error metrics used {mem:.3f} GB of RAM"
            )
        self.wall_time_total = time.time() - self.timer_start

        res["wall_time"] = {}
        res["wall_time"]["wall_time_train"] = self.wall_time_train
        res["wall_time"]["wall_time_predict"] = self.wall_time_predict
        res["wall_time"]["wall_time_total"] = self.wall_time_total

        return res

    def __del__(self):
        self.logger_train.close()
        self.logger_predict.close()
        self.logger_metrics.close()
