import sys
from collections import defaultdict
from pathlib import Path

import hydra
import matplotlib.pyplot as plt
import numpy as np
import torch
from mpl_toolkits.axes_grid1 import make_axes_locatable
from omegaconf import DictConfig, ListConfig
import yaml
from torch.utils.data import DataLoader
from tqdm import tqdm

from dklfm.model import DKLFMWrapper
from dklfm.plotter import DeepKernelLFMPlotter
from dklfm.run import get_model, load_dataset
from velocity.loaders.dataset_helpers import from_loom
import scvelo as scv
from alfi.utilities import softplus

import matplotlib

matplotlib.rc('font', **font)


def add_cbar(fig, ax, scat, pos='top'):
    divider = make_axes_locatable(ax)
    cax = divider.append_axes(pos, size='5%', pad=0.05)
    cb = fig.colorbar(scat, cax=cax, orientation='horizontal')
    cb.ax.xaxis.set_ticks_position('top')

def plot_mses(dataset='transcriptomics', version_range=range(0, 100)):
    from pathlib import Path
    from tensorboard.backend.event_processing import event_accumulator
    size_to_output_mses = defaultdict(list)
    size_to_latent_mses = defaultdict(list)
    # 107 to 171
    for version in version_range:
        path = Path(__file__).parent / f'tb_logs/{dataset}/version_{version}'
        if not path.exists():
            continue

        event_acc = event_accumulator.EventAccumulator(str(path), size_guidance={'scalars': 0})
        event_acc.Reload()
        output_mse = min(map(lambda x: x.value, event_acc.Scalars('mse_output')))
        latent_mse = min(map(lambda x: x.value, event_acc.Scalars('mse_latent')))
        with open(path / 'hydra/.hydra/config.yaml') as f:
            train_cfg = yaml.safe_load(f)
        size = train_cfg[f"dataset_{train_cfg['training']['dataset']}"]['n_training_tasks']
        size_to_output_mses[size].append(output_mse)
        size_to_latent_mses[size].append(latent_mse)
        print(f'Version {version} with size {size}: Latent MSE: {latent_mse:.04f}, Output MSE: {output_mse:.04f}')

    fig, ax = plt.subplots(figsize=(5, 4))

    def plt_mses(ax, mses, color):
        x = list(mses.keys())
        map_y = lambda y, fn: np.array(list(map(fn, y)))
        y = map_y(mses.values(), np.mean)
        yerr = map_y(mses.values(), np.std)
        order = np.argsort(x)
        x, y, yerr = np.array(x)[order], y[order], yerr[order]
        ln = ax.plot(
            x,
            y,
            c=color
        )
        ax.fill_between(x, y - yerr, y + yerr, alpha=0.2, color=color)
        return ln
    ln1 = plt_mses(ax, size_to_output_mses, 'C0')
    ax2 = ax.twinx()
    ln2 = plt_mses(ax2, size_to_latent_mses, 'C1')

    ax.set_ylabel('Output MSE')
    ln3 = ax.axhline(0.0155, ls='--', c='C0', alpha=0.5)
    ax2.set_ylabel('Latent MSE')
    ln4 = ax2.axhline(0.117, ls='--', c='C1', alpha=0.5)
    ax.set_xlabel('Number of training tasks')
    plt.legend(ln1 + ln2 + [ln3, ln4], ['Output MSE (ours)', 'Latent MSE (ours)', 'Output MSE (Alfi)', 'Latent MSE (Alfi)'])
    save_path = Path(__file__).parent / f'tb_logs/{dataset}/mses_{version_range[0]}_{version_range[-1]}.pdf'
    plt.savefig(save_path, bbox_inches="tight")
    # return size_to_output_mses, size_to_latent_mses

def plot_results_transcriptomics(model: DKLFMWrapper, real_dataset, synthetic_dataset, save_dir):
    y_scaler = f_scaler = None
    if (save_dir.parent / 'y_scaler.pt').exists():
        y_scaler = torch.load(save_dir.parent / 'y_scaler.pt')
        f_scaler = torch.load(save_dir.parent / 'f_scaler.pt')
        real_y_scaler = torch.load(save_dir.parent / 'real_y_scaler.pt')
        real_f_scaler = torch.load(save_dir.parent / 'real_f_scaler.pt')

    # Plot synthetic results
    t_min = synthetic_dataset.timepoints.min()
    t_max = synthetic_dataset.timepoints.max()
    t_range = (t_max - t_min) * 0.1
    ylabels = ['mRNA count', 'mRNA count']
    t_predict = torch.linspace(t_min - t_range, t_max + t_range, 30, dtype=torch.float64, device=model.device)
    plotter = DeepKernelLFMPlotter(model.model, synthetic_dataset, t_predict, y_scaler, f_scaler)
    for i in tqdm(range(20, 30)):
        plotter.plot_results(i, plot_dists=False, by_row=False, ylabels=ylabels)
        plt.savefig(save_dir / f'synthetic_{i}.pdf', bbox_inches='tight')

    # Plot real results
    t_min = real_dataset.timepoints.min()
    t_max = real_dataset.timepoints.max()
    t_range = (t_max - t_min) * 0.1
    t_predict = torch.linspace(t_min - t_range, t_max + t_range, 500, dtype=torch.float32, device=model.device)
    plotter = DeepKernelLFMPlotter(model.model, real_dataset, t_predict, real_y_scaler, real_f_scaler)
    out_loc = torch.load('../out.loc.pt').detach().t()
    out_f_loc = torch.load('../var_out_f.loc.pt').detach().t()
    print(out_f_loc.shape, 'shape', real_dataset.timepoints.shape)
    out_t_predict = torch.linspace(0, 1, out_f_loc.shape[0])  # torch.load('../t_predict.pt').detach()
    t = out_t_predict

    print(out_f_loc.shape, 'f')
    out_t_predict /= out_t_predict.max()
    out_t_predict *= t_max

    print(real_dataset.y_cond.shape, 'ycond')
    for task_index in tqdm(range(3)):
        fig, axes = plt.subplots(figsize=(10, 4), ncols=2)

        y_pred = plotter.mean[task_index].cpu(), plotter.var[task_index].cpu()
        f_pred = plotter.mean_f[task_index].cpu(), plotter.var_f[task_index].sqrt().cpu() * 2
        y_data = plotter.y_scaler.inv_scale(plotter.dataset.y)[task_index].t().detach()
        f_shape = (plotter.n_task, 1, -1)
        f_data = plotter.f_scaler.inv_scale(plotter.dataset.f)[task_index].squeeze()
        f_cond = None if plotter.dataset.f_cond is None else \
        plotter.f_scaler.inv_scale(plotter.dataset.f_cond.view(f_shape))[task_index].squeeze()
        _train_y = plotter.y_scaler.inv_scale(plotter.dataset.y_cond.view(plotter.n_task, plotter.n_functions, -1))
        y_cond = _train_y[task_index]
        # print(t.shape, y.shape, f.shape)
        axes[0].margins(x=0)
        axes[1].margins(x=0)
        plotter.plot_result(
            axes, t_predict.cpu(), y_pred, f_pred, plotter.dataset.timepoints,
            t_cond=real_dataset.timepoints_cond, y_cond=y_cond, f_cond=0.1 + softplus(out_f_loc),
            t_f_cond=t / t.max() * t_max, ylabels=ylabels
        )
        axes[0].set_ylim(-1.5, 2.5)
        axes[1].set_ylim(-1, 3)
        plt.tight_layout()
        plt.savefig(save_dir / f'real_{task_index}.pdf', bbox_inches='tight')


plotters = {
    'transcriptomics': plot_results_transcriptomics,
    'lotkavolterra': plot_results_transcriptomics,
}

def plot(cfg: DictConfig):
    version = cfg['version']
    root_dir = Path(__file__).parent
    if version == 'latest':
        save_dir = list(sorted((root_dir / f'tb_logs/{cfg["dataset"]}').iterdir(), key=lambda x: int(x.stem.split('_')[1])))[-1]
    else:
        save_dir = root_dir / f"tb_logs/{cfg['dataset']}/version_{version}"
    print(save_dir)
    with open(f"{save_dir}/hydra/.hydra/config.yaml") as f:
        train_cfg = yaml.safe_load(f)


    # Load data
    synthetic_dataset, real_dataset, scaler_modules = load_dataset(train_cfg, scaler_dir=Path(save_dir))
    batch_size = train_cfg['training']['batch_size']
    train_loader = DataLoader(synthetic_dataset, batch_size=batch_size)
    test_loader = None

    # Instantiate the model
    path = f"{save_dir}/checkpoints/last.ckpt"
    train_cfg['model']['ckpt_path'] = path
    model = get_model(train_cfg, synthetic_dataset, scaler_modules)
    save_dir = Path(save_dir) / 'evaluation'
    save_dir.mkdir(exist_ok=True)

    plotters[train_cfg['training']['dataset']](model, real_dataset, synthetic_dataset, Path(save_dir))

@hydra.main(version_base=None, config_path="conf", config_name="eval")
def app(cfg: DictConfig):
    if cfg['plots'] == 'mse':
        plot_mses(dataset='transcriptomics', version_range=range(100, 172))
        return

    if isinstance(cfg['version'], ListConfig):
        for version in cfg['version']:
            _cfg = cfg.copy()
            _cfg['version'] = version
            try:
                plot(_cfg)
            except Exception as e:
                raise (e)
    else:
        plot(cfg)


if __name__ == '__main__':
    sys.argv.append('hydra.job.chdir=False')
    app()
