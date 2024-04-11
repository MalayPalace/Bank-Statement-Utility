import os

BANK_NAMES = ['HDFC', 'KOTAK', 'SBI', 'BOB', 'IDBI', 'SVC']
ACCOUNT_TYPE = ['Saving', 'Current', 'Creditcard']

COMMA = ","
SPACE = " "
TAB = "\t"
CREDIT_CARD_SUFFIX = "_Creditcard"
APP_CONFIG_PATH = os.path.expanduser("~") + "/.local/share/bank-statement-app/"
# APP_CONFIG_PATH = "./config/" # For local Testing