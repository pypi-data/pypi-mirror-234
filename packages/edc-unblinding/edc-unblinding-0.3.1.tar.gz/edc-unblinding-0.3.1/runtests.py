#!/usr/bin/env python
import logging
import os
import sys
from os.path import abspath, dirname

import django
from django.conf import settings
from django.test.runner import DiscoverRunner
from edc_constants.constants import IGNORE
from edc_test_utils import DefaultTestSettings

app_name = "edc_unblinding"
base_dir = dirname(abspath(__file__))

DEFAULT_SETTINGS = DefaultTestSettings(
    calling_file=__file__,
    template_dirs=[os.path.join(base_dir, app_name, "tests", "templates")],
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    ETC_DIR=os.path.join(base_dir, app_name, "tests", "etc"),
    EDC_AUTH_CODENAMES_WARN_ONLY=True,
    EDC_NAVBAR_VERIFY_ON_LOAD=IGNORE,
    SUBJECT_SCREENING_MODEL="visit_schedule_app.subjectscreening",
    SUBJECT_CONSENT_MODEL="visit_schedule_app.subjectconsent",
    SUBJECT_VISIT_MODEL="edc_visit_tracking.subjectvisit",
    SUBJECT_VISIT_MISSED_MODEL="visit_schedule_app.subjectvisitmissed",
    SUBJECT_REQUISITION_MODEL="visit_schedule_app.subjectrequisition",
    EXTRA_INSTALLED_APPS=["visit_schedule_app.apps.AppConfig"],
    # INSTALLED_APPS=[
    #     "django.contrib.admin",
    #     "django.contrib.auth",
    #     "django.contrib.contenttypes",
    #     "django.contrib.sessions",
    #     "django.contrib.messages",
    #     "django.contrib.staticfiles",
    #     "django.contrib.sites",
    #     "simple_history",
    #     "django_crypto_fields.apps.AppConfig",
    #     "edc_appointment.apps.AppConfig",
    #     "edc_crf.apps.AppConfig",
    #     "edc_action_item.apps.AppConfig",
    #     "edc_adverse_event.apps.AppConfig",
    #     "adverse_event_app.apps.AppConfig",
    #     "edc_dashboard.apps.AppConfig",
    #     "edc_consent.apps.AppConfig",
    #     "edc_facility.apps.AppConfig",
    #     "edc_metadata.apps.AppConfig",
    #     "edc_notification.apps.AppConfig",
    #     "edc_device.apps.AppConfig",
    #     "edc_identifier.apps.AppConfig",
    #     "edc_registration.apps.AppConfig",
    #     "edc_sites.apps.AppConfig",
    #     "edc_timepoint.apps.AppConfig",
    #     "edc_visit_schedule.apps.AppConfig",
    #     "visit_schedule_app.apps.AppConfig",
    #     "edc_unblinding.apps.AppConfig",
    #     "edc_auth.apps.AppConfig",
    # ],
    DASHBOARD_BASE_TEMPLATES={
        "dashboard_template": os.path.join(
            base_dir, "edc_unblinding", "tests", "templates", "dashboard.html"
        ),
        "dashboard2_template": os.path.join(
            base_dir, "edc_unblinding", "tests", "templates", "dashboard2.html"
        ),
    },
    EDC_SITES_DEFAULT_COUNTRY="tanzania",
    use_test_urls=True,
    add_dashboard_middleware=True,
    add_lab_dashboard_middleware=True,
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
