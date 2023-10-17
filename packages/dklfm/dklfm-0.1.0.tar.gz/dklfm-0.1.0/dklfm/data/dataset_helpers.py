import numpy as np
import torch
import gpytorch
from torch.optim import Adam
from gpytorch.kernels import RBFKernel
from gpytorch.likelihoods import MultitaskGaussianLikelihood
from gpytorch.mlls import VariationalELBO
from matplotlib import pyplot as plt
from torch.utils.data import TensorDataset
from tqdm import tqdm

from alfi.datasets import ToyTranscriptomics, ToyTranscriptomicGenerator, P53Data
from dklfm.data.dklfm_dataset import DeepKernelLFMDataset
from alfi.models import generate_multioutput_gp
from alfi.utilities.torch import spline_interpolate_gradient, softplus
from dklfm.data.velo_dataset import VeloDataset, get_initial_parameters
from dklfm import sc_rna_dir


def synthetic_transcriptomics(load=True, data_dir='../../../data', num_genes=5, num_tfs=1, scalers=None, scale_x_max=False, n_training_instances=500, n_test_instances=1.):
    if load:
        toy_dataset = ToyTranscriptomics(data_dir=data_dir)
    else:
        toy_dataset = ToyTranscriptomicGenerator(
            num_outputs=num_genes, num_latents=num_tfs, num_times=10, softplus=True, latent_data_present=True)
        toy_dataset.generate(500, 100, '../../../data/')

    num_tasks = len(toy_dataset.train_data) + len(toy_dataset.test_data)
    y = torch.from_numpy(np.stack([
        [*toy_dataset.train_data, *toy_dataset.test_data][i][0] for i in range(num_tasks)
    ])).permute(0, 2, 1)
    f = torch.from_numpy(np.stack([
        [*toy_dataset.train_data, *toy_dataset.test_data][i][1] for i in range(num_tasks)
    ])).permute(0, 2, 1)
    timepoints = y[0, 0].type(torch.float64)
    y = y[:, 1:]
    f = softplus(f)
    if scalers:
        y_scaler, f_scaler = scalers
        y = y_scaler.scale(y).type(torch.float64)
        f = f_scaler.scale(f).type(torch.float64)

    if scale_x_max:
        timepoints = timepoints / timepoints.max()
    synth_trans_dataset = DeepKernelLFMDataset(
        timepoints, y, f,
        n_train=9, n_training_instances=n_training_instances, n_test_instances=n_test_instances
    )
    return synth_trans_dataset


def p53_transcriptomics(t_scale=1.0, data_dir='../../alfi/data', scalers=None, scale_x_max=False):
    real_dataset = P53Data(data_dir=data_dir)
    y = real_dataset.m_observed.type(torch.float64)
    f = real_dataset.f_observed.repeat(3, 1, 1).type(torch.float64)
    t = real_dataset.t_observed * t_scale
    _, y, _, _ = spline_interpolate_gradient(t, y.transpose(-2, -1), num_disc=2)
    t, f, _, _ = spline_interpolate_gradient(t, f.transpose(-2, -1), num_disc=2)
    y = y.transpose(-2, -1)
    f = f.transpose(-2, -1)
    if scalers:
        y_scaler, f_scaler = scalers
        y = y_scaler.scale(y).type(torch.float64)
        f = f_scaler.scale(f).type(torch.float64)
    if scale_x_max:
        t = t / t.max()
    return DeepKernelLFMDataset(t, y, f, n_train=10)


def from_loom(
        dataset_name='pancreas', load=True,
        scalers=None,
        plot=False, cell_type_key='clusters', calculate_slingshot=True, interpolate=True, include_loom=False):

    if dataset_name == 'pancreas':
        gene_index = 1710
        start_node = 1
    else:
        gene_index = 1175
        start_node = 5
    if dataset_name == 'pancreas':
        gene_indices = np.array([
            1588,  # actn4
            1182,  # ppp3ca
            1710,  # Cpe
            1072,  # Nnat
            *list(np.random.randint(0, 2000, 100))
        ])
    elif dataset_name == 'gastrulation':
        gene_indices = np.array([
            312,
            313,
            314,
            *list(np.random.randint(0, 2000, 101))
        ])

    velo_dataset = VeloDataset.from_config(
        dataset=dataset_name,
        gene_indices=gene_indices,
        cell_mask=None,
        cell_type_key=cell_type_key,
        # subset_margin=100
    )
    y = torch.stack(velo_dataset.data).type(torch.float64)
    y = y.reshape(2, 104, -1).permute(1, 0, 2)
    x = torch.linspace(0, 26, y.shape[-1])
    pseudotime = None
    if calculate_slingshot:
        from slingshot import Slingshot
        x = torch.linspace(0, 26, 1000)
        x_umap = velo_dataset.loom.obsm['X_umap']
        if plot:
            plt.scatter(x_umap[:, 0], x_umap[:, 1], c=velo_dataset.cell_colors, s=5)
        slingshot = Slingshot(x_umap, velo_dataset.cluster_labels_onehot, start_node=start_node)
        if load and (velo_dataset.data_path / dataset_name / 'sling_params.npy').exists():
            slingshot.load_params(velo_dataset.data_path / dataset_name / 'sling_params.npy')
        else:
            if plot:
                fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
                custom_xlim = (-15, 15)
                custom_ylim = (-12, 15)
                plt.setp(axes, xlim=custom_xlim, ylim=custom_ylim)
            else:
                axes = None
                plt.ioff()
            slingshot.fit(num_epochs=3, debug_axes=axes)
            slingshot.save_params(velo_dataset.data_path / dataset_name / 'sling_params.npy')
            plt.ion()

        pseudotime = slingshot.unified_pseudotime
        if plot:
            fig, axes = plt.subplots(ncols=2, figsize=(12, 4))
            axes[0].set_title('Clusters')
            axes[1].set_title('Pseudotime')
            slingshot.plotter.curves(axes[0], slingshot.curves)
            slingshot.plotter.clusters(axes[0], labels=list(velo_dataset.unique_cell_types.keys()), s=4, alpha=0.5)
            slingshot.plotter.curves(axes[1], slingshot.curves)
            slingshot.plotter.clusters(axes[1], color_mode='pseudotime', s=5)
        y = y[..., np.argsort(pseudotime)]
        pseudotime = torch.from_numpy(np.sort(pseudotime))

        dist_matrix = (x.reshape(1, -1) - pseudotime.reshape(-1, 1)) ** 2
        # each row contains the distance of all points to the linspace
        assignments = dist_matrix.argmin(dim=0)
        # each element is the assignment index of each time onto a specific cell
        # some times will be assigned to the same cell, so we take the first assignment
        assignments, indices = torch.unique_consecutive(assignments, return_inverse=True)
        indices = torch.unique_consecutive(indices)
        x, y = x[indices], y[:, :, assignments]

    if pseudotime is not None and interpolate:
        # now we can interpolate, since we have unique timepoints
        x_interpolate, y_interpolate, y_grad, y_grad_2 = spline_interpolate_gradient(x, y.transpose(-2, -1), num_disc=1)
        if plot:
            plt.scatter(x, y[2, 0], s=5)
            plt.plot(x_interpolate, y_interpolate[2, :, 0])
        y = y_interpolate.transpose(-2, -1)
        x = x_interpolate
    if scalers is not None:
        y_scaler, _ = scalers
        y = y_scaler.scale(y)
    real_dataset = DeepKernelLFMDataset(x, y, n_train=0.1)
    if calculate_slingshot:
        real_dataset.slingshot = slingshot
    if plot:
        plt.figure()
        plt.scatter(real_dataset.timepoints_cond, real_dataset.y_cond[2].reshape(2, -1)[0], s=5, alpha=0.5)
    if include_loom:
        real_dataset.loom = velo_dataset.loom[:, gene_indices].copy()
    return real_dataset


def create_or_load_synthetic(
        num_cells=512, end_t=25., scalers=None, scale_x_max=False,
        n_train=30, n_training_tasks=256,
        load=True, gene_indices=None, save_dir=sc_rna_dir, save_suffix='with_velocities_v5', plot=False, return_type='DKLFM'):
    timepoints = torch.linspace(0, end_t, num_cells)

    if load:
        synthetic_dataset = torch.load(save_dir / f'./synthetic_dataset_{save_suffix}.pt')
    else:
        # Dataset generation
        trans, splic, decay = get_initial_parameters('pancreas')
        if gene_indices is None:
            gene_indices = np.arange(trans.shape[0])
        f = lambda x: torch.tensor(x)[gene_indices].unsqueeze(-1)
        splicing_rate = f(splic)
        splicing_rate = splicing_rate.nan_to_num(splicing_rate.nan_to_num(0).mean())
        transcription_rate = f(trans).nan_to_num(0.2)
        decay_rate = f(decay).nan_to_num(0.2)

        assert isinstance(n_train, int), 'n_train must be an integer for generating synthetic data'
        synthetic_dataset = generate_synthetic_dataset(
            transcription_rate, splicing_rate, decay_rate, num_cells, timepoints, num_data=n_train
        )
        torch.save(synthetic_dataset, save_dir / f'./synthetic_dataset_{save_suffix}.pt')

    f = synthetic_dataset[:][1].transpose(1, 2).type(torch.float64)
    y = synthetic_dataset[:][0].transpose(1, 2).type(torch.float64)  # s, u (N, T, 2) -> (N, 2, T)
    timepoints = torch.linspace(0, end_t, y.shape[-1])

    f = softplus(f)
    if plot:
        plt.figure()
        plt.scatter(y[1, 0], y[1, 1], c='blue')
    if scalers is not None:
        y_scaler, f_scaler = scalers
        y = y_scaler.scale(y)
        f = f_scaler.scale(f)
    if plot:
        plt.scatter(y[1, 0], y[1, 1], s=5, c='red')
    if y.shape[-1] != num_cells:
        indices = np.random.permutation(np.arange(y.shape[-1]))[:num_cells]
        y = y[..., indices]
        f = f[..., indices]
        timepoints = timepoints[indices]
        synthetic_dataset = TensorDataset(*[synthetic_dataset[:][i][:, indices] for i in range(len(synthetic_dataset[:]))])
    if return_type == 'DKLFM':
        return DeepKernelLFMDataset(timepoints, y, f, n_train=n_train, n_training_instances=n_training_tasks, scale_x_max=scale_x_max)
    else:
        return timepoints, synthetic_dataset


def generate_synthetic_dataset(transcription_rate, splicing_rate, decay_rate, num_cells, timepoints, num_data=1, f=None):
    from velocity.models import RNAVelocityConfiguration, RNAVelocityLFM

    x_datapoints = list()
    y_datapoints = list()
    d_datapoints = list()
    lengthscale = 7
    class ExactGPModel(gpytorch.models.ExactGP):
        def __init__(self, likelihood=gpytorch.likelihoods.GaussianLikelihood()):
            super(ExactGPModel, self).__init__(None, None, likelihood)
            self.mean_module = gpytorch.means.ConstantMean()
            self.covar_module = gpytorch.kernels.ScaleKernel(gpytorch.kernels.RBFKernel())
            self.covar_module.base_kernel.lengthscale *= 0
            self.covar_module.base_kernel.lengthscale += lengthscale
            # print('lengthscale, ', lengthscale , self.covar_module.base_kernel.lengthscale)
            self.covar_module.outputscale *= 12

        def forward(self, x):
            mean_x = self.mean_module(x)
            covar_x = self.covar_module(x)
            return gpytorch.distributions.MultivariateNormal(mean_x, covar_x)

    # print(transcription_rate.shape)
    splicing_lower = torch.quantile(splicing_rate, .2)
    splicing_higher = torch.quantile(splicing_rate, .9)
    splicing_mean = (splicing_lower + splicing_higher) / 2
    decay_lower = torch.quantile(decay_rate, 0.2)
    decay_higher = torch.quantile(decay_rate, .89)
    decay_mean = (decay_lower + decay_higher) / 2
    num_genes = 1
    num_inducing = 25
    num_timepoint_choices = 150
    use_natural = False
    print(f'Constructing model for {num_cells} cells')
    for i in tqdm(range(num_data)):
        # Initialise GP
        decay = np.random.uniform(decay_lower, decay_higher, num_genes)
        splicing = np.random.normal(splicing_mean, .5, num_genes)
        transcription = np.random.uniform(3., 4.5, num_genes)
        # transcription = np.random.normal(1., .2, num_genes)
        # print("decay ranges", decay_lower, decay_higher, 'actual', decay)
        # print('splicing mean', splicing_mean, 'actual', splicing)
        # print('transcription uniform', 3., 4.5, 'actual', transcription)
        decay[decay > 6] = 6.
        if any(decay < 0):
            continue
        if any(splicing < 0):
            continue

        inducing_points = torch.linspace(0, timepoints.max(), num_inducing) \
            .repeat(num_genes, 1) \
            .view(num_genes, num_inducing, 1)

        gp_model = generate_multioutput_gp(num_genes, inducing_points,
                                           kernel_class=RBFKernel,
                                           kernel_kwargs=dict(nu=1.5),
                                           zero_mean=False,
                                           use_scale=False, initial_lengthscale=lengthscale,
                                           gp_kwargs=dict(natural=use_natural))
        if f is None or i > 0:
            # Train GP
            gp = ExactGPModel()
            gp.eval()
            timepoints = timepoints.cpu()
            with gpytorch.settings.prior_mode(True):
                f = gp(timepoints).sample(torch.Size([1])).t()
                # f = 1000*gp_model(timepoints).mean.detach()
                # print(f.shape)
        # fig, axes = plt.subplots(ncols=2)
        optimizer = Adam(gp_model.parameters(), lr=1e-2)
        likelihood = MultitaskGaussianLikelihood(num_tasks=1)
        likelihood = likelihood.cuda()
        timepoints = timepoints.cuda()
        gp_model = gp_model.cuda()
        f = f.cuda()
        likelihood.train()
        loss_fn = VariationalELBO(likelihood, gp_model, num_data=timepoints.shape[0])
        gp_model.train()
        for _ in range(200):
            optimizer.zero_grad()
            out = gp_model(timepoints)
            loss = -loss_fn(out, f)
            loss.backward()
            optimizer.step()
        f_gpmodel = out.mean.detach()
        gp_model.eval()
        num_inducing = 25  # (I x m x 1)
        config = RNAVelocityConfiguration(
            latent_data_present=False,
            num_samples=50,
            num_cells=num_cells,
            end_pseudotime=timepoints.max(),
            num_timepoint_choices=num_timepoint_choices
        )

        num_data = num_cells  # config.num_timepoint_choices

        lfm = RNAVelocityLFM(
            2, gp_model, config,
            nonlinearity=softplus,
            num_training_points=num_data,
            time_assignments=timepoints,
            splicing_rate=torch.from_numpy(splicing).cuda(),
            decay_rate=torch.from_numpy(decay).cuda(),
            transcription_rate=torch.from_numpy(transcription).cuda(),
            return_derivatives=True,
        )
        lfm = lfm.cuda()
        # axes[0].plot(lfm.nonlinearity(f))
        # axes[0].plot(lfm.nonlinearity(gp_model(timepoints).sample(torch.Size([10])).squeeze().t()), alpha=0.5, c='b')
        out, derivatives = lfm(timepoints)

        if torch.isnan(out.mean).any():
            continue
        # axes[1].plot(out.sample(torch.Size([5])).mean(0))
        x_datapoints.append(out.sample(torch.Size([3])).mean(0).cpu())
        y_datapoints.append(f.cpu())
        d_datapoints.append(derivatives.squeeze().t().cpu())

    x_dataset = torch.stack(x_datapoints).to(torch.float32)
    y_dataset = torch.stack(y_datapoints).to(torch.float32)
    d_dataset = torch.stack(d_datapoints).to(torch.float32)

    filt = torch.isinf(x_dataset).any(dim=1).any(dim=1)
    y_dataset = y_dataset[~filt]
    x_dataset = x_dataset[~filt]
    d_dataset = d_dataset[~filt]
    dataset = TensorDataset(x_dataset, y_dataset, d_dataset)
    return dataset