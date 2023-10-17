import os
from pathlib import Path

data_dir = Path(os.getenv('data_dir'))
sc_rna_dir = Path(data_dir) / 'singlecell'
