# Setup

## Creating a virtual environment

A virtual environment should be created and activated before installation of requirements

```
python/python3 -m venv mind_map_venv
source mind_map_venv/bin/activate
```

Based on the preference, a `conda` environment could also be used.

---
## Installation of requirements

All the necessary python libraries can be installed using `pip` or `conda` inside the project folder.

```
pip install -r requirements.txt -q
```

---
## Start the server

The django server can then be started using the following inside the project folder.

```
python manage.py runserver
```