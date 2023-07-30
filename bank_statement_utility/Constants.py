import os

bank_names = ['HDFC', 'KOTAK', 'SBI', 'BOB', 'IDBI', 'SVC']
account_type = ['Saving', 'Current', 'Creditcard']

COMMA = ","
SPACE = " "
TAB = "\t"
APP_CONFIG_PATH = os.path.expanduser("~") + "/.local/share/bank-statement-app/"
# APP_CONFIG_PATH = "./config/" # For local Testing