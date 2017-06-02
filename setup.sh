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

### Check for log fil

if ! [ -s ./data/punsch.log ]
then
    touch ./data/punsch.log
fi

### Check for error log

if ! [ -s ./data/punsch.err ]
then
    touch ./data/punsch.err
fi

### Check for input file

if ! [ -s ./data/punschRawInput ]
then
    touch ./data/punschRawInput
    echo "dl_status."$date".0000" >>punsch.log
fi    

### Check status of input XML

if [ -s punschRawInput ]
then
    created=$(grep -oE "<[^>]*tid>[^<]*<[^>]*>" punschRawInput | sed "s/<[^>]*>//g")
    dlmonth=$(echo $created | grep -o '\-[0-9][0-9]\-' | grep -o '[0-9]*')
    dldate=$(echo $created | grep -o '\-[0-9][0-9][^\-]' | grep -o '[0-9]*')
    echo -e 'dl_status.'$date'.'$dlmonth$dldate >>punsch.log
else
    echo -e 'dl_status.'$date'.0000' >>punsch.log
fi

python3 punschCalculator.py
