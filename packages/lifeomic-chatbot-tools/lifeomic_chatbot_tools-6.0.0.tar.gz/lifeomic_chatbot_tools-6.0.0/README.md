# lifeomic-chatbot-tools

Python utilities for machine learning, web services, and cloud infrastructure.
Includes classes and methods for:

1. ML model serialization/deserialization
2. ML model evaluation utilities
3. Data structures/models related to chatbots
4. ML model artifact persistence and version management
5. And more

The data structures in this package can all be found in the
`lifeomic_chatbot_tools.types` sub-package, and are all
[Pydantic](https://pydantic-docs.helpmanual.io/) data models. For example the
`lifeomic_chatbot_tools.types.agent.AgentConfig` class represents a chatbot's
configuration and training data.

## Getting Started

To begin using the package, use your favorite package manager to install it from PyPi.
For example, using pip:

```
pip install lifeomic-chatbot-tools
```

Some of the features in this repo require more heavy weight dependencies, like AWS
related utilities, or utilities specific to machine learning. If you try to import
those features, they will tell you if you do not have the correct package extra
installed. For example, many of the features in the `lifeomic_chatbot_tools.ml`
sub-package require the `ml` extra. To install `lifeomic-chatbot-tools` with that
extra:

```
pip install lifeomic-chatbot-tools[ml]
```

You can then begin using any package features that require ML dependencies.

## Developing Locally

Before making any new commits or pull requests, please complete these steps.

1. Install the Poetry package manager for Python if you do not already have it.
   Installation instructions can be found
   [here](https://python-poetry.org/docs/#installation).
2. Clone the project.
3. From the root directory of the repo, install the dependencies, including all dev
   dependencies and extras:
   ```
   poetry install --all-extras
   ```

## Testing Locally

With Yarn, Docker, and docker-compose installed, run this command from the project
root:

```
poetry run poe ci
```

This will build the project, lint it, and run the unit tests and integration tests.
All those steps can be run individually as well. See the scripts in the `pyproject.toml`
file for the command names.

### MacOS Users

When developing using MacOS, it is recommended to use a dev container. This project supports
[VS Code dev containers](https://code.visualstudio.com/docs/devcontainers/containers) out of
the box.

## Releasing The Package

Releasing the package is automatically handled by CI, but three steps must be taken
to trigger a successful release:

1. Use Poetry's [`version` command](https://python-poetry.org/docs/cli/#version) to
   bump the package's version.
2. Update the [CHANGELOG](./CHANGELOG.md) file with the latest changes added under the new version.
3. Open a PR. When it's merged to `master`, the release will happen automatically.

CI will then build and release the package to pypi with that version once the PR is
merged to `master`.
