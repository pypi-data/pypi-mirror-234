# PyTDI

[![pipeline status](https://gitlab.in2p3.fr/LISA/LDPG/wg6_inrep/pytdi/badges/latest/pipeline.svg)](https://gitlab.in2p3.fr/LISA/LDPG/wg6_inrep/pytdi/-/commits/latest)
[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.6351736.svg)](https://doi.org/10.5281/zenodo.6351736)

PyTDI is a Python package that provides a toolset to perform symbolical and numerical
time-delay interferometry (TDI) calculations. It can be used to define arbitrary linear combination
of time-shifted signals (i.e., combinations), symbolically handle these combinations, and numerically
evaluate these combinations against data.

PyTDI also provides ready-to-use standard TDI combinations for the LISA mission.

* Documentation for the latest stable release is available at <https://lisa.pages.in2p3.fr/LDPG/wg6_inrep/pytdi>
* Documentation for the current development version is available at <https://lisa.pages.in2p3.fr/LDPG/wg6_inrep/pytdi/master>

## Contributing

### Report an issue

We use the issue-tracking management system associated with the project provided by Gitlab. If you want to report a bug or request a feature, open an issue at [https://gitlab.in2p3.fr/LISA/LDPG/wg6_inrep/pytdi/-/issues](https://gitlab.in2p3.fr/LISA/LDPG/wg6_inrep/pytdi/-/issues). You may also thumb-up or comment on existing issues.

### Development environment

We strongly recommend to use [Python virtual environments](https://docs.python.org/3/tutorial/venv.html).

To setup the development environment, use the following commands:

```shell
git clone git@gitlab.in2p3.fr:LISA/LDPG/wg6_inrep/pytdi.git
cd pytdi
python -m venv .
source ./bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Workflow

The project's development workflow is based on the issue-tracking system provided by Gitlab, as well as peer-reviewed merge requests. This ensures high-quality standards.

Issues are solved by creating branches and opening merge requests. Only the assignee of the related issue and merge request can push commits on the branch. Once all the changes have been pushed, the "draft" specifier on the merge request is removed, and the merge request is assigned to a reviewer. They can push new changes to the branch, or request changes to the original author by re-assigning the merge request to them. When the merge request is accepted, the branch is merged onto master, deleted, and the associated issue is closed.

### Pylint and pytest

We enforce [PEP 8 (Style Guide for Python Code)](https://www.python.org/dev/peps/pep-0008/) with [Pylint](http://pylint.pycqa.org/) syntax checking, and testing of the code via unit and integration tests with the [pytest](https://docs.pytest.org/) framework. Both are implemented in the continuous integration system. Only if all tests pass successfully a merge request can be merged.

You can run them locally

```shell
pylint pytdi/*.py
python -m pytest
```

## How to cite

By releasing PyTDI as an open source software package we want to foster open science and enable everyone to use it in their research free of charge. However, please keep in mind that developing and maintaining such a tool takes time and effort. Hence, we would appreciate to be associated with you research:

* Please cite the DOI (see badge above), and acknowledge the authors in any publication that uses PyTDI
* Do not hesitate to send an email for support and/or collaboration

## Contact

* Martin Staab (martin.staab@aei.mpg.de)
* Jean-Baptiste Bayle (j2b.bayle@gmail.com)
