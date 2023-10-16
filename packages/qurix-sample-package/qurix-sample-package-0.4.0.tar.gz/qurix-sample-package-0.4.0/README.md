# Python package template

Template for Python packages for qurix Technology.

## Structure

A normal Python package will start with the namespace `qurix` as in this sample package. A sample structure is as follows:

```text
.
├── LICENCE
├── Makefile
├── README.md
├── qurix
│   └── <domain>
│       └── <module-organization-level>
│           ├── __init__.py
│           ├── __version__.py
│           └── <module>
├── requirements.txt
├── setup.py
└── tests
    ├── __init__.py
    └── test_module.py
```

## Versioning and release

Package versions will be identified according to [semantic versioning](https://semver.org/lang/en). The release process will deploy in both [Test PyPI](https://test.pypi.org/) and [PyPI](https://pypi.org/).

```mermaid
%%{init: { 'logLevel': 'debug', 'theme': 'base', 'gitGraph': {'rotateCommitLabel': true}} }%%
gitGraph
    commit
    branch staging
    branch feat/some-feature
    checkout feat/some-feature
    commit
    commit
    checkout staging
    merge feat/some-feature id: "Rel. Test PyPI 0" tag: "v0.1.0rc0"
    checkout main
    merge staging id: "Rel. PyPI 0" tag: "v0.1.0"
    branch fix/some-fix
    checkout fix/some-fix
    commit
    checkout staging
    merge fix/some-fix id: "Rel. Test PyPI 1" tag: "v0.1.1rc0"
    checkout main
    merge staging id: "Rel. PyPI 1" tag: "v0.1.1"
```

## Deployment

Automatic deployments via Github Actions. See `.github/worfklows/`