import sys
from pathlib import Path
from dotenv import load_dotenv

import hydra
import numpy as np
import torch
import gpytorch
from omegaconf import DictConfig
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping, LearningRateMonitor
from pytorch_lightning.loggers import TensorBoardLogger
import pytorch_lightning as pl
from torch.utils.data import DataLoader
from matplotlib import pyplot as plt
from torch.nn import LSTM
from alfi.models.mlp import MLP

from dklfm.model import DeepKernelLFM, DKLFMWrapper
from alfi.models import NeuralOperator
from dklfm.transformer_encoder import TransformerEncoder
from dklfm.util import map_device, Scaler
from dklfm import data_dir, sc_rna_dir
from dklfm.data.dataset_helpers import synthetic_transcriptomics, from_loom, \
    create_or_load_synthetic
from tqdm import trange
from dklfm.data.dklfm_dataset import DeepKernelLFMDataset

plt.rcParams['axes.unicode_minus'] = False


# input given as (batch, seq, feature)
def load_dataset(cfg, scaler_dir=None):
    dataset = cfg['training']['dataset']
    ds_cfg = cfg[f'dataset_{dataset}']

    # Scaler uses the final dimension, i.e. the times
    if scaler_dir is not None:
        y_scaler = torch.load(scaler_dir / 'y_scaler.pt')
        f_scaler = torch.load(scaler_dir / 'f_scaler.pt')
        real_y_scaler = torch.load(scaler_dir / 'real_y_scaler.pt')
        real_f_scaler = torch.load(scaler_dir / 'real_f_scaler.pt')
    else:
        y_scaler = Scaler()
        f_scaler = Scaler()
        real_y_scaler = Scaler()
        real_f_scaler = Scaler()

    y_scaler.do_scale = cfg['training']['scale_data']
    f_scaler.do_scale = cfg['training']['scale_data']
    real_y_scaler.do_scale = cfg['training']['scale_data']
    real_f_scaler.do_scale = cfg['training']['scale_data']

    if dataset == 'transcriptomics':
        synthetic_dataset = synthetic_transcriptomics(
            data_dir=sc_rna_dir, load=True,
            scalers=(y_scaler, f_scaler),
            scale_x_max=cfg['training']['scale_x_max'],
            n_training_instances=ds_cfg['n_training_tasks'],
            n_test_instances=ds_cfg['n_test_tasks']
        )
        real_dataset= None
        # real_dataset = p53_transcriptomics(data_dir='/media/jacob/ultra/genomics/microarray', t_scale=9 / 12,
        #                                    scalers=(real_y_scaler, real_f_scaler), scale_x_max=cfg['training']['scale_x_max'])

    elif dataset == 'rnavelo':
        real_dataset = from_loom(
            load=True,
            scalers=(real_y_scaler, real_f_scaler),
        )
        synthetic_dataset = create_or_load_synthetic(
            load=True,
            scalers=(y_scaler, f_scaler),
            scale_x_max=cfg['training']['scale_x_max'],
            n_train=ds_cfg['n_train'], n_training_tasks=ds_cfg['n_training_tasks'])
    elif dataset == 'reactiondiffusion':
        from pathlib import Path
        ultra_dir = Path("/Volumes/ultra")
        ultra_dir = Path("/media/jacob/ultra")
        # ultra_dir = Path("/Users/jacob/data")

        synthetic_spatial = torch.load(ultra_dir / 'toydata.pt')
        data = synthetic_spatial['orig_data']
        print(data.shape)
        plt.imshow(data[0, 0].reshape(41, 41).t(), origin='lower')
        plt.figure()
        plt.imshow(data[0, 1].reshape(41, 41).t(), origin='lower')
        y = data[:500, 1:2].view(500, 1, 41, 41)[..., ::2, ::2].reshape(500, 1, -1).type(torch.float64)
        f = data[:500, 0:1].view(500, 1, 41, 41)[..., ::2, ::2].reshape(500, 1, -1).type(torch.float64)
        plt.figure()
        plt.imshow(y[0, 0].reshape(21, 21).t(), origin='lower')
        x = synthetic_spatial['x_observed'].view(2, 41, 41)[..., ::2, ::2].reshape(2, -1).t().type(torch.float64)
        data = None
        synthetic_spatial = None
        # n_data = n_times
        # train_indices = np.sort(np.random.permutation(np.arange(41))[:n_times])
        # print(train_indices)
        print('y, f', y.shape, f.shape, x.shape)
        synthetic_dataset = DeepKernelLFMDataset(
            x, y, f=f, n_train=f.shape[-1], scale_x_max=cfg['training']['scale_x_max'],
            n_test_instances=ds_cfg['n_test_tasks']
        )
        synthetic_dataset.input_dim = 2
        real_dataset = None
        # orig_data = data
        # x_observed = synthetic_spatial['x_observed']
        # num_data = 400
        # num_outputs = 1
        # num_discretised = 40
        #
        # tx = x_observed.t()[:, 0:2]
        # t_sorted = np.argsort(tx[:, 0], kind='mergesort')
        # x_observed = x_observed[:, t_sorted]
        # orig_data = torch.cat([
        #     x_observed.unsqueeze(0).repeat(num_data, 1, 1),
        #     orig_data[:num_data, :, t_sorted]
        # ], dim=1)
        # params = synthetic_spatial['params'][:num_data]
        # neural_dataset = generate_neural_dataset_2d(orig_data, params, 300, 100)
        # print(neural_dataset[0][0][0].shape)
    elif dataset == 'lotkavolterra':
        from alfi.datasets import DeterministicLotkaVolterra
        load_lokta = True
        if load_lokta:
            t, lf, y = torch.load(data_dir / 'lotka_data.pt')
        else:
            t = None
            lf = list()
            y = list()
            for _ in trange(500):
                data = DeterministicLotkaVolterra(
                    alpha = np.random.uniform(0.5, 1.),
                    beta = np.random.uniform(1., 1.4),
                    gamma = 1.,
                    delta = 1.,
                    steps=30,
                    end_time=30,
                    fixed_initial=0.8,
                    silent=True
                )
                t = data.data[0][0]
                lf.append(data.prey[::data.num_disc+1])
                y.append(data.data[0][1])

            y = torch.stack(y).unsqueeze(1)
            lf = torch.stack(lf).unsqueeze(1)
            torch.save([t, lf, y], 'lotka_data.pt')
            x_min, x_max = min(data.times), max(data.times)
            plt.plot(data.data[0][0], data.data[0][1], c='red', label='predator')
            plt.plot(torch.linspace(x_min, x_max, data.prey.shape[0]), data.prey, c='blue', label='prey')
            plt.legend()

        y = y_scaler.scale(y)
        lf = f_scaler.scale(lf)
        synthetic_dataset = DeepKernelLFMDataset(
            t, y, f=lf,
            train_indices=np.arange(0, t.shape[0]),
            scale_x_max=cfg['training']['scale_x_max'],
            n_test_instances=ds_cfg['n_test_tasks'],
        )
        real_dataset = None
    else:
        raise ValueError(f'Unknown dataset {dataset}')
    return synthetic_dataset, real_dataset, {'y_scaler': y_scaler, 'f_scaler': f_scaler, 'real_y_scaler': real_y_scaler, 'real_f_scaler': real_f_scaler}


def get_embedder(cfg):
    ds_cfg = cfg[f"dataset_{cfg['training']['dataset']}"]
    block_dim = ds_cfg['block_dim']
    out_channels = cfg['embedder']['out_channels']

    if cfg['embedder']['type'] == 'lstm':
        embedder_model = LSTM(1, out_channels, 1, batch_first=True, bidirectional=False).type(
            torch.float64)  # input_size, hidden_size, num_layers

        def embedder(y_reshaped, **kwargs):
            _, (hn, _) = embedder_model(y_reshaped)
            return hn
    elif cfg['embedder']['type'] == 'transformer':
        embedder_model = TransformerEncoder(ds_cfg['embedder_in_channels'], output_dim=out_channels).type(torch.float64)
        def embedder(y_reshaped, **kwargs):

            hn = embedder_model(y_reshaped).mean(dim=1)
            return hn

    else:
        embedder_model = NeuralOperator(
            block_dim,
            ds_cfg['embedder_in_channels'],
            out_channels,
            ds_cfg['modes'],
            cfg['embedder']['width'],
            params=False
        )

        def embedder(y_reshaped, x_cond=None):
            if cfg['training']['dataset'] == 'reactiondiffusion':
                n_task = y_reshaped.shape[0]
                y_reshaped = y_reshaped.view(n_task, ds_cfg['t_width'], ds_cfg['x_width'], 1)
                x_cond = x_cond.view(n_task, ds_cfg['t_width'], ds_cfg['x_width'], 2)
                y_reshaped = torch.cat([x_cond, y_reshaped], dim=-1)

            hn = embedder_model(y_reshaped.type(torch.float32)).mean(1).type(torch.float64)

            if cfg['training']['dataset'] == 'reactiondiffusion':
                hn = hn.mean(1)

            return hn
    return embedder_model, embedder


def get_model(cfg, synthetic_dataset, scaler_modules):
    ds_cfg = cfg[f"dataset_{cfg['training']['dataset']}"]
    block_dim = ds_cfg['block_dim']
    out_channels = cfg['embedder']['out_channels']
    latent_dims = cfg['model']['latent_dims']
    num_hidden_layers = ds_cfg['num_hidden_layers']
    include_embedding = cfg['model']['include_embedding']
    ckpt_path = cfg['model']['ckpt_path']


    if include_embedding is not False:
        embedder_model, embedder_fn = get_embedder(cfg)
    if cfg['model']['fixed_noise']:
        likelihood = gpytorch.likelihoods.FixedNoiseGaussianLikelihood(
            torch.ones(1, dtype=torch.float64) * ds_cfg['initial_noise']).type(torch.float64)
        likelihood_f = gpytorch.likelihoods.FixedNoiseGaussianLikelihood(
            torch.ones(1, dtype=torch.float64) * ds_cfg['initial_noise']).type(torch.float64)
    else:
        from gpytorch.constraints import LessThan
        likelihood_f = gpytorch.likelihoods.GaussianLikelihood(noise_constraint=LessThan(2*ds_cfg['initial_noise'])).type(torch.float64)
        likelihood_f.noise = ds_cfg['initial_noise']
        likelihood = gpytorch.likelihoods.GaussianLikelihood(noise_constraint=LessThan(2*ds_cfg['initial_noise'])).type(torch.float64)
        likelihood.noise = ds_cfg['initial_noise']

    joint_operator = MLP(block_dim + out_channels, latent_dims, num_hidden_layers).type(torch.float64)
    x1_operator = MLP(1 + out_channels, latent_dims, num_hidden_layers).type(torch.float64)
    x2_operator = MLP(1 + out_channels, latent_dims, num_hidden_layers).type(torch.float64)

    model = DeepKernelLFM(
        synthetic_dataset.train_x_cond_blocks, synthetic_dataset.train_y_cond, synthetic_dataset.train_f_cond,
        likelihood, likelihood_f,
        joint_operator if include_embedding is not False else (x1_operator, x2_operator),
        num_functions=synthetic_dataset.y.shape[1],
        embedder=(embedder_model, embedder_fn) if include_embedding is not False else None,
        kernel=cfg['model']['kernel'],
        kernel_in_dims=latent_dims,
        include_embedding=include_embedding
    )
    # model.covar_module = model.covar_module.type(torch.float64)
    model.covar_module.base_kernel.lengthscale *= 0
    model.covar_module.base_kernel.lengthscale += cfg['model']['lengthscale']
    if cfg['model']['kernel'] == 'periodic':
        model.covar_module.base_kernel.period_length *= 0
        model.covar_module.base_kernel.period_length += cfg['model']['period']
    print(dict(model.named_parameters()).keys())

    # lr = 1e-4
    if ckpt_path is not None:
        return DKLFMWrapper.load_from_checkpoint(ckpt_path, cfg=cfg, model=model, mse_data=synthetic_dataset, scaler_modules=scaler_modules)
    return DKLFMWrapper(cfg, model, mse_data=synthetic_dataset, scaler_modules=scaler_modules)


@hydra.main(version_base=None, config_path="conf", config_name="train")
def app(cfg: DictConfig):
    num_epochs = cfg['training']['num_epochs']
    device = map_device(cfg['training']['device'])
    logger = TensorBoardLogger(Path(__file__).parent / "tb_logs", name=cfg['training']['dataset'])
    save_dir = Path(logger.log_dir)
    print("Save directory:", save_dir)

    # Load data
    synthetic_dataset, real_dataset, modules_to_save = load_dataset(cfg)
    batch_size = cfg['training']['batch_size']
    train_loader = DataLoader(synthetic_dataset, batch_size=batch_size)
    val_loader = DataLoader(synthetic_dataset.validation(), batch_size=batch_size)

    # Instantiate the model
    if cfg['training']['load_version'] is not None:
        path = save_dir.parent / f"version_{cfg['training']['load_version']}/checkpoints/last.ckpt"
        cfg['model']['ckpt_path'] = path
    model = get_model(cfg, synthetic_dataset, modules_to_save)

    # Instantiate the trainer

    Path(logger.log_dir).mkdir(exist_ok=True, parents=True)
    Path(logger.log_dir + '/hydra').symlink_to(Path.cwd())
    for obj_name, obj in modules_to_save.items():
        torch.save(obj, logger.log_dir + f'/{obj_name}.pt')
    if torch.cuda.is_available():
        torch.set_float32_matmul_precision('medium')
    # checkpoint_monitor = 'val_loss' if len(test_loader) > 0 else 'train_loss'
    checkpoint_monitor = 'train_loss'
    latent_mses = list()
    output_mses = list()

    trainer = pl.Trainer(
        logger=logger, log_every_n_steps=10,
        max_epochs=num_epochs,
        # gradient_clip_val=0.5,
        accelerator=device,
        callbacks=[
            ModelCheckpoint(save_top_k=1, monitor=checkpoint_monitor, save_last=True),
            EarlyStopping(monitor=checkpoint_monitor, patience=cfg['training']['patience']),
            LearningRateMonitor(logging_interval='epoch'),
        ]
    )
    trainer.fit(model, train_dataloaders=train_loader, val_dataloaders=val_loader, ckpt_path=cfg['model']['ckpt_path'])



if __name__ == '__main__':
    sys.argv.append('hydra.job.chdir=True')
    load_dotenv()
    app()
