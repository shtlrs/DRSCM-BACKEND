#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import django
from django.core.management import call_command


DEFAULT_ENVS = {
    "DJANGO_SETTINGS_MODULE": "backend.settings",
}


for key, value in DEFAULT_ENVS.items():
    os.environ.setdefault(key, value)


class ApplicationBootstrapper:
    """
    Manages serving of the API & running the necessary migrations.

    Inspired by Python Discord's `SiteManager` class
    https://github.com/python-discord/site/blob/bd1479736ec172752b897ebe0559100e93c996ad/manage.py#L29

    This approach is fairly simple compared to the original one as we only serve with Django's WSGI for now.
    """

    def __init__(self):
        self.verbosity = 1
        self.debug = False

    def apply_migrations(self) -> None:
        """Applies pending migrations"""
        django.setup()

        print("Applying migrations.")

        call_command("makemigrations", verbosity=self.verbosity)
        call_command("migrate", verbosity=self.verbosity)

    def run_server(self) -> None:
        """Runs the server."""

        self.apply_migrations()

        call_command("runserver", "0.0.0.0:8000")


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    if sys.argv[1] == "run":
        bootsrapper = ApplicationBootstrapper()
        bootsrapper.run_server()
        return

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
