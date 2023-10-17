# Deep Kernel Latent Force Models

## Installation

### Pip

- `pip install dklfm`

Add a .env file to the root of this project with the data directory `data_dir=<directory>`.

### From source
- Install [poetry](https://python-poetry.org/docs/#installation)
- `cd dklfm`
- `poetry install`

If a cublas error, try:
- `poetry run pip install torch`