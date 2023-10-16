### Installation
```bash
$ pip install pylint-django-settings
```

### Examples
`.pylintrc`
```
[MASTER]
load-plugins=pylint_django
django-settings-module=pylint_django_settings
```

```bash
$ pylint django-settings-module=pylint_django_settings
```

