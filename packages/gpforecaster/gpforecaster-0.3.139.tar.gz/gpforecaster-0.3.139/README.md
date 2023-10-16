![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gpforecaster)
[![license](https://img.shields.io/badge/License-BSD%203-brightgreen)](https://github.com/luisroque/hierarchical_gp_forecaster/blob/main/LICENSE)
![PyPI](https://img.shields.io/pypi/v/gpforecaster)
[![Downloads](https://pepy.tech/badge/gpforecaster)](https://pepy.tech/project/gpforecaster)

# GPHF: A Gaussian Process Approach to Hierarchical Time Series Forecasting

We present the Gaussian Process Hierarchical Forecaster (GPHF), a novel approach to forecasting hierarchical time series critical for retail, energy, and finance industries. Accurate forecasting of these time series is challenging because lower-level forecasts must sum to upper-level ones while capturing complex dependencies within the data. GPHF addresses the limitations of existing methods like DeepAR and MinT by providing a more flexible and data-driven approach to capturing dependencies. GPHF utilizes Gaussian Processes and a covariance mixture to learn time series dependencies in hierarchical data efficiently. In our evaluation using multiple real-world datasets, GPHF consistently demonstrated competitive results and outperformed both DeepAR and MinT in several cases. This performance advantage showcases the potential of GPHF in improving the accuracy and reliability of hierarchical time series forecasting across various industries and applications.

You can install gpforecaster as a python package
```python
pip install gpforecaster
```

## Functionality


The main functionality of this repository includes:

* **GPHF Model:** The implementation of the Gaussian Process Hierarchical Forecaster for forecasting hierarchical time series data built on top of GPyTorch.
* **Scalable Gaussian Processes:** A scalable approach to Gaussian Processes that can handle large-scale hierarchical time series datasets.
* **Automatic Forecasting:** A method for automatic time series forecasting on hierarchical data, offering robust performance even with missing data and without requiring prior knowledge.
* **Visualization Tools:** Tools for visualizing predictions, losses, and other aspects of the GPHF model.


## Getting started
The code below creates new versions of the prison dataset by applying time series augmentation transformations.

```python
import gpforecaster as gpf
import tsaugmentation as tsag

# Get the data
dataset = 'prison'
data = tsag.preprocessing.PreprocessDatasets(dataset).apply_preprocess()

# Initialize the GPHF model
gpf_model = gpf.model.GPF(dataset, data)

# Train the model
model, like = gpf_model.train()

# Plot the losses
gpf_model.plot_losses()
```

![Experimental Results](loss.png)

```python
# Generate predictions
preds, preds_scaled = gpf_model.predict(model=model, likelihood=like)

# Plot predictions vs. original data
gpf.visualization.plot_predictions_vs_original(
    dataset=dataset,
    prediction_mean=preds[0],
    prediction_std=preds[1],
    origin_data=gpf_model.original_data,
    inducing_points=gpf_model.inducing_points,
    x_original=gpf_model.train_x.numpy(),
    x_test=gpf_model.test_x.numpy(),
    n_series_to_plot=8,
    gp_type=gpf_model.gp_type,
)

# Calculate and store metrics
res = gpf_model.metrics(pred_mean=preds[0], pred_std=preds[1])
gpf_model.store_metrics(res)
```

![Experimental Results](pred.png)

### Contributing
We welcome contributions to this repository. If you find a bug, or if you have an idea for a new feature, please open an issue or submit a pull request.

### License
This repository is licensed under the BSD 3-Clause License. See the LICENSE file for more information.