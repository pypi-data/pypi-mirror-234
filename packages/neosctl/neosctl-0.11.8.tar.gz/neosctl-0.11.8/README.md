# Core CLI v0.11.8

## Prerequisites

The following packages are used across python repositories. A global install of them all is _highly_ recommended.

- [Poetry](https://python-poetry.org/docs/#installation)
- [Invoke](https://www.pyinvoke.org/installing.html)
- [Kubefwd](https://kubefwd.com)

A running cluster from [Local
Helm](https://github.com/NEOM-KSA/neos-core-platform/tree/main/demo/helm) with
`gateway` service port forwarded. Details on port forwarding below.

### WSL

If running on Windows, you may need to install `distutils` to install the service.

```bash
$ sudo apt-get install python3.10-distutils
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

## Running locally

### Port forwarding

To access the gateway api locally, you will need to connect to the pod inside
the cluster using `kubefwd`.

```bash
$ sudo kubefwd svc -n core -c ~/.kube/config
```

## Neosctl

When running locally, if you do not manage your own virtual environments, you
can use poetry to put you in a shell with access to the installed code.

```bash
$ poetry shell
```

### Initialize profile

```bash
$ neosctl -p my-profile profile init
Initialising [default] profile.
Gateway API url [http://core-gateway.core-gateway:9000/api/gateway]: <http://gateway_api_url:port>
Registry API url [http://neos-registry.registry:80/api/registry]: <http://registry_api_url:port>
IAM API url [http://core-iam.core-iam:80/api/iam]: <http://iam_api_url:port>
Storage API url [http://core-storage.core-storage:9000/api/storage]: <http://storage_api_url:port>
Username: <username>
```

```bash
$ cat ~/.neosctl
```

To work with the same profile across multiple commands you can export the
profile name as an environment variable.

```bash
$ neosctl -p my-profile product list
...
$ export NEOSCTL_PROFILE=my-profile
$ neosctl product list
```

### Login

```bash
$ neosctl -p=<my-profile> auth login
```

### Commands to work with data products

```bash
$ neosctl --help
$ neosctl product --help
$ neosctl metadata --help
```

To work with the same product across multiple commands you can export the
product name as an environment variable.

```bash
$ neosctl product get my-data-product
...
$ export NEOSCTL_PRODUCT=my-data-product
$ neosctl product get
```

## Generate docs

To generate docs in a markdown format, run the following command.
The output DOCS.md file could be used to update the NEOS documentation site
([docs.neosmesh.com](https://docs.neosmesh.com)).

```bash
pip install typer-cli
typer neosctl.cli utils docs --name neosctl --output DOCS.md
```

## Releases

Release management is handled using `bump2version`. The below commands will tag
a new release. This will also update the helm chart version, this should not be
manually changed.

```bash
$ invoke bump-patch
$ invoke bump-minor
$ invoke bump-major
> vX.Y.Z
```
