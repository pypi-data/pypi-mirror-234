# Drifters for Alliance Auth

Drifter wormhole tracker/manager plugin for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth/).

![License](https://img.shields.io/badge/license-MIT-green)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)

![python](https://img.shields.io/badge/python-3.8-informational)
![python](https://img.shields.io/badge/python-3.9-informational)
![python](https://img.shields.io/badge/python-3.10-informational)
![python](https://img.shields.io/badge/python-3.11-informational)

![django-4.0](https://img.shields.io/badge/django-4.0-informational)

## Features

- AA-Discordbot Cogs for recording the status of Jove Observatory systems and their contained Drifter holes
- Cogs for recalling this information in a few ways

## Planned Features

- P2P Mapping using known holes
- Possible Pathfinder Integration/sync? To investigate usefullness

## Installation

### Step 1 - Django Eve Universe

Drifters is an App for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth/), Please make sure you have this installed. Drifters is not a standalone Django Application

Drifters needs the App [django-eveuniverse](https://gitlab.com/ErikKalkoken/django-eveuniverse) to function. Please make sure it is installed before continuing.

### Step 2 - Install app

```bash
pip install aa-drifters
```

### Step 3 - Configure Auth settings

Configure your Auth settings (`local.py`) as follows:

- Add `'drifters'` to `INSTALLED_APPS`
- Add below lines to your settings file:

```python
## Settings for AA-Drifters
# Cleanup Task
CELERYBEAT_SCHEDULE['drifters_garbage_collection'] = {
    'task': 'drifters.tasks.garbage_collection',
    'schedule': crontab(minute=0, hour='*'),
}
```

### Step 4 - Maintain Alliance Auth

- Run migrations `python manage.py migrate`
- Gather your staticfiles `python manage.py collectstatic`
- Restart your project `supervisorctl restart myauth:`

### Step 5 - Pre-Load Django-EveUniverse

- `python manage.py eveuniverse_load_data map` This will load Regions, Constellations and Solar Systems

## Contributing

Make sure you have signed the [License Agreement](https://developers.eveonline.com/resource/license-agreement) by logging in at <https://developers.eveonline.com> before submitting any pull requests. All bug fixes or features must not include extra superfluous formatting changes.
