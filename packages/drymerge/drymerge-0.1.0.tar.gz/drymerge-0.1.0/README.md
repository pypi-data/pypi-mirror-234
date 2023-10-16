# DryMerge Client SDK

## Description

Use this to poll the DryMerge backend for jobs.

## Installation

Install the package from PyPI:

```bash
pip install your_package_name
```

## Usage

Here's a simple example to get you started:

```python
from drymerge import DryClient

client = (DryClient(
    api_key="YOUR_API_KEY_HERE",
    verbose=True, )
    .route("print_with_reflect", lambda request: {'test': 'test'})
    .route("py2", lambda request: {'test2': 'test2'})
)

client.start()
```

## Dependencies

This package requires Python 3.3 or higher. Additional dependencies like `requests` will be installed automatically during the package installation.
