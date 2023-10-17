# Incursions for Alliance Auth

Incursion Tools for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth/).

![License](https://img.shields.io/badge/license-MIT-green)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)

![python](https://img.shields.io/badge/python-3.8-informational)
![python](https://img.shields.io/badge/python-3.9-informational)
![python](https://img.shields.io/badge/python-3.10-informational)
![python](https://img.shields.io/badge/python-3.11-informational)

![django-4.0](https://img.shields.io/badge/django-4.0-informational)

## Features

- AA-Discordbot Cogs for information about active incursions, their status and any set Focus
- Webhook notifications for new incursions and them changing state (Mobilizing/Withdrawing)

## Planned Features

- Waitlist
- AA Fittings Integration
- Secure Groups Integration

## Installation

### Step 1 - Django Eve Universe

Incursions is an App for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth/), Please make sure you have this installed. incursions is not a standalone Django Application

Incursions needs the App [django-eveuniverse](https://gitlab.com/ErikKalkoken/django-eveuniverse) to function. Please make sure it is installed before continuing.

### Step 2 - Install app

```bash
pip install aa-incursions
```

### Step 3 - Configure Auth settings

Configure your Auth settings (`local.py`) as follows:

- Add `'incursions'` to `INSTALLED_APPS`
- Add below lines to your settings file:

```python
## Settings for AA-Incursions ##
# Route is Cached for 300 Seconds, if you aren't riding the Kundalini Manifest to the last minute
# Feel free to adjust this to minute='*/5'
CELERYBEAT_SCHEDULE['incursions_update_incursions'] = {
    'task': 'incursions.tasks.update_incursions',
    'schedule': crontab(minute='*/1', hour='*'),
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
