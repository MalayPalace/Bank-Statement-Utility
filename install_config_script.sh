#!/bin/bash

# create directories (that don't exist, yet)
App_Path=$HOME/.local/share/bank-statement-app
mkdir -p "$App_Path"

cp "config/config.ini" "$App_Path/config.ini"
echo "DONE"