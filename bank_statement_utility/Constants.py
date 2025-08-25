import os
import platform

from enum import Enum

BANK_NAMES = ['HDFC', 'KOTAK', 'SBI', 'BOB', 'IDBI', 'SVC', 'YES']
ACCOUNT_TYPE = ['Saving', 'Current', 'Creditcard']
EXPORT_TYPE = ['CSV', 'QIF']

COMMA = ","
SPACE = " "
TAB = "\t"
CREDIT_CARD_SUFFIX = "_Creditcard"

####################################
APP_ENV = os.getenv("APP_ENV", "Release").lower()
if APP_ENV == "test":
    # For Local Test run
    print("Running in test environment")
    APP_CONFIG_PATH = "./config/"
    DB_TABLE_NAME = "bank_statement.statement_test"
else:
    # For Release
    print("Running in production environment")
    APP_CONFIG_PATH = os.path.expanduser("~") + "/.local/share/bank-statement-app/"
    if platform.system() == 'Windows':
        APP_CONFIG_PATH = os.path.expanduser("~") + "/AppData/Local/bank-statement-app/"

    DB_TABLE_NAME = "bank_statement.statement"

####################################

class ExportType(Enum):
    CSV = "csv"
    QIF = "qif"


# Other constants can be added here as needed
EMPTY_STRING = ""
