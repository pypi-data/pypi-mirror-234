from typing import Union, Optional

import torch
import numpy as np
import seaborn as sns

from pathlib import Path
from alfi.datasets import TranscriptomicTimeSeries
from dklfm import sc_rna_dir
from scvelo.datasets import dentategyrus, gastrulation


def get_initial_parameters(dataset: str):
    trans = np.load(sc_rna_dir / dataset / 'transcription_rate_initial.npy')
    splic = np.load(sc_rna_dir / dataset / 'splicing_rate_initial.npy')
    decay = np.load(sc_rna_dir / dataset / 'decay_rate_initial.npy')
    return trans, splic, decay


class VeloDataset(TranscriptomicTimeSeries):

    def __init__(self,
                 dataset='pancreas',
                 max_cells=10000, max_genes=2000,
                 gene_indices: Optional[np.ndarray] = None, cell_mask=None,
                 data_dir='../data/',
                 calc_moments=True,
                 load=True,
                 cell_type_key='clusters'
                 ):
        super().__init__()
        self.dataset = dataset
        if gene_indices is None:
            self.num_outputs = 4000
        elif type(gene_indices) is np.ndarray:
            self.num_outputs = gene_indices.shape[0]
        else:
            self.num_outputs = 2

        self.data_path = Path(data_dir)
        cache_path = self.data_path / dataset / f'{dataset}.pt'
        if not cache_path.exists() or not load:
            self.cache_data(max_cells, max_genes, calc_moments)

        data = torch.load(cache_path)
        if gene_indices is None:
            self.m_observed = data['m_observed']
            self.data = data['data']
        elif type(gene_indices) is np.ndarray:
            self.m_observed = data['m_observed'][:, [*gene_indices, *(2000 + gene_indices)]]
            self.data = [data['data'][i] for i in np.concatenate([gene_indices, 2000 + gene_indices])]

        self.gene_names = data['gene_names']
        self.loom = data['loom']
        if cell_mask is not None:
            self.m_observed = self.m_observed[..., cell_mask]
            self.data[0] = self.data[0][..., cell_mask]
            self.data[1] = self.data[1][..., cell_mask]
            self.loom = self.loom[cell_mask]

        if cell_type_key in self.loom.obs:
            cell_types = self.loom.obs[cell_type_key]
            unique_cell_types = cell_types.unique()
            colors = np.array(sns.color_palette(n_colors=len(unique_cell_types)))
            self.unique_cell_types = dict(zip(unique_cell_types, range(len(unique_cell_types))))
            cell_types = cell_types.map(lambda x: self.unique_cell_types[x])
            self.cell_colors = colors[cell_types.to_numpy()]
            cluster_labels = cell_types.to_numpy()
            self.cluster_labels_onehot = np.zeros((cluster_labels.shape[0], cluster_labels.max() + 1))
            self.cluster_labels_onehot[np.arange(cluster_labels.shape[0]), cluster_labels] = 1

    def cache_data(self, max_cells, max_genes, calc_moments):
        import scvelo as scv

        if self.dataset == 'pancreas':
            filename = self.data_path / self.dataset / 'endocrinogenesis_day15.h5ad'
            data = scv.read(filename, sparse=True, cache=True)
            data.var_names_make_unique()
        elif self.dataset == 'dentategyrus':
            data = dentategyrus()
        elif self.dataset == 'gastrulation':
            data = gastrulation()
        else:
            filename = self.data_path / f'{self.dataset}.loom'
            data = scv.read(filename, sparse=True, cache=True)
        scv.pp.filter_and_normalize(data, min_shared_counts=20, n_top_genes=max_genes)
        u = data.layers['unspliced'].toarray()[:max_cells]
        s = data.layers['spliced'].toarray()[:max_cells]
        if calc_moments:
            scv.pp.moments(data, n_neighbors=30, n_pcs=30)
            u = data.layers['Mu']
            s = data.layers['Ms']
        # scaling = u.std(axis=0) / s.std(axis=0)
        # u /= np.expand_dims(scaling, 0)

        loom = data
        gene_names = loom.var.index
        data = np.concatenate([s, u], axis=1)
        num_cells = data.shape[0]
        num_genes = data.shape[1] // 2
        data = torch.tensor(data.swapaxes(0, 1).reshape(num_genes * 2, 1, num_cells))
        m_observed = data.permute(1, 0, 2)

        data = list(data)
        (self.data_path / self.dataset).mkdir(exist_ok=True)
        torch.save({
            'data': data,
            'm_observed': m_observed,
            'gene_names': gene_names,
            'loom': loom,
        }, self.data_path / self.dataset / f'{self.dataset}.pt')

    @classmethod
    def from_config(cls, dataset='pancreas', gene_indices: Optional[Union[int, np.ndarray]] = False, **kwargs):
        kwargs = dict(dataset=dataset, data_dir=sc_rna_dir, **kwargs)

        if type(gene_indices) is int:
            gene_indices = np.arange(gene_indices, gene_indices + 1)

        kwargs['gene_indices'] = gene_indices

        dataset = VeloDataset(**kwargs)

        return dataset
