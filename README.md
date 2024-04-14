# Neurons for infant social bonding in the mouse zona incerta

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10962543.svg)](https://doi.org/10.5281/zenodo.10962543)

## Authors
Yuexuan Li<sup>1,2</sup>, Gustavo Santana<sup>1,3</sup>, Zhong-Wu Liu<sup>2</sup>, Xiao-Bing Gao<sup>2</sup>, Marcelo O.Dietrich<sup>*1,2,3</sup>

<br>

<sup>1</sup>Laboratory of Physiology of Behavior, Department of Comparative Medicine, School of Medicine, Yale University; New Haven, 06520, United States of America<br>
<sup>2</sup>Department of Comparative Medicine, School of Medicine, Yale University; New Haven, 06520, United States of America<br>
<sup>3</sup>Department of Neuroscience, School of Medicine, Yale University; New Haven, 06520, United States of America<br>
<sup>4</sup>
<sup>5</sup>


*Corresponding Author 

<br><br>

# Overview

Analysis is done using Jupyter notebooks. You will need to have Jupyter or Jupyterlab installed on your machine. 

<br><br>

# Installation

Installation instructions

1. Install Miniconda on your machine https://docs.anaconda.com/free/miniconda/. On Mac you can use these commands in the terminal.

               mkdir -p ~/miniconda3
               curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
               bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
               rm -rf ~/miniconda3/miniconda.sh

3. Install jupyterlab in the base environment with `nb_conda_kernel`

		conda install jupyter
		
4. Once Miniconda is installed create the environment used for nearly all notebooks in this repository by running from the command line.

		conda create -n env python=3.10
		conda activate env
5. Install the library needed to run the code by running `pip install -e .` while in the `env` environment.


<br><br>

# Data

1. Demo data provided in the notebook folder.
2. Download data from Zenodo [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10962543.svg)](https://doi.org/10.5281/zenodo.10962543).

<br><br>

# Notebooks

1. For each notebook, first update file path to data.
2. Next, check the versions of packages for reproductivity before running notebooks.

<br><br><br>
