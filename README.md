# Bank Statement Utility

<!-- buttons -->
<p>
    <a href="https://www.python.org/">
        <img src="https://img.shields.io/badge/python-v3-blue.svg"
            alt="python"></a> &nbsp;
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/license-MIT-blue.svg"
            alt="MIT license"></a> &nbsp;
    <a href="https://github.com/MalayPalace/bank-statment-utility/commits/master">
        <img src="https://img.shields.io/badge/Maintained%3F-yes-blue.svg"
            alt="maintained"></a> &nbsp;
</p>

Bank-Statment-Utility developed out of my personal need to store (and process) bank statements to track expenses or to just search
specific
refund/charge/expense etc across all bank (refer supported banks below) I personally have accounts.
<br><b>SUPPORTS ONLY INDIAN BANK</b>

As a solution created this utility which can be used for dumping bank statement data to the database<i>(as of now Cassandra)</i>
which can be queried upon.

## Background

Have created various configurable parser which can read and store bank statement data to database. It is resilient against any
failure and can log the data which failed storing to database. Re-executable as in same file can be reprocessed wihtout any
duplication issue.

## Banks which are currently supported:

Below are the format information that the utility support for various banks. Download statement as prescribed format below:

### For Saving/Current Account

1. HDFC (Saving and Current Account): `Download as Delimited`
2. Kotak (Saving and Current Account): `Download as CSV (Check Debit/Credit check box)`
3. SBI (Saving & Current Acc): `Download in MS Excel format`
4. Bank of Baroda (Saving & Current Acc): `Download in XLS format`
   _NOTE: Have observed that BOB change the column format quite frequently, so might have to change config settings._
5. IDBI Bank (Saving & Current Acc): `Download in XLS format`
6. SVC Bank (Saving & Current Acc): `Download in XLS format`

## Pre-requisite:
1. You will need running instance of Cassandra database for the Utility to work. Can use official Cassandra docker: https://hub.docker.com/_/cassandra/
2. Create necessary Cassadra keyspace and table by executing ddl: `resource/cqlsh-ddl.sql`
3. Edit the `config/config.ini` file with your Cassandra credentials.
4. Config File need to copied to as local user location for Utility to read it. Execute `install_config_script.sh` file to copy it to target location <i>(Had created primarily on Ubuntu Linux)</i>. For Windows had to manually copy the file. 
5. Install the wheel file directly:
```bash
pip install dist/bank_statement_utility-1.0.0-py3-none-any.whl
```
OR install additional library required for the project from requirement.txt  
```bash
pip install -r requirements.txt
```

## Basic Usage:
Execute the `main.py` from project folder or if you have installed wheel and pip install path is in your Environmental Variable then execute directly `bank_statement_utility`

```bash
bank_statement_utility -n {HDFC,KOTAK,SBI,BOB,IDBI} -t {Saving,Current,Creditcard} filename
```
OR
```bash
python bank_statement_utility/main.py -n {HDFC,KOTAK,SBI,BOB,IDBI} -t {Saving,Current,Creditcard} filename
```

## Build wheel file locally
```bash
python setup.py bdist_wheel
```

## Road Map:
Planning to add more banks and even Credit Card statements.

## Dependencies:
Thanks to below library creator:
<p>
<a href="https://github.com/datastax/python-driver">DataStax Driver for Apache Cassandra</a><br>
<a href="https://pypi.org/project/xlrd/">xlrd</a><br>
<a href="https://pypi.org/project/pytz/">pytz</a><br>