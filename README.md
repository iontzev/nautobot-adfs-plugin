# Nautobot Auth Plugin
ADFS Authentification plugin for [Nautobot](https://github.com/nautobot/nautobot). Nautobot v1.0.0+ is required.

### Package Installation from Source Code
The source code is available on GitLab.<br/>
Download and install the package. Assuming you use a Virtual Environment for Nautobot:
```
$ sudo -iu nautobot
$ cd [directory with nautobot-topology-plugin]
$ pip3 install .
```
### Install django-auth-adfs
The source code is available on GitLab.<br/>
Download and install the package. Assuming you use a Virtual Environment for Nautobot:
```
$ sudo -iu nautobot
$ pip3 install django-auth-adfs
```

### Enable the Plugin
In a global Nautobot **nautobot_config.py** configuration file, update or add PLUGINS parameter:
```python
PLUGINS = [
    'nautobot_adfs_plugin',
]
```

Also you need add in **nautobot_config.py** next dircetives:
```python
# AUTH BY ADFS
BANNER_LOGIN = '<a href="/plugins/sso/login" class="btn btn-primary btn-block">Login with SSO [ADFS]</a>'


REMOTE_AUTH_ENABLED = True
REMOTE_AUTH_BACKEND = 'utilities.auth_backends.RemoteUserBackend'
REMOTE_AUTH_CREATE_USER = True

AUTH_ADFS = {
    "SERVER": "fs.hoff.ru",
    "CLIENT_ID": "ADFS_ID_HERE",
    "RELYING_PARTY_ID": "ADFS_ID_HERE",
    "AUDIENCE": "microsoft:identityserver:ADFS_ID_HERE",
    "CLAIM_MAPPING": {"first_name": "given_name",
                      "last_name": "family_name",
                      "email": "email"},
    "USERNAME_CLAIM": "winaccountname",
    "GROUPS_CLAIM": "View_group_only",
}

AUTHENTICATION_BACKENDS = [
    "nautobot.core.authentication.ObjectPermissionBackend",
]

LOGIN_ERROR_REDIRECT_URL = 'https://nautobot.kifr-ru.local/login'
LOGIN_REDIRECT_URL = 'https://nautobot.kifr-ru.local'

```

### Restart Nautobot
Restart the WSGI service to apply changes:
```
sudo systemctl restart nautobot
```

