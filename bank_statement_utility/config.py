import configparser
import sys

from .Constants import APP_CONFIG_PATH
from .config_writer import write_default_config

# create object
config = configparser.ConfigParser()

# READ CONFIG FILE
try:
    config.read_file(open(APP_CONFIG_PATH + "config.ini"))
except IOError:
    write_default_config()
    try:
        config.read_file(open(APP_CONFIG_PATH + "config.ini"))
    except IOError:
        sys.exit("Config file not found. Ensure config.ini is placed at path:" + APP_CONFIG_PATH)
