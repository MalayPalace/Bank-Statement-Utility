import configparser
import sys

from .Constants import APP_CONFIG_PATH
from .config_writer import write_default_config, check_and_update_config_to_latest

# create object
config = configparser.ConfigParser()

# READ CONFIG FILE
try:
    config.read_file(open(APP_CONFIG_PATH + "config.ini"))
    check_and_update_config_to_latest(config)
except IOError:
    write_default_config()
    try:
        config.read_file(open(APP_CONFIG_PATH + "config.ini"))
        check_and_update_config_to_latest(config)
    except IOError:
        sys.exit("Config file not found. Ensure config.ini is placed at path:" + APP_CONFIG_PATH)
