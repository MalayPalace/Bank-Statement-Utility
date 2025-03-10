import os
import platform

from enum import Enum

BANK_NAMES = ['HDFC', 'KOTAK', 'SBI', 'BOB', 'IDBI', 'SVC']
ACCOUNT_TYPE = ['Saving', 'Current', 'Creditcard']
EXPORT_TYPE = ['CSV', 'QIF']

COMMA = ","
SPACE = " "
TAB = "\t"
CREDIT_CARD_SUFFIX = "_Creditcard"

####################################
# For Release
APP_CONFIG_PATH = os.path.expanduser("~") + "/.local/share/bank-statement-app/"
if platform.system() == 'Windows':
    APP_CONFIG_PATH = os.path.expanduser("~") + "/AppData/Local/bank-statement-app/"

DB_TABLE_NAME = "bank_statement.statement"

# For Local Test run
# APP_CONFIG_PATH = "./config/"
# DB_TABLE_NAME = "bank_statement.statement_test"
####################################

class ExportType(Enum):
    CSV = "csv"
    QIF = "qif"