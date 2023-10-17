# AA "Top"
System Utilization and AA Statistics plugin for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth/).

Inspired by https://zkillboard.com/ztop/ by Squizz Caphinator

![License](https://img.shields.io/badge/license-MIT-green)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)

![python](https://img.shields.io/badge/python-3.8-informational)
![python](https://img.shields.io/badge/python-3.9-informational)
![python](https://img.shields.io/badge/python-3.10-informational)

![django-4.0](https://img.shields.io/badge/django-4.0-informational)

## Features

## Planned Features

# Installation
## Step 2 - Install app
```bash
pip install aa-top
```

## Step 3 - Configure Auth settings
Configure your Auth settings (`local.py`) as follows:

- Add `'top'` to `INSTALLED_APPS`
- Add below lines to your settings file:

```python
## Settings for AA-Top
# Update aatop.txt
CELERYBEAT_SCHEDULE['top_update_aa_top_txt'] = {
    'task': 'top.tasks.update_aa_top_txt',
    'schedule': crontab(minute='*'),
}
```

## Step 4 - Maintain Alliance Auth
- Run migrations `python manage.py migrate`
- Gather your staticfiles `python manage.py collectstatic`
- Restart your project `supervisorctl restart myauth:`

# Permissions
| Perm | Admin Site	 | Perm | Description |
| --- | --- | --- | --- |
| basic_access | nill | Can access the web view for this app

# Settings
| Name | Description | Default |
| --- | --- | --- |

## Contributing
Make sure you have signed the [License Agreement](https://developers.eveonline.com/resource/license-agreement) by logging in at <https://developers.eveonline.com> before submitting any pull requests. All bug fixes or features must not include extra superfluous formatting changes.
