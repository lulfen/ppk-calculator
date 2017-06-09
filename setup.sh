#!/bin/bash

clear
echo "Welcome to Ulfens punsch calculator!"

date=$(date +'%m.%d')
userInput='i'

### Check for data dir

if ! [ -d "./data" ]
then
    mkdir ./data
fi

### Check for calculation

if ! [ -s ./data/ppk.txt ]
then
    touch ./data/ppk.txt
fi

### Check for input file

if ! [ -s ./data/punschRawInput ]
then
    touch ./data/punschRawInput
fi    

echo "Setup complete! Run 'python3 punschOutput.py' to start the actual prgoram."
