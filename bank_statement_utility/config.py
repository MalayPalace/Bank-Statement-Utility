import configparser

from .Constants import APP_CONFIG_PATH

# create object
config = configparser.ConfigParser()

# READ CONFIG FILE
config.read(APP_CONFIG_PATH + "config.ini")
