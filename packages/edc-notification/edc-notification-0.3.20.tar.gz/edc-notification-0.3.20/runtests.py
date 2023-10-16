#!/usr/bin/env python
import logging
import sys
from os.path import abspath, dirname, join

import django
from django.conf import settings
from django.test.runner import DiscoverRunner
from edc_constants.constants import IGNORE
from edc_test_utils import DefaultTestSettings

base_dir = dirname(abspath(__file__))
app_name = "edc_notification"

DEFAULT_SETTINGS = DefaultTestSettings(
    calling_file=__file__,
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    ETC_DIR=join(base_dir, app_name, "tests", "etc"),
    EDC_AUTH_CODENAMES_WARN_ONLY=True,
    EDC_NAVBAR_VERIFY_ON_LOAD=IGNORE,
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sites",
        "django_crypto_fields.apps.AppConfig",
        "django_revision.apps.AppConfig",
        "edc_auth.apps.AppConfig",
        "edc_device.apps.AppConfig",
        "edc_export.apps.AppConfig",
        "edc_randomization.apps.AppConfig",
        "edc_dashboard.apps.AppConfig",
        "edc_identifier.apps.AppConfig",
        "edc_sites.apps.AppConfig",
        "edc_protocol.apps.AppConfig",
        "edc_notification.apps.AppConfig",
    ],
    RANDOMIZATION_LIST_PATH=join(base_dir, app_name, "tests", "test_randomization_list.csv"),
    add_dashboard_middleware=True,
    # add_lab_dashboard_middleware=True,
).settings


def main():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    django.setup()
    tags = [t.split("=")[1] for t in sys.argv if t.startswith("--tag")]
    failures = DiscoverRunner(failfast=False, tags=tags).run_tests([f"{app_name}.tests"])
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()
