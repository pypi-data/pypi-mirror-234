# Plant Management System Utils
Fundamental package for the Danone New Zealanda Supply Point Plant Management System.

## Requirements

1. Python 3.7.
2. Flask application context.

## Installation Guide

### Using pip

```
python -m pip install nzsp_pms_utils
```

### Download from last releases

<a href="https://github.com/danone/nzsp.plant-management-system-utils/releases">Releases</a>

## How to use it

### Setting up application before request

```python
    from flask import Flask, g
    ...
    @app.before_request
    def set_service_name_globally():
        g.service_name = SERVICE_NAME
```

### Calling it in a blueprint

```python
    from nzsp_pms_utils.middleware import verify_authorization
    ...
    bp.before_request(verify_authorization)
```

## Testing results

```
python -m unittest discover .
```