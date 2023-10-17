# YAW Dashboards

## Description

> Dashboard for all YAW members to get better insights from real time KPI data. Provides visualizations for personalisation logic in real-time using Python Dash.

## Project structure

```text
YAW-dashboards
    ├── .gitignore
    ├── Makefile
    ├── README.md
    ├── docker
    │   └── Dockerfile
    ├── requirements.txt
    └── src
        ├── assets
        │   └── css
        │       └── layout.css
        ├── config
        │   └── dev.yaml
        ├── config.py
        ├── layout
        │   ├── layout.py
        │   └── navbar.py
        ├── pages
        │   ├── __init__.py
        │   ├── framework_batches.py
        │   └── home.py
        └── run.py
```

## Starting Dashboards

```python
python run.py
```

## Images

```shell
# build image
$ make image

# run the image
$ make run

# push the image
$ make push-image
```
