# Deep Kernel Latent Force Models

This is the code for running the experiments found in the paper "Meta-Learning Nonlinear Dynamical Systems with Deep Kernels".

We use some code from the `Alfi` package, so follow the installation instructions there first.

## Structure

- conf: configuration files for running experiments
- model.py: the DKLFM model as a GPytorch ExactGP model with PyTorch Lightning wrapper
- plotter.py: plotting functions for both 1d and 2d tasks
- transformer_encoder.py: the transformer encoder used
- scaler.py: simple standard scaler with saving functionality
- run.py: the experiment runner, use the conf/train.yaml file to specify the experiment
- eval.py: the evaluation script, use the conf/eval.yaml file to specify the experiment

When an experiment is run, a `tb_logs` directory will be created, containing the full experiment data.

When the evaluation script is run on an experiment, a subdirectory `evaluation` will be created, containing the plots.

## Key configuration items

A lot of the configuration is automated, for example if using a 2d dataset, the config has the correct `block_dim`.

For the `train.yaml` file:
- `training` -> `dataset` specifies the dataset to use
- `embedder` -> `type` specifies the type of embedding to use, either `transformer` or `neural_operator`
- `model` -> `lengthscale` and `period` and `kernel` to specify the kernel to use and associated hyperparameters
- The dataset configs specify some of the model parameters since they are dataset dependent

For the `eval.yaml` file:
- `version` can be set to `latest` or specific version numbers. Can be an array of versions.
- `dataset` specifies the dataset to use

Run `python dklfm/run.py` to run using the train.yaml
Run `python dklfm/eval.py` to evaluate using the eval.yaml
