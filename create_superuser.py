"""Create an admin user from environment variables when configured.

Set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL and
DJANGO_SUPERUSER_PASSWORD in the deployment environment. If they are not
set, this script safely skips creation.
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = os.getenv("DJANGO_SUPERUSER_USERNAME")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

if not username or not password:
    print("Superuser not created: set DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD.")
elif User.objects.filter(username=username).exists():
    print(f"Superuser '{username}' already exists.")
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created.")
