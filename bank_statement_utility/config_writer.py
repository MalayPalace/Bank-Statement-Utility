# python 3.x
from configparser import ConfigParser

from .Constants import APP_CONFIG_PATH
from .version import __version_1_2_1__, __version_2_0_0__, __version_2_0_1__, __version_2_1_0__

config = ConfigParser()


def version_compare(v1, v2):
    """
    Method to compare two versions.
    Return 1 if v2 is smaller, -1 if v1 is smaller,
    0 if equal
    :param v1:
    :param v2:
    :return: int
    """
    arr1 = v1.split(".")
    arr2 = v2.split(".")
    n = len(arr1)
    m = len(arr2)

    # converts to integer from string
    arr1 = [int(i) for i in arr1]
    arr2 = [int(i) for i in arr2]

    # compares which list is bigger and fills
    # smaller list with zero (for unequal delimiters)
    if n > m:
        for i in range(m, n):
            arr2.append(0)
    elif m > n:
        for i in range(n, m):
            arr1.append(0)

    # returns 1 if version 1 is bigger and -1 if
    # version 2 is bigger and 0 if equal
    for i in range(len(arr1)):
        if arr1[i] > arr2[i]:
            return 1
        elif arr2[i] > arr1[i]:
            return -1
    return 0


def check_and_update_config_to_latest(config_file):
    """
    Apply incremental changes to config file so to update to latest version
    :param config_file:
    :return: NaN
    """
    if version_compare(config_file['Basic']['version'], __version_2_0_0__) == -1:
        __update_to_2_0_0()
    if version_compare(config_file['Basic']['version'], __version_2_0_1__) == -1:
        __update_to_2_0_1()
    if version_compare(config_file['Basic']['version'], __version_2_1_0__) <= 0:
        __update_to_2_1_0()


def write_default_config():
    config.read(APP_CONFIG_PATH + 'config.ini')

    config.add_section('Basic')
    config.set('Basic', 'version', __version_1_2_1__)
    config.set('Basic', 'appname', 'Bank Statement Utility')

    config.add_section('Cass')
    config.set('Cass', 'contact.points', '127.0.0.1')
    config.set('Cass', 'port', '9042')
    config.set('Cass', 'username', '')
    config.set('Cass', 'password', '')

    config.add_section('KOTAK')
    config.set('KOTAK', 'record_starts_with', 'Sl. No.')
    config.set('KOTAK', 'record_ends_with', 'Opening balance')
    config.set('KOTAK', 'skip_data_column_no', '9')

    config.add_section('KOTAK_Creditcard')
    config.set('KOTAK_Creditcard', 'record_selector_regex',
               '^(\\d{2}\\/\\d{2}\\/\\d{4}) (.*) ([0-9,]+[.][0-9]{2}( Cr){0,1})')
    config.set('KOTAK_Creditcard', 'data_headers', 'Date,Transaction Details,Amount')

    config.add_section('SBI')
    config.set('SBI', 'record_starts_with', 'Txn Date')

    config.add_section('SBI_Creditcard')
    config.set('SBI_Creditcard', 'record_selector_regex',
               '^(\\d{2} [A-Z][a-z][a-z] \\d{2}) (.*) ([0-9,]+[.][0-9]{2} [DCM])')
    config.set('SBI_Creditcard', 'data_headers', 'Date,Transaction Details,Amount')
    config.set('SBI_Creditcard', 'igst_selector_regex',
               '^(IGST [DC][BR] @ [0-9]{1,2}[.][0-9]{2}[%%]) ([0-9,]+[.][0-9]{2} [DC])')

    config.add_section('BOB')
    config.set('BOB', 'record_starts_with', '10')
    config.set('BOB', 'data_headers1',
               "{4:'Date',8:'Description',15:'Instrument ID',17:'Amount (INR)',21:'Balance (INR)'}")
    config.set('BOB', 'data_headers2', '')

    config.add_section('IDBI')
    config.set('IDBI', 'record_starts_with', '7')
    config.set('IDBI', 'data_headers1',
               "{4:'Txn Date',5:'Value Date',6:'Description',7:'Cheque No',8:'CR/DR',10:'Amount (INR)',11:'Balance (INR)'}")

    config.add_section('SVC')
    config.set('SVC', 'record_starts_with', '16')

    with open(APP_CONFIG_PATH + 'config.ini', 'w') as f:
        config.write(f)


def __update_to_2_0_0():
    print("Updating config to 2.0.0")
    config.read(APP_CONFIG_PATH + 'config.ini')
    config.set('Basic', 'version', __version_2_0_0__)

    with open(APP_CONFIG_PATH + 'config.ini', 'w') as f:
        config.write(f)


def __update_to_2_0_1():
    print("Updating config to 2.0.1")
    config.read(APP_CONFIG_PATH + 'config.ini')
    config.set('Basic', 'version', __version_2_0_1__)
    config.set('KOTAK', 'record_ends_with', 'Closing balance')

    with open(APP_CONFIG_PATH + 'config.ini', 'w') as f:
        config.write(f)


def __update_to_2_1_0():
    print("Checking and updating config to 2.1.0")
    config.read(APP_CONFIG_PATH + 'config.ini')
    config.set('Basic', 'version', __version_2_1_0__)

    if not config.has_option('SBI_Creditcard', 'igst_date_regex'):
        config.set('SBI_Creditcard', 'igst_date_regex',
                   'for Statement Period: [0-9]{2} [A-Za-z]{3} [0-9]{2} to ([0-9]{2} [A-Za-z]{3} [0-9]{2})')

    CATEGORY = 'YES_Creditcard'
    if not config.has_section(CATEGORY):
        config.add_section(CATEGORY)
    if not config.has_option(CATEGORY, 'data_headers'):
        config.set(CATEGORY, 'data_headers', 'Date,Transaction Details,Merchant Category,Amount')
    if not config.has_option(CATEGORY, 'record_selector_regex'):
        config.set(CATEGORY, 'record_selector_regex',
                   '^(\\d{2}\\/\\d{2}\\/\\d{4}) (.*? - Ref No:[ \\n][0-9A-Z]{23})([ \\nA-Za-z0-9()]*) ([0-9,]+[.][0-9]{2}( Cr| Dr))')
    if not config.has_option(CATEGORY, 'record_end_regex'):
        config.set(CATEGORY, 'record_end_regex',
                   '-End of the Statement-')

    with open(APP_CONFIG_PATH + 'config.ini', 'w') as f:
        config.write(f)
