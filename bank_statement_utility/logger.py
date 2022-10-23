import logging

#### logging configs #######
log_file_name = "bank-statement-app.log"
log_console_level = logging.INFO
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
