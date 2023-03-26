import logging
import os

from .Constants import APP_CONFIG_PATH


def check_or_create_base_app_path(app_base_path: str):
    if not os.path.exists(app_base_path):
        print("Creating App directory: " + app_base_path)
        os.makedirs(app_base_path)
    return app_base_path


# logging configs #######
log_path = check_or_create_base_app_path(APP_CONFIG_PATH + "Log/")
log_file_name = log_path + "bank-statement-app.log"
log_console_level = logging.CRITICAL
log_file_level = logging.DEBUG
log_format = "%(levelname)s [%(asctime)s] {%(filename)s:%(lineno)d} - %(message)s"

# set up logging to file
logging.basicConfig(
    filename=log_file_name,
    level=log_file_level,
    format=log_format
)

# set up logging to console
console = logging.StreamHandler()
console.setLevel(log_console_level)
formatter = logging.Formatter(log_format)
console.setFormatter(formatter)

# add the handler to the root logger
logging.getLogger().addHandler(console)

log = logging.getLogger(__name__)
