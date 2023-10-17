# Alliance Auth - Hunting Tools

We are hunting Rabbits.

![License](https://img.shields.io/badge/license-MIT-green)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)

![python](https://img.shields.io/badge/python-3.8-informational)
![python](https://img.shields.io/badge/python-3.9-informational)
![python](https://img.shields.io/badge/python-3.10-informational)
![python](https://img.shields.io/badge/python-3.11-informational)

![django-4.0](https://img.shields.io/badge/django-4.0-informational)

## Features

- Display active targets
- Last known Locate and Past Locates for a given target
- Manage target Alts and their capability
- Note taking on given targets

### Planned Features

- Manage Locator Agent Expiries
- Request a Locate from available users
- Generate potential targets from kill activity

## Installation

### Step 1 - Install from pip

```bash
pip install aa-hunting
```

### Step 3 - Configure Auth settings
Configure your Auth settings (`local.py`) as follows:

- Add `'hunting'` to `INSTALLED_APPS`
- Add below lines to your settings file:

```python
## Settings for AA-Hunting
# Notifications (Locator Agent Results)
CELERYBEAT_SCHEDULE['hunting_pull_notifications'] = {
    'task': 'hunting.tasks.pull_notifications',
    'schedule': crontab(minute='0', hour='*'),
}
CELERYBEAT_SCHEDULE['hunting_import_notifications_apps'] = {
    'task': 'hunting.tasks.import_notifications_apps',
    'schedule': crontab(minute='30', hour='*'),
}
# Dont hit squizz too hard, im not shipping the agent file incase it updates
CELERYBEAT_SCHEDULE['hunting_import_agents_squizz'] = {
    'task': 'hunting.tasks.import_agents_squizz',
    'schedule': crontab(minute='0', hour='0', day_of_week='0'),
}
```

### Step 3 - Maintain Alliance Auth

- Run migrations `python manage.py migrate`
- Gather your staticfiles `python manage.py collectstatic`
- Restart your project `supervisorctl restart myauth:`

## Permissions

| Perm | Admin Site  | Perm | Description |
| --- | --- | --- | --- |
| basic_access | nill | Can access the Hunting App | Can access the Hunting App
| target_add | nill | Can add a Hunting target | Can add a Hunting target
| target_edit | nill | Can edit a Hunting target | Can edit a Target, Add Alts, Modify Ship Type
| target_archive | nill | Can archive a Hunting target | Can
| alt_add | nill |
| alt_edit | nill |
| alt_remove | nill |
| locator_addtoken | nill |
| locator_request | nill |
| locator_action | nill |

## Settings

| Name | Description | Default |
| --- | --- | --- |
| `HUNTING_ENABLE_CORPTOOLS_IMPORT`| Enable (if Installed) LocateCharMsg's to be pulled from Corp-Tools, for historical information | `True`

## Contributing

Make sure you have signed the [License Agreement](https://developers.eveonline.com/resource/license-agreement) by logging in at <https://developers.eveonline.com> before submitting any pull requests. All bug fixes or features must not include extra superfluous formatting changes.
