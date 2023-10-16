# NEOS Platform Common Code v0.10.23

## Prerequisites

The following packages are used across python repositories. A global install of them all is *highly* recommended.

* [Poetry](https://python-poetry.org/docs/#installation)
* [Invoke](https://www.pyinvoke.org/installing.html)

### WSL

If running on Windows, you may need to install `distutils` to install the service.

```bash
$ sudo apt-get install python3.8-distutils
```

## Initial setup

```bash
$ invoke install-dev
```

## Code Quality

### Tests

```bash
invoke tests
invoke tests-coverage
```

## Linting

```bash
invoke check-style
invoke isort
```

## Releases

Release management is handled using `bump2version`. The below commands will tag
a new release. Jenkins will then publish the release to the artifact repository.

```bash
$ invoke bump-patch
$ invoke bump-minor
$ invoke bump-major
> vX.Y.Z
```
