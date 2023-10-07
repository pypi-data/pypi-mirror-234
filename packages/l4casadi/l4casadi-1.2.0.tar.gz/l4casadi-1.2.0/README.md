[![PyPI version](https://badge.fury.io/py/l4casadi.svg)](https://badge.fury.io/py/l4casadi)
![L4CasADi CI](https://github.com/Tim-Salzmann/l4casadi/actions/workflows/ci.yaml/badge.svg)
![Downloads](https://img.shields.io/pypi/dm/l4casadi.svg)

---
# Learning 4 CasADi Framework

L4CasADi enables the use of PyTorch models and functions in a CasADi graph while supporting CasADi code generation 
capabilities. The only requirement on the PyTorch model is to be traceable and differentiable.

[Installation](#installation)\
[Examples](#examples)\
[Real-time L4CasADi](#real-time-l4casadi)

If you use this framework please cite our paper
```
@article{salzmann2023neural,
  title={Real-time Neural-MPC: Deep Learning Model Predictive Control for Quadrotors and Agile Robotic Platforms},
  author={Salzmann, Tim and Kaufmann, Elia and Arrizabalaga, Jon and Pavone, Marco and Scaramuzza, Davide and Ryll, Markus},
  journal={IEEE Robotics and Automation Letters},
  doi={10.1109/LRA.2023.3246839},
  year={2023}
}
```

---
## Installation
### Prerequisites
Independently if you install from source or via pip you will need to meet the following requirements:

- Working build system: CMake compatible C++ compiler.
- PyTorch (`>=2.0`) installation in your python environment.\
`python -c "import torch; print(torch.__version__)"`

### Pip Install
- Ensure all build dependencies are installed
```
setuptools>=68.1
scikit-build>=0.17
cmake>=3.27
ninja>=1.11
torch>=2.0
```

- Run\
`pip install l4casadi --no-build-isolation`

### From Source
- Clone the repository\
`git clone https://github.com/Tim-Salzmann/l4casadi.git`

- All build dependencies installed via\
`pip install -r requirements_build.txt`

- Build from source\
`pip install . --no-build-isolation`

The `--no-build-isolation` flag is required for L4CasADi to find and link against the installed PyTorch.

#### GPU (CUDA)
Install L4CasADi via `CUDACXX=<PATH_TO_nvcc> pip install l4casadi --no-build-isolation` or `CUDACXX=<PATH_TO_nvcc> pip install . --no-build-isolation` to build from source.

---

## Examples
https://github.com/Tim-Salzmann/l4casadi/blob/23e07380e214f70b8932578317aa373d2216b57e/examples/readme.py#L28-L40

Please note that only `casadi.MX` symbolic variables are supported as input.

Multi-input multi-output functions can be realized by concatenating the symbolic inputs when passing to the model and
splitting them inside the PyTorch function.

To use GPU (CUDA) simply pass `device="cuda"` to the `L4CasADi` constructor.

Further examples:
- Simple nonlinear programming with L4CasADi model as objective and constraints: [examples/simple_nlp.py](/examples/simple_nlp.py)
- L4CasADi in pure C(++) projects: [examples/cpp_executable](/examples/cpp_executable)

---

## Batch Dimension

If your PyTorch model expects a batch dimension as first dimension (which most models do) you should pass
`model_expects_batch_dim=True` to the `L4CasADi` constructor. The `MX` input to the L4CasADi component is then expected
to be a vector of shape `[X, 1]`. L4CasADi will add a batch dimension of `1` automatically such that the input to the
underlying PyTorch model is of shape `[1, X]`.

---

## Acados Integration
To use this framework with Acados:
- Follow the [installation instructions](https://docs.acados.org/installation/index.html).
- Install the [Python Interface](https://docs.acados.org/python_interface/index.html).
- Ensure that `LD_LIBRARY_PATH` is set correctly (`DYLD_LIBRARY_PATH`on MacOS).
- Ensure that `ACADOS_SOURCE_DIR` is set correctly.

An example of how a PyTorch model can be used as dynamics model in the Acados framework for Model Predictive Control 
can be found in [examples/acados.py](/examples/acados.py)

To use L4CasADi with Acados you will have to set `model_external_shared_lib_dir` and `model_external_shared_lib_name`
in the `AcadosOcp.solver_options` accordingly.

```
ocp.solver_options.model_external_shared_lib_dir = l4c_model.shared_lib_dir
ocp.solver_options.model_external_shared_lib_name = l4c_model.name
```

https://github.com/Tim-Salzmann/l4casadi/blob/421de6ef408267eed0fd2519248b2152b610d2cc/examples/acados.py#L156-L160

---
## Real-time L4CasADi
Real-time L4Casadi (former [ML-CasADi](https://github.com/TUM-AAS/ml-casadi)) is the underlying framework powering
[Real-time Neural-MPC](https://arxiv.org/pdf/2203.07747). It replaces complex models with local Taylor approximations
to enable real-time optimization procedures. More information [here](l4casadi/realtime).

https://github.com/Tim-Salzmann/l4casadi/blob/62219f61375af4c4133167f1d8b138d90f678c32/l4casadi/realtime/examples/readme.py#L32-L43

---

## Warm Up

Note that PyTorch builds the graph on first execution. Thus, the first call(s) to the CasADi function will be slow.
You can warm up to the execution graph by calling the generated CasADi function one or multiple times before using it.

---

## Roadmap
Further development of this framework will be prioritized by popular demand. If a feature is important to your work
please get in contact or create a pull request.

Possible upcoming features include:
```
- Explicit multi input, multi output functions.
```