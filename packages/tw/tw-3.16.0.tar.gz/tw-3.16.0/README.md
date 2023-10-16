
# TensorWrapper
TensorWrapper is a extension library for PyTorch framework. It aims to supplement a few of common components: newest optimizer, opeartors, utils, drawer, common structure and etc.

## Installation
```bash
# create conda environment - based python3.8
conda env create -f environment.yml
conda activate tw


# install torch version respect to cuda version
pip install -r requirements/cu116.txt

# pytorch 1.10 above require gcc 7.0 above version
conda install gxx_linux-64=7.5.0 gcc_linux-64=7.5.0
conda install -c anaconda cmake
make ops

python setup.py develop

```
