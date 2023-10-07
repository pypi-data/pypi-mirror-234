# Kognic IO Client

Python 3 library providing access to Kognic IO. This package is public and available on [PyPi](https://pypi.org/project/kognic-io/).

Note that any changes to the examples are automatically pushed [kognic-io-python-examples](https://github.com/annotell/kognic-io-examples-python/tree/master), which is a **public** repository.
This is where the examples in the documentation are taken from.

## Installation

To install the latest public version, run `pip install kognic-io`.

For local development it is recommended to install locally with `pip install -e .` in the root folder.

## Documentation

The public documentation is hosted by the [public-docs](https://github.com/annotell/public-docs) repository and publicly available [here](https://developers.kognic.com/).

## Testing

Testing can be done either against `development` (local environment) or `staging`. The default is `development` and can 
be changed by setting the `--env` flag to `staging` in the following way

```bash
pytest --env=staging ./tests
```

Note that `KOGNIC_CREDENTIALS` needs to be set to a valid credentials file for the environment you are testing against.

Many of the tests are integration tests and require a valid credentials file. If you want to skip the integration tests
you can run 
```bash
pytest -m 'not integration' ./tests
```

## Releasing

Releasing new versions of the package is done by creating a git tag. This will trigger a GitHub action that will build
and publish the package to PyPi. The version number is determined by the git tag, so make sure to use the correct format
when creating a new tag. The format is `vX.Y.Z` where `X`, `Y` and `Z` are integers. To create a new tag and push it to
the remote repository, run the following commands

```bash
git tag vX.Y.Z; git push origin vX.Y.Z
```

**Important:** Don't forget to update the changelog with the new version number and a description of the changes before
releasing a new version. The changelog is located in the root folder and is named `CHANGELOG.md`.
