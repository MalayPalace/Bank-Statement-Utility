# python 3.x
from configparser import ConfigParser

from .version import __version__
from .Constants import APP_CONFIG_PATH

config = ConfigParser()


def write_default_config():
    config.read(APP_CONFIG_PATH + 'config.ini')

    config.add_section('Basic')
    config.set('Basic', 'version', __version__)
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
