import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

data_dir = Path(os.getenv('data_dir'))
sc_rna_dir = Path(data_dir) / 'singlecell'
