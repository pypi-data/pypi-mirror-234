# Argus Enterprise API

[![Build and Test](https://github.com/budaesandrei/argus-enterprise-api/actions/workflows/ci_cd_pipeline.yml/badge.svg)](https://github.com/budaesandrei/argus-enterprise-api/actions/workflows/ci_cd_pipeline.yml)
[![codecov](https://codecov.io/gh/budaesandrei/argus-enterprise-api/graph/badge.svg?token=2W281SPKSE)](https://codecov.io/gh/budaesandrei/argus-enterprise-api)
[![PyPi](https://img.shields.io/pypi/v/argus-enterprise-api.svg)](https://pypi.python.org/pypi/argus-enterprise-api/)
[![License MIT](https://img.shields.io/:license-MIT-blue.svg)](LICENSE)
[![Codestyle Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub Downloads](https://img.shields.io/github/downloads/budaesandrei/argus-enterprise-api/total.svg?label=GitHub%20Downloads)]()
[![PyPI Downloads](https://img.shields.io/pypi/dm/argus-enterprise-api?label=PyPI%20Downloads)]()

## Overview

This Python package is a convenient wrapper for interacting with the Argus API by [Altus Group](https://www.altusgroup.com/). The package dynamically generates Python classes and methods based on the API's Swagger specification, offering an intuitive way to interact with various Argus services like Workspace, ModelManagement, and more.

### Features

- Dynamically generated API methods
- Automatic API version handling
- Comprehensive documentation
- Easy-to-use Pythonic interfaces

## Installation

To install the package, run:

```
pip install argus-enterprise-api
```

## Quick Start

```python
from argus_enterprise_api import ArgusClient

# Initialize the client
client_key = "your_key"
client_secret = "your_secret"
cert_path = "your_cert_path"
cert_pwd = "your_cert_password"
email = "your_email_granted_to_argus_api"
env_id = "your_environment_id"

client = ArgusClient(
    client_key=client_key,
    client_secret=client_secret,
    cert_path=cert_path,
    cert_pwd=cert_pwd,
    email=email,
    env_id=env_id
)

# Use the Workspace API
workspace_instance = client.workspace
workspace_instance.some_method()

# Use the ModelManagement API
model_mgmt_instance = client.model_management
model_mgmt_instance.some_other_method()
```

## Documentation

Each dynamically generated class comes with comprehensive documentation. You can refer to the documentation for each class like so:

```python
print(ArgusClient.__doc__)
print(workspace_instance.some_method.__doc__)
print(model_mgmt_instance.some_method.__doc__)
```

For more technical details, refer to [Argus API Documentation](https://cloud.altusplatform.com/help/index.htm).

## Testing

To run the test suite:

```
pytest tests/
```

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
