# AutoML Native Client README

This repository contains the AutoML Native Client which can be used to train models with AutoML without dependencies on Azure.

## Content

- [Installation](#installation)
- [Notebook setup](#notebook-setup)
- [Usage](#usage)

## Installation

Start by installing [Anaconda](https://www.anaconda.com/download/) or [Miniconda](https://conda.io/miniconda.html). Miniconda is recommended if you don't know which one to use. Make sure to get the Python 3.x version.

Once this is completed, open a new Anaconda Prompt window if on Windows, or a new terminal window on MacOS/Linux, then run the following set of commands:

```
conda create -n myenv
conda activate myenv
conda install Cython numpy tensorflow
pip install --upgrade automl_client_core_nativeclient --extra-index-url https://automlpkgtestpypi.azureedge.net/pkg-release/master --extra-index-url https://azuremlsdktestpypi.azureedge.net/sdk-release/master/588E708E0DF342C4A80BD954289657CF
```

Note that we recommend pinning the version number of the native client if you plan to use it outside of development. This can be done by specifying which version of the package to install with pip, like so:

```
pip install --upgrade automl_client_core_nativeclient==0.1.288 --extra-index-url https://automlpkgtestpypi.azureedge.net/pkg-release/master --extra-index-url https://azuremlsdktestpypi.azureedge.net/sdk-release/master/588E708E0DF342C4A80BD954289657CF
```

This readme may not always specify the latest known stable version, so if in doubt, contact erah.

## Notebook setup

If you wish to run AutoML with Jupyter notebooks, run the following commands inside your environment (substituting **myenv** with your environment name):

```
pip install jupyter ipykernel
python -m ipykernel install --user --name myenv --display-name "Python (myenv)"
```

Once that is complete, you can run Jupyter from within your environment with the following commands:
```
cd path/to/notebooks
jupyter notebook
```

## Usage

Sample notebooks are provided alongside this README which describe how to use the Native Client.

Native Client requires authentication in order to fetch new pipeline recommendations - you will need to create an AAD application and provide us with the tenant and application ID so we can whitelist it on our side. Creating the AAD application is out of the scope of this document, but you can refer to [this page](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal) for instructions on how to set this up. You can choose to just plug in a static service principal key in the example notebooks or provide your own implementation to fetch an AAD access token.
