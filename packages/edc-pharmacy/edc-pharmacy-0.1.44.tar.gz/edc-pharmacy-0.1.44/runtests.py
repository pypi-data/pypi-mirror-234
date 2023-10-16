#!/usr/bin/env python
import logging
from os.path import abspath, dirname

from dateutil.relativedelta import relativedelta
from edc_constants.constants import IGNORE
from edc_test_utils import DefaultTestSettings, func_main
from edc_utils import get_utcnow

app_name = "edc_pharmacy"
base_dir = dirname(abspath(__file__))

project_settings = DefaultTestSettings(
    calling_file=__file__,
    EDC_NAVBAR_VERIFY_ON_LOAD=IGNORE,
    EDC_AUTH_CODENAMES_WARN_ONLY=True,
    EDC_AUTH_SKIP_SITE_AUTHS=True,
    EDC_AUTH_SKIP_AUTH_UPDATER=True,
    BASE_DIR=base_dir,
    APP_NAME=app_name,
    EDC_PROTOCOL_STUDY_OPEN_DATETIME=(
        get_utcnow().replace(microsecond=0, second=0, minute=0, hour=0)
        - relativedelta(years=6)
    ),
    EDC_PROTOCOL_STUDY_CLOSE_DATETIME=(
        get_utcnow().replace(microsecond=999999, second=59, minute=59, hour=11)
        + relativedelta(years=6)
    ),
    add_dashboard_middleware=True,
    add_lab_dashboard_middleware=True,
    excluded_apps=["edc_adverse_event.apps.AppConfig", "adverse_event_app.apps.AppConfig"],
).settings


def main():
    func_main(project_settings, f"{app_name}.tests")


if __name__ == "__main__":
    logging.basicConfig()
    main()
