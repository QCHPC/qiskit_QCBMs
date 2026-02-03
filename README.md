<!-- SHIELDS -->
<div align="left">

  ![Platform](https://img.shields.io/badge/%F0%9F%92%BB%20Platform-Linux%20%7C%20macOS%20%7C%20Windows-informational)
  [![Qiskit](https://img.shields.io/badge/Qiskit%20-%20%3E%3D1.1%20-%20%236133BD?logo=Qiskit)](https://github.com/Qiskit/qiskit)
  [![License](https://img.shields.io/github/license/Qiskit/qiskit-addon-cutting?label=License)](LICENSE.txt)

# Qiskit-QCBMs
## Quantum Circuit Born Machines in Qiskit. 

### Table of Contents

* [About](#about)
* [Documentation](#documentation)
* [Installation](#installation)
* [Deprecation Policy](#deprecation-policy)
* [References](#references)
* [License](#license)

----------------------------------------------------------------------------------------------------

### About

Quantum Circuit Born Machines are generative models that use quantum circuits to represent probability distributions. The expressive power of these models makes them a good candidate for tackling difficult unsupervised generative modeling tasks. Also, because of their relatively simple architecture, Quantum Circuit Born Machines are a great testbed for nearterm devices. 

----------------------------------------------------------------------------------------------------
  
### Documentation

All documentation is available at https://qiskit-qcbms.readthedocs.io/en/latest/#.

----------------------------------------------------------------------------------------------------
  
### Installation
This package is in its earliest of stages and is still very much under development.  

You can `git clone` the repo, and from the main directory, `pip install .` the code into your environment.

It will appear on `pip list` as: `qiskit-addon-qcbm`.

We encourage installing this package via ``pip``, when possible.

```bash
pip install .
```
----------------------------------------------------------------------------------------------------

### Deprecation Policy

We follow [semantic versioning](https://semver.org/) and are guided by the principles in [Qiskit's deprecation policy](https://github.com/Qiskit/qiskit/blob/main/DEPRECATION.md).  We may occasionally make breaking changes in order to improve the user experience.  When possible, we will keep old interfaces and mark them as deprecated, as long as they can co-exist with the new ones.  Each substantial improvement, breaking change, or deprecation will be documented.

----------------------------------------------------------------------------------------------------

### References

[1] Liu, Jin-Guo and Wang, Lei, [Differentiable learning of quantum circuit Born machines](https://journals.aps.org/pra/pdf/10.1103/PhysRevA.98.062324), Phys. Rev. A, vol 8, issue 6, 2018.
  
----------------------------------------------------------------------------------------------------

<!-- LICENSE -->
### License
[Apache License 2.0](LICENSE.txt)
