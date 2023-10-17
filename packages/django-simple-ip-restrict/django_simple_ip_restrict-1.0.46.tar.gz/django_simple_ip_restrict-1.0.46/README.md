# django-simple-ip-restrict

This middleware allows you to mark Django URL namespaces as unavailable to all
requests except those coming from a whitelisted IP subnet.


## Instructions

Add to the list of MIDDLEWARE:

    "django_simple_ip_restrict.middleware.ip_filter",

Then you can set the following keys on settings.py:

  - IP_PROTECTED_NAMESPACES: list of namespaces to block (default: ["admin"])
  - IP_NETWORKS_WHITELIST: list of subnets to allow, in CIDR notation

## Manual deployment
Since we don't have a CI/CD pipeline set up right now. You'll have to follow the following steps to release

1. Do your changes
2. Install `bumpversion` and `twine`
```
pip install twine bumpversion
```
3. Bump the version using `bumpversion`
```
bumpversion patch
```
4. A commit should be made automatically, just push
```
git push
```
5. Build using setup.py
```
python setup.py sdist
```
6. Push to pypi using twine
```
twine upload dist/*
```
Use `1password` to find the credentials for pypi.

In order to upload, we have 2FA and the following needs to be done:
- username should be "\_\_token__"
- password should be the Access Token value