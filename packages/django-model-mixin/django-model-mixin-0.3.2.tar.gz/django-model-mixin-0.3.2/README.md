# django-model-mixin [![PyPi license](https://img.shields.io/pypi/l/django-model-mixin.svg)](https://pypi.python.org/pypi/django-model-mixin)

[![PyPi status](https://img.shields.io/pypi/status/django-model-mixin.svg)](https://pypi.python.org/pypi/django-model-mixin)
[![PyPi version](https://img.shields.io/pypi/v/django-model-mixin.svg)](https://pypi.python.org/pypi/django-model-mixin)
[![PyPi python version](https://img.shields.io/pypi/pyversions/django-model-mixin.svg)](https://pypi.python.org/pypi/django-model-mixin)
[![PyPi downloads](https://img.shields.io/pypi/dm/django-model-mixin.svg)](https://pypi.python.org/pypi/django-model-mixin)
[![PyPi downloads](https://img.shields.io/pypi/dw/django-model-mixin.svg)](https://pypi.python.org/pypi/django-model-mixin)
[![PyPi downloads](https://img.shields.io/pypi/dd/django-model-mixin.svg)](https://pypi.python.org/pypi/django-model-mixin)

## GitHub ![GitHub release](https://img.shields.io/github/tag/DLRSP/django-model-mixin.svg) ![GitHub release](https://img.shields.io/github/release/DLRSP/django-model-mixin.svg)

## Test [![codecov.io](https://codecov.io/github/DLRSP/django-model-mixin/coverage.svg?branch=main)](https://codecov.io/github/DLRSP/django-model-mixin?branch=main) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DLRSP/django-model-mixin/main.svg)](https://results.pre-commit.ci/latest/github/DLRSP/django-model-mixin/main) [![gitthub.com](https://github.com/DLRSP/django-model-mixin/actions/workflows/ci.yaml/badge.svg)](https://github.com/DLRSP/django-model-mixin/actions/workflows/ci.yaml)

## Check Demo Project
* Check the demo repo on [GitHub](https://github.com/DLRSP/example/tree/django-model-mixin)

## Requirements
-   Python 3.8+ supported.
-   Django 3.2+ supported.

## Setup
1. Install from **pip**:
```shell
pip install django-model-mixin
```

2. Modify `settings.py` by adding the app to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ...
    "model_mixin",
    # ...
]
```

3. Modify your project `models.py` with needed imports and class extends:
```python
# ...other imports...
from model_mixin.models import AuditModelMixin, PublishModelMixin

class MyCustomClass(AuditModelMixin, PublishModelMixin):
    # ...
```

4. Execute Django's command `makemigrations` inside your project's root:
```shell
python manage.py makemigrations
```

5. Finally, execute Django's command `migrate` inside your project's root:
```shell
python manage.py migrate
```

## Run Example Project

```shell
git clone --depth=50 --branch=django-model-mixin https://github.com/DLRSP/example.git DLRSP/example
cd DLRSP/example
python manage.py runserver
```

Now browser the app @ http://127.0.0.1:8000
