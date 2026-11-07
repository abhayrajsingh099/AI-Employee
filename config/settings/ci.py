from os import getenv

from .base import *

SECRET_KEY = getenv("SECRET_KEY", "ci-only-secret-key")
DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
