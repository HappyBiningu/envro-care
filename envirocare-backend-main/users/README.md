# User Guide

1. **Copy the code onto the project root directory to a folder named "users". Make sure no other app is named "users" as well.**

2. **Enter the following configureations in your settings.py file**

- _Register the application_

```python
"users.apps.UsersConfig",
```

- _Include the CustomUser model as the default AUTH_USER_MODEL_

```python
AUTH_USER_MODEL = "users.CustomUser"
```

- _Add the following REST_FRAMEWORK configs_

```python
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        # 'rest_framework.permissions.IsAuthenticated',
        "rest_framework.permissions.AllowAny",
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'users.services.authentication.CustomAuthentication',
    ),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.AnonRateThrottle","rest_framework.throttling.UserRateThrottle",],
    "DEFAULT_THROTTLE_RATES": {"anon": "100000/hour", "user": "1000000/day"},
}
```

- _Configure properties of SIMPLE_JWT cookies_

```python
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_COOKIE": "access_token",
    "AUTH_COOKIE_DOMAIN": None,
    "AUTH_COOKIE_SECURE": False,
    "AUTH_COOKIE_HTTP_ONLY": True,
    "AUTH_COOKIE_PATH": "/",
    "AUTH_COOKIE_SAMESITE": "Lax",
}

SESSION_COOKIE_AGE=60*60*48 # Session/Cookie age in seconds. Ideally should be 2 days old
```

- _Include the users app urls in the base urls file_

```python
path('api/v1/', include("users.urls")),
```

- _Run migrations_

```bash
python3 manage.py migrate
```
