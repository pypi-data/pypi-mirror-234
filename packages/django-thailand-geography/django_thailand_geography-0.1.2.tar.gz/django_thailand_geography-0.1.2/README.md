# django-thailand-geography

[![GitHub](https://img.shields.io/github/license/earthpyy/django-thailand-geography)](https://github.com/earthpyy/django-thailand-geography/blob/main/LICENSE)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/earthpyy/django-thailand-geography/ci.yml?branch=main)](https://github.com/earthpyy/django-thailand-geography/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/earthpyy/django-thailand-geography/branch/main/graph/badge.svg?token=PW280Y917H)](https://codecov.io/gh/earthpyy/django-thailand-geography)
[![PyPI](https://img.shields.io/pypi/v/django-thailand-geography)](https://pypi.org/project/django-thailand-geography/)  
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-thailand-geography)](https://github.com/earthpyy/django-thailand-geography)

Django models for Thailand geography information. This library also includes a command to import geography data from [thailand-geography-data/thailand-geography-json](https://github.com/thailand-geography-data/thailand-geography-json)

## Installation

```bash
pip install django-thailand-geography
```

## Setup

1. Add `thailand_geography` into `INSTALLED_APPS`

   ```python
   # settings.py

   INSTALLED_APPS = [
       ...
       'thailand_geography',
   ]
   ```

1. Run migration

   ```bash
   python manage.py migrate
   ```

1. Import data from JSON database

   ```bash
   python manage.py import_geo
   ```

## Development

### Requirements

- Docker
- Python
- Poetry

### Migrate

```bash
make migrate
```

### Linting

```bash
make lint
```

### Testing

```bash
make test
```

### Fix Formatting

```bash
make yapf
```
