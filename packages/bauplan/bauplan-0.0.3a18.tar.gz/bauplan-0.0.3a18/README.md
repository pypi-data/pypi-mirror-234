# Bauplan CLI

## Requirements

- [direnv](https://direnv.net/)
- [nix](https://nixos.org)
- [devenv](https://devenv.sh/)

## Package publication

### Nathan version

Currently wheel is only supported on OSX with arm64

First compile dependency binaries (the actual CLI)

```bash
$ python build.py
...
```

To build the poetry package:

```bash
$ poetry build
...
```

To publish, first bump the version, then run `publish`

```bash
$ python build.py && poetry -vvv publish -u __token__ -p pypi-blahblahblah --build
...
```

### Big version

Create a `.env` file on the root of the `cli` project (I have a `.env-amarone-dev` file) with:

```bash
POETRY_PYPI_TOKEN_PYPI={{ op://BauplanLabs/pypi - github-all-events-publish-bauplan/credential }}
```

Where:

- `BauplanLabs` is my Vault name
- `pypi - github-all-events-publish-bauplan` is the Key of my `API Credential` item
- `credential` is the field containing the auth token.

To build the poetry package:

```bash
$ make build
```

To publish, first bump the version, then run `publish`

```bash
$ make publish
...
```
