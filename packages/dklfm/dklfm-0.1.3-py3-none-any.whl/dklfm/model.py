import torch
import gpytorch
from gpytorch.distributions import MultivariateNormal
import matplotlib.pyplot as plt
import pytorch_lightning as pl

from dklfm.warmup_lr_scheduler import CosineWarmupScheduler
from alfi.utilities.data import create_tx


class DeepKernelLFM(gpytorch.models.ExactGP):
    def __init__(self, train_x, train_y, train_f, likelihood, likelihood_f, deepkernel, num_functions=2, embedder=None, kernel='rbf', kernel_in_dims=8, include_embedding='f'):
        super().__init__(train_x, train_y, likelihood)
        self.train_y = train_y
        self.train_f = train_f
        self.likelihood_f = likelihood_f
        self.deepkernel = deepkernel
        self.embedder_model, self.embedder = embedder if embedder is not None else (None, None)
        self.include_embedding = include_embedding
        self.mean_module = gpytorch.means.ConstantMean().type(torch.float64)
        self.mean_module_f = gpytorch.means.ConstantMean().type(torch.float64)
        # self.mean_1 = torch.nn.Parameter(torch.zeros(1))
        # self.mean_2 = torch.nn.Parameter(torch.zeros(1))
        if kernel == 'rbf':
            self.covar_module = gpytorch.kernels.ScaleKernel(
                gpytorch.kernels.RBFKernel(ard_num_dims=kernel_in_dims+2)
            ).type(torch.float64)
        else:
            self.covar_module = gpytorch.kernels.ScaleKernel(
                gpytorch.kernels.PeriodicKernel(ard_num_dims=kernel_in_dims+2)
            ).type(torch.float64)

        embedding_scale_bounds = (0., 1.)
        b = 1.
        self.scale_to_bounds = gpytorch.utils.grid.ScaleToBounds(-b, b)
        self.scale_to_bounds_em = gpytorch.utils.grid.ScaleToBounds(*embedding_scale_bounds)
        self.num_functions = num_functions
        self.hn = None  # (n_task, n_functions, embedding_size)
        self.debug = False

    def cat_embedding(self, t, is_blocked=True):
        """
        Concatenates the embedding onto t
        Args:
            t: (num_task, T, 1) or (num_task, T * n_functions, 1) if is_blocked
            is_blocked: boolean indicating whether t is a blocked timepoint vector
        """
        # Reshape inputs (T) -> (num_task, T * num_functions, 1)
        # inputs = self.scale_to_bounds(inputs)
        n_task = t.shape[0]
        if self.debug and not self.training:
            plt.figure()
            plt.plot(t[0].squeeze())
            plt.title('inputs')
            print("GET_INPUTS called", t.shape)

        embedding_size = self.hn.shape[-1]
        # embedding = self.scale_to_bounds_em(self.hn)
        embedding = self.hn
        num_blocks = embedding.shape[1]
        num_points = t.shape[1]
        block_size = num_points // self.num_functions
        if is_blocked:
            embedding_shaped = torch.empty(n_task, num_points, embedding_size, device=t.device)
            for i in range(num_blocks):
                start_index = i * block_size
                end_index = (i+1) * block_size
                embedding_shaped[:, start_index:end_index] = embedding[:, i].unsqueeze(1)
            embedding = embedding_shaped
        else:
            embedding_shaped = torch.empty(n_task, num_points, embedding_size, device=t.device)
            embedding_shaped[:, :] = embedding.sum(dim=1).unsqueeze(1)
            # embedding_shaped[:, :] = embedding[:, 0].unsqueeze(1) + embedding[:, 1].unsqueeze(1)
            embedding = embedding_shaped
            # embedding = embedding.reshape(embedding.shape[0],  1, -1).repeat(1, num_points, 1)
        # if diff > 0:
        #     embedding_shaped[:, num_train:num_train + diff // self.num_functions] = embedding[:, 0].unsqueeze(1)
        #     embedding_shaped[:, num_train + diff // self.num_functions:] = embedding[:, 1].unsqueeze(1)

        if self.debug and not self.training:
            print('embedding shape', embedding.shape)
            plt.figure()
            plt.plot(embedding.mean(-1).detach()[0])
            plt.title('emb')

        # embedding = embedding.reshape(self.num_functions, 1, embedding_size)  # (n_task, n_functions, 1, embedding_size)
        # embedding = embedding.repeat(1, num_train // self.num_functions, 1)  # -> (n_task, n_functions, T, embedding_size)
        # embedding = embedding.reshape(-1, embedding_size)  # -> (n_task, n_functions * T, embedding_size)
        # embedding = embedding.reshape(n_task, self.num_functions, 1, embedding_size)  # (n_task, n_functions, 1, embedding_size)
        # embedding = embedding.repeat(1, t_x.shape[1] // self.num_functions, 1)  # -> (n_task, n_functions, T, embedding_size)
        # embedding = embedding.reshape(n_task, -1, embedding_size)  # -> (n_task, n_functions * T, embedding_size)
        return torch.cat([t, embedding], dim=-1)  # (n_task, n_functions * T, embedding_size + 1

    def kxf(self, t_x, t_f):
        """
        First, convert the input times t_x and t_f into higher-dimensional objects,
        so we have a D-dimensional vector for each timepoint.
        Args:
            t_x: (num_task, T * n_functions, 1)
            t_f: (num_task, T', 1)
        """
        x_projected_a = self.project_x(t_x)
        # diff = x_projected_a[:, : x_projected_a.shape[1] // n_functions] - x_projected_a[:, x_projected_a.shape[1] // n_functions:]
        # print('xf projected diff', diff[diff < 1e-2])

        t_projected = self.project_f(t_f)
        return self.covar_module(x_projected_a, t_projected)

    def kff(self, ta, tb):
        t_projected_a = self.project_f(ta)
        # plt.figure()
        # plt.title('inputs to Kff, one task')
        # pca = PCA(n_components=2)
        # print('tproj', t_projected_a[0].shape)
        # x = pca.fit_transform(t_projected_a.detach()[0])
        # plt.xlabel('component 1')
        # plt.ylabel('component 2')
        # print(x.shape, ta.shape)
        # plt.scatter(x[:, 0], x[:, 1], c=ta[0].squeeze())
        if ta.shape[1] == tb.shape[1] and torch.all(ta == tb):
            return self.covar_module(t_projected_a)
        t_projected_b = self.project_f(tb)

        return self.covar_module(t_projected_a, t_projected_b)

    def kxx(self, xa, xb):
        x_projected_a = self.project_x(xa)

        if xa.shape[1] == xb.shape[1] and torch.all(xa == xb):
            return self.covar_module(x_projected_a)

        x_projected_b = self.project_x(xb)
        return self.covar_module(x_projected_a, x_projected_b)

    def scale(self, x):
        # return x
        return self.scale_to_bounds(x)

    def project_x(self, t):
        t_scaled = t

        t_emb = t_scaled

        if self.embedder is not None:
            if self.include_embedding == 'y':
                t_emb = self.cat_embedding(t_scaled)
            else:
                embedding_size = self.hn.shape[-1]
                t_emb = torch.cat([
                   t_scaled,
                   torch.zeros(t_scaled.shape[0], t_scaled.shape[1], embedding_size, device=t_scaled.device)
                ], dim=-1)

        emb = self.deepkernel(t_emb, use_output_head=True)
        # emb = self.scale(emb)
        emb = torch.cat([emb, t_scaled], dim=-1)
        return emb

    def project_f(self, t):
        t_scaled = t

        t_emb = t_scaled
        if self.embedder is not None:
            if self.include_embedding == 'f':
                t_emb = self.cat_embedding(t_scaled, is_blocked=False)
            else:
                embedding_size = self.hn.shape[-1]
                t_emb = torch.cat([
                   t_scaled,
                   torch.zeros(t_scaled.shape[0], t_scaled.shape[1], embedding_size, device=t_scaled.device)
                ], dim=-1)

        emb = self.deepkernel(t_emb, use_output_head=False)
        # emb = t_emb
        # emb = self.scale(emb)
        emb = torch.cat([emb, t_scaled], dim=-1)

        return emb

    # def mean_module(self, xa):
    #     length = len(xa) // 2
    #     return torch.cat([self.mean_1.repeat(length), self.mean_2.repeat(length)])
    def compute_embedding(self, y_cond, x_cond=None):
        if self.embedder is not None:
            n_task = y_cond.shape[0]
            y_reshaped = y_cond.reshape(n_task, self.num_functions, -1).reshape(n_task * self.num_functions, -1, 1)  # (n_task, n_functions, T -> n_task * n_functions, T, 1)
            self.hn = self.embedder(y_reshaped, x_cond=x_cond).reshape(n_task, self.num_functions, -1)

    def __call__(self, *args, **kwargs):
        y_reshaped = args[0]
        self.compute_embedding(y_reshaped)

        return super().__call__(*args[1:], **kwargs)

    def latent_prior(self, x_pred):
        prior_mean = self.mean_module_f(x_pred)
        #torch.zeros(t_f.shape[1], dtype=torch.float64).unsqueeze(0).repeat(t_f.shape[0], 1)
        prior_cov = self.kff(x_pred, x_pred) + torch.eye(x_pred.shape[1], dtype=torch.float64) * 1e-7
        return MultivariateNormal(prior_mean, prior_cov.to(x_pred.device))

    def output_prior(self, t_x):
        return MultivariateNormal(
            self.mean_module(t_x),
            self.kxx(t_x, t_x) + torch.eye(t_x.shape[1], dtype=torch.float64, device=t_x.device) * 1e-6
        )

    def get_conditioning_or_default(self, x_cond, y_cond):
        """
        Returns the conditioning data or the training conditioning if not exist.
        """
        if x_cond is None:
            x_cond = self.train_inputs[0]
        if y_cond is None:
            y_cond = self.train_y
        return x_cond, y_cond

    def predictive(self, y_cond, x_pred, x_cond_blocks=None):
        """
        Args:
            y_cond: the output conditioning data
            x_pred: the timepoints to be predicted
            x_cond_blocks: the time inputs that is conditioned (n_task, T*n_functions) if None, then train_inputs are used.
        """
        x_cond_blocks, y_cond = self.get_conditioning_or_default(x_cond_blocks, y_cond)
        kxx = self.kxx(x_cond_blocks, x_cond_blocks)
        kxstarxstar = self.kxx(x_pred, x_pred)
        kxstarx = self.kxx(x_pred, x_cond_blocks)
        kxstarx_kxx_x = self.mean_module(x_pred) + kxstarx.matmul(kxx.inv_matmul(y_cond.unsqueeze(-1))).squeeze(-1)

        kxx_kxstarx_kxx_kxxstar = kxstarxstar - kxstarx.matmul(kxx.inv_matmul(kxstarx.transpose(-2, -1).evaluate()))
        kxx_kxstarx_kxx_kxxstar += torch.eye(kxx_kxstarx_kxx_kxxstar.shape[-1], device=kxx.device) * self.likelihood.noise
        return gpytorch.distributions.MultivariateNormal(kxstarx_kxx_x, kxx_kxstarx_kxx_kxxstar)

    def latent_predictive(self, x_pred, x_cond=None, y_cond=None):
        p = self.conditional_f_given_x(x_cond, x_pred=x_pred, y_cond=y_cond)
        return p.add_jitter(noise=self.likelihood_f.noise)

    def conditional_x_given_f(self, x_cond_blocks, f_cond=None):
        if f_cond is None:
            f_cond = self.train_f
        jitter = torch.eye(x_cond_blocks.shape[1] // self.num_functions, device=f_cond.device) * 1e-7
        kxx = self.kxx(x_cond_blocks, x_cond_blocks)
        kff = self.kff(
            x_cond_blocks[:, :x_cond_blocks.shape[1] // self.num_functions],
            x_cond_blocks[:, :x_cond_blocks.shape[1] // self.num_functions]
        ) + jitter
        kxf = self.kxf(x_cond_blocks, x_cond_blocks[:, :x_cond_blocks.shape[1] // self.num_functions])
        mean_cond = self.mean_module(x_cond_blocks) + kxf.matmul(kff.inv_matmul(f_cond.unsqueeze(-1))).squeeze(-1)
        k_cond = kxx - kxf.matmul(kff.inv_matmul(kxf.transpose(-1, -2).evaluate()))

        return gpytorch.distributions.MultivariateNormal(mean_cond, k_cond)

    def conditional_f_given_x(self, x_cond_blocks, x_pred=None, y_cond=None):
        """
        Args:
            x_cond_blocks: conditioning input data in blocks for each function
            x_pred: the timepoints to be predicted
            y_cond: the outputs to be conditioned on
        """
        if x_pred is None:
            x_pred = x_cond_blocks[:, :x_cond_blocks.shape[1] // self.num_functions]
        x_cond_blocks, y_cond = self.get_conditioning_or_default(x_cond_blocks, y_cond)

        jitter = torch.eye(x_pred.shape[1], device=x_pred.device, dtype=x_cond_blocks.dtype) * 1e-7
        kxx = self.kxx(x_cond_blocks, x_cond_blocks)
        kxf = self.kxf(x_cond_blocks, x_pred)  # (n_task, |x|*n_functions, |f|*n_functions)
        kff = self.kff(x_pred, x_pred) + jitter
        kfx_kxx_x = self.mean_module_f(x_pred) + kxf.transpose(-2, -1).matmul(kxx.inv_matmul(y_cond.unsqueeze(-1))).squeeze(-1)

        kff_kfx_kxx_kxf = kff - kxf.transpose(-2, -1).matmul(kxx.inv_matmul(kxf.evaluate()))

        return gpytorch.distributions.MultivariateNormal(kfx_kxx_x, kff_kfx_kxx_kxf)

    def forward(self, input):
        return self.conditional_f_given_x(input)
        # return self.conditional_x_given_f(input)


class DKLFMWrapper(pl.LightningModule):
    def __init__(self, cfg, model: DeepKernelLFM, mse_data=None, scaler_modules=None):
        super().__init__()
        self.cfg = cfg
        self.model = model
        self.mll = gpytorch.mlls.ExactMarginalLogLikelihood(self.model.likelihood, self.model)
        self.mll_f = gpytorch.mlls.ExactMarginalLogLikelihood(self.model.likelihood_f, self.model)
        self.automatic_optimization = False
        self.mse_data = mse_data
        self.scaler_modules = scaler_modules
        self.prior_weight = cfg['training']['prior_weight'] if 'prior_weight' in cfg['training'] else 1.0
        self.add_schedulers = self.cfg['training']['add_schedulers']

    def training_step(self, batch, batch_idx):
        if self.cfg['training']['alternate_likelihood']:
            if (self.current_epoch % 2) == 0:
                optimizer = self.optimizers()[0]
                likelihood_over_y = True
            else:
                optimizer = self.optimizers()[1]
                likelihood_over_y = False
        else:
            likelihood_over_y = self.cfg['training']['likelihood_over_y']
            optimizer = self.optimizers()[0 if likelihood_over_y else 1]

        optimizer.zero_grad()

        loss_batch, loss_prior, loss_cond = self.generic_step(batch, likelihood_over_y)

        self.log('train_loss', loss_batch.item())
        self.log('train_loss_prior', loss_prior.item())
        self.log('train_loss_cond', loss_cond.item())
        self.log('likelihood_noise', self.model.likelihood.noise.item())
        self.log('likelihood_f_noise', self.model.likelihood_f.noise.item())
        if self.cfg['training']['dataset'] == 'lotkavolterra':
            self.log('kernel_period', self.model.covar_module.base_kernel.period_length.mean().item())
        self.log('kernel_lengthscale', self.model.covar_module.base_kernel.lengthscale.mean().item())
        self.log('kernel_scale', self.model.covar_module.outputscale.mean().item())
        if self.cfg['training']['gradient_clip_val']:
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.cfg['training']['gradient_clip_val'])
        self.manual_backward(loss_batch)
        optimizer.step()

    def generic_step(self, batch, likelihood_over_y):
        train_x_cond_blocks, train_x_cond, train_y_cond, train_f_cond = batch

        self.model.compute_embedding(train_y_cond, x_cond=train_x_cond)
        # if (i % 2) == 0:
        if likelihood_over_y:
            # compute x | f
            output = self.model.conditional_x_given_f(train_x_cond_blocks, f_cond=train_f_cond)
            loss_cond = - self.mll(output, train_y_cond).mean()

            prior = self.model.latent_prior(train_x_cond)
            loss_prior = - (prior.log_prob(train_f_cond) / prior.event_shape.numel()).mean()
        else:
            # compute f | x
            output = self.model.conditional_f_given_x(train_x_cond_blocks, y_cond=train_y_cond)
            loss_cond = - self.mll_f(output, train_f_cond).mean()

            prior = self.model.output_prior(train_x_cond_blocks)

            loss_prior = - (prior.log_prob(train_y_cond) / prior.event_shape.numel()).mean()

        # output = model.conditional_f_given_x(train_x_cond_blocks, y_cond=train_y_cond)
        # loss_nll = - mll_f(output, train_f_cond).mean()

        # loss_nll = - model.latent_predictive(
        #     train_x_cond, x_cond=train_x_cond_blocks, y_cond=train_y_cond
        # ).log_prob(train_f_cond).mean(0) / train_f_cond.shape[-1]
        # output = model.conditional_f_given_x(train_x_cond_blocks, y_cond=train_y_cond)
        # loss_nll = - mll(output, train_f_cond).mean()

        loss_batch = loss_cond + self.prior_weight * loss_prior #+ 1. * loss_nll

        return loss_batch, loss_prior, loss_cond

    def mse_step(self):
        # n_task = self.mse_data.test_instance_indices.shape[0]
        n_task = 128
        indices = torch.cat([
            torch.arange(0, 64),
            torch.arange(self.mse_data.y_cond.shape[0] - 64, self.mse_data.y_cond.shape[0])
        ])
        y_cond = self.mse_data.y_cond[indices].to(self.device)
        x_cond = self.mse_data.x_cond[indices].to(self.device)
        x_cond_blocks = self.mse_data.x_cond_blocks[indices].to(self.device)
        t_predict = self.mse_data.timepoints

        self.model.compute_embedding(y_cond, x_cond=x_cond)

        eval_input = t_predict.reshape(1, -1, 1).repeat(n_task, self.model.num_functions, 1).type(torch.float64).to(self.device)

        eval_input_f = eval_input
        # if train_cfg['training']['dataset'] == 'reactiondiffusion':
        t_predict = t_predict[:, 0].unique()
        eval_input = create_tx(t_predict, n_task).to(self.device)
        # else:
        # eval_input_f = eval_input[:, :t_predict.shape[0]]
        latent_pred = self.model.latent_predictive(eval_input, x_cond=x_cond_blocks, y_cond=y_cond)
        output_pred = self.model.predictive(y_cond, eval_input, x_cond_blocks=x_cond_blocks)
        latent_pred = latent_pred.mean.reshape(latent_pred.mean.shape[0], 1, -1).cpu()
        output_pred = output_pred.mean.reshape(output_pred.mean.shape[0], self.model.num_functions, -1).cpu()
        output_pred = self.scaler_modules['y_scaler'].inv_scale(output_pred, indices=indices)
        latent_pred = self.scaler_modules['f_scaler'].inv_scale(latent_pred, indices=indices)
        y = self.scaler_modules['y_scaler'].inv_scale(self.mse_data.y[indices], indices=indices)
        f = self.scaler_modules['f_scaler'].inv_scale(self.mse_data.f[indices], indices=indices)
        mse_output = torch.square(output_pred - y)
        mse_latent = torch.square(latent_pred - f)
        return mse_output[:64].mean(), mse_latent[:64].mean(), mse_output[64:].mean(), mse_latent[64:].mean()

    def on_train_epoch_end(self):
        super().on_train_epoch_end()
        if self.add_schedulers:
            [lr.step() for lr in self.lr_schedulers()]

    def on_validation_epoch_end(self):
        super().on_validation_epoch_end()
        if (self.current_epoch % 5) == 0:
            with torch.no_grad():
                mse_output, mse_latent, mse_output_test, mse_latent_test = self.mse_step()
            self.log('mse_output', mse_output.item())
            self.log('mse_latent', mse_latent.item())
            self.log('mse_output_test', mse_output_test.item())
            self.log('mse_latent_test', mse_latent_test.item())

    def validation_step(self, batch, batch_idx):
        with torch.no_grad():
            loss_batch, loss_prior, loss_cond = self.generic_step(batch, likelihood_over_y=self.cfg['training']['likelihood_over_y'])
        self.log('val_loss', loss_batch.item())
        self.log('val_loss_prior', loss_prior.item())
        self.log('val_loss_cond', loss_cond.item())

    def configure_optimizers(self):
        lr = self.cfg['training']['lr']
        params = [{'params': self.parameters()}]
        if self.cfg['training']['optimizer_type'] == 'LBFGS':
            optimizer_y = torch.optim.LBFGS(params)
            optimizer_f = torch.optim.LBFGS(params)
        else:
            optimizer_y = torch.optim.Adam(params, lr=lr, weight_decay=self.cfg['training']['weight_decay'])
            optimizer_f = torch.optim.Adam(params, lr=lr, weight_decay=self.cfg['training']['weight_decay'])

        if self.add_schedulers:
            lr_scheduler_y = CosineWarmupScheduler(
                optimizer_y, warmup=self.cfg['training']['warmup'], max_iters=self.cfg['training']['warmup_max_iters']
            )
            lr_scheduler_f = CosineWarmupScheduler(
                optimizer_f, warmup=self.cfg['training']['warmup'], max_iters=self.cfg['training']['warmup_max_iters']
            )
            schedulers = [
                {'scheduler': lr_scheduler_y, 'interval': 'step'},
                {'scheduler': lr_scheduler_f, 'interval': 'step'}
            ]
            return [optimizer_y, optimizer_f], schedulers
        return [optimizer_y, optimizer_f]
