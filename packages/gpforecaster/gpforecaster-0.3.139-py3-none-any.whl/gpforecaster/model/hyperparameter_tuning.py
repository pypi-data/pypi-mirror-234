from typing import Tuple, Dict, List, Any, Optional
import gc
import numpy as np

from skopt import Optimizer
from skopt.space import Real, Categorical, Integer
from skopt.utils import use_named_args

from gpforecaster.model.gpf import GPF
from gpforecaster.utils.logger import Logger
from gpforecaster import __version__


def single_trial(
    epochs: int,
    dataset_name: str,
    hierarchical_data: Dict[str, List],
    hyperparameters: Dict[str, Any],
    gp_type: str,
    device: str,
    logger_tuning: Logger,
    trial_num: int,
) -> Tuple[float, float, Dict[str, Any]]:
    """
    Train a single GPF model with the given hyperparameters.

    Args:
        dataset_name (str): The name of the dataset.
        hierarchical_data (Dict[str, List]): The hierarchical data for the model.
        hyperparameters (Dict[str, Any]): The hyperparameters to use for the model.
        gp_type (str): The type of Gaussian Process model to use (e.g., "exact").
        device (str): The device to use for computation (e.g., "cpu" or "cuda").
        logger_tuning (Logger): The logger for hyperparameter tuning.
        trial_num (int): The trial number (for display purposes).

    Yields:
        Tuple[float, Dict[str, Any]]: A tuple containing the validation loss and the hyperparameters used.
    """
    print(f"Running trial number {trial_num}")
    logger_tuning.info(f"Running trial number {trial_num}")

    gpf = GPF(
        dataset=dataset_name,
        groups=hierarchical_data,
        gp_type=gp_type,
        device=device,
        scaler_type=hyperparameters["scaler_type"],
        scale_x_values=hyperparameters["scale_x_values"],
    )

    penalty = 1e5

    model, like = None, None

    try:
        model, like = gpf.train(epochs=epochs, hyperparameters=hyperparameters, verbose=False)
        val_loss = np.mean(gpf.avg_val_loss)
        test_loss = np.mean(gpf.avg_test_loss)
        if np.isnan(val_loss):
            val_loss = penalty
            test_loss = penalty

        if gp_type == "svg" or gp_type == "sparse":
            # for svg and sparse we need to test on the new data,
            # since they often fail the optimization
            gpf = GPF(
                dataset=dataset_name,
                groups=hierarchical_data,
                gp_type=gp_type,
                device=device,
                scaler_type=hyperparameters["scaler_type"],
                scale_x_values=hyperparameters["scale_x_values"],
            )
            model, like = gpf.train(
                epochs=epochs,
                hyperparameters=hyperparameters,
                cross_validation=False,
                no_validation=True,
                n_splits=2,
                early_stopping=True,
            )
    except Exception as e:
        print(f"Error occurred during training with the current set of hyperparameters")
        print(e)
        val_loss = penalty
        test_loss = penalty

    log_and_print_best_hyperparameters(
        gp_type, dataset_name, hyperparameters, val_loss, test_loss, logger_tuning
    )

    if model is not None:
        del model
    if like is not None:
        del like
    if gpf is not None:
        del gpf
    gc.collect()

    return (val_loss, test_loss, hyperparameters)


def optimize_hyperparameters_bayesian(
    dataset_name: str,
    hierarchical_data: Dict[str, List],
    num_trials: int,
    gp_type: str = "exact",
    device: str = "cpu",
    epochs: int = 500,
    hyperparameters_list: Optional[List[str]] = None,
    fixed_hyperparameters: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Optimize hyperparameters using Bayesian search.

    Args:
        dataset_name (str): The name of the dataset.
        hierarchical_data (Dict[str, List]): The hierarchical data for the model.
        num_trials (int): The number of trials to perform.
        gp_type (str): The type of Gaussian Process model to use (e.g., "exact").

    Returns:
        Dict[str, Any]: The best set of hyperparameters found during optimization.
    """
    logger_tuning = Logger(
        "hyperparameter_tuning", dataset=f"{dataset_name}_hypertuning", to_file=True
    )

    if hyperparameters_list is None:
        hyperparameters_list = [
            "lr",
            "weight_decay",
            "scheduler_type",
            "gamma_rate",
            "patience",
            "rbf_kernel_lengthscale",
            "scale_rbf_kernel_outputscale",
            "periodic_kernel_lengthscale",
            "scale_periodic_kernel_outputscale",
            "m",
            "k",
            "b",
            "like_noise",
            "scaler_type",
            "scale_x_values",
            "random_init",
            "learn_like_noise",
            "mean_type",
        ]

    # Define the search space for hyperparameters
    all_hyperparameters = {
        "lr": Real(1e-3, 0.1, name="lr"),
        "weight_decay": Real(1e-6, 1e-3, name="weight_decay"),
        "scheduler_type": Categorical(
            ["step", "exponential", "cosine", "none"], name="scheduler_type"
        ),
        "gamma_rate": Real(0.1, 0.95, name="gamma_rate"),
        "patience": Integer(15, 40, name="patience"),
        "rbf_kernel_lengthscale": Real(0.01, 0.2, name="rbf_kernel_lengthscale"),
        "scale_rbf_kernel_outputscale": Real(1, 2, name="scale_rbf_kernel_outputscale"),
        "periodic_kernel_lengthscale": Real(
            0.01, 0.2, name="periodic_kernel_lengthscale"
        ),
        "scale_periodic_kernel_outputscale": Real(
            1, 2, name="scale_periodic_kernel_outputscale"
        ),
        "m": Real(0.0001, 0.3, name="m"),
        "k": Real(0.0001, 0.3, name="k"),
        "b": Real(0.0001, 0.3, name="b"),
        "like_noise": Real(0.3, 1, name="like_noise"),
        "scaler_type": Categorical(["minmax", "standard"], name="scaler_type"),
        "scale_x_values": Categorical([True, False], name="scale_x_values"),
        "random_init": Categorical([True, False], name="random_init"),
        "learn_like_noise": Categorical([True, False], name="learn_like_noise"),
        "mean_type": Categorical(["piecewise", "constant", "zero"], name="mean_type"),
    }

    if fixed_hyperparameters is not None:
        for key in fixed_hyperparameters.keys():
            all_hyperparameters.pop(key, None)

    search_space = [
        hp
        for name, hp in all_hyperparameters.items()
        if hp.name in hyperparameters_list
    ]

    optimizer = Optimizer(search_space)
    trial_num = 0
    test_loss = []

    current_best_val_loss = float("inf")
    current_best_hyperparameters = None
    current_best_test_loss = None

    @use_named_args(search_space)
    def wrapped_single_trial(**hyperparameters):
        nonlocal trial_num, current_best_val_loss, current_best_hyperparameters, current_best_test_loss
        if fixed_hyperparameters is not None:
            hyperparameters = {**fixed_hyperparameters, **hyperparameters}
        val_loss, temp_test_loss, current_hyperparameters = single_trial(
            epochs,
            dataset_name,
            hierarchical_data,
            hyperparameters,
            gp_type,
            device,
            logger_tuning,
            trial_num=trial_num,
        )
        test_loss.append(temp_test_loss)
        trial_num += 1

        if val_loss < current_best_val_loss:
            current_best_val_loss = val_loss
            current_best_hyperparameters = current_hyperparameters
            current_best_test_loss = temp_test_loss

        log_and_print_best_hyperparameters(
            gp_type,
            dataset_name,
            current_best_hyperparameters,
            current_best_val_loss,
            current_best_test_loss,
            logger_tuning,
            best="CURRENT BEST",
        )
        return val_loss

    results = optimizer.run(wrapped_single_trial, num_trials)
    best_hyperparameters = {k.name: v for k, v in zip(search_space, results.x)}

    best_trial_idx = np.argmin(results.func_vals)
    best_test_loss = test_loss[best_trial_idx]

    if fixed_hyperparameters:
        best_hyperparameters = {**fixed_hyperparameters, **best_hyperparameters}

    log_and_print_best_hyperparameters(
        gp_type,
        dataset_name,
        best_hyperparameters,
        results.fun,
        best_test_loss,
        logger_tuning,
        best="BEST",
    )
    return best_hyperparameters


def log_and_print_best_hyperparameters(
    gp_type: str,
    dataset_name: str,
    best_hyperparameters: Dict[str, Any],
    best_val_loss: float,
    best_test_loss: float,
    logger_tuning: Logger,
    best="",
):
    """
    Log and print the best hyperparameters and validation loss.

    Args:
        gp_type (str): The type of Gaussian Process model used (e.g., "exact").
        dataset_name (str): The name of the dataset.
        best_hyperparameters (Dict[str, Any]): The best set of hyperparameters found.
        best_val_loss (float): The best validation loss.
    """

    logger_tuning.info(
        f"\n{best} -> "
        f"Algorithm: gpf_{gp_type}, "
        f"Version: {__version__}, "
        f"Dataset: {dataset_name}, "
        f"{best} hyperparameters: {best_hyperparameters}, "
        f"Validation loss: {best_val_loss}\n"
        f"Test loss: {best_test_loss}\n"
    )

    print(
        f"\n{best} -> "
        f"Algorithm: gpf_{gp_type}, \n"
        f"Version: {__version__}, \n"
        f"Dataset: {dataset_name}, \n"
        f"{best} hyperparameters: {best_hyperparameters}, \n"
        f"Validation loss: {best_val_loss}\n"
        f"Test loss: {best_test_loss}\n"
    )
