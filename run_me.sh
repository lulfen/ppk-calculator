#!/bin/bash

clear
echo "Welcome to Ulfens punsch calculator!"

date=$(date +'%m.%d')
userInput='i'

### Check for log fil

if ! [ -s punsch.log ]
then
    touch punsch.log
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

### Run the first part to initiate either new download or new calculation

python3 punschFirstStep.py

### Run dl or calc

lastLog=$( tail -n 1 punsch.log)
lastMessage=$(echo $lastLog | cut -d \. -f 1 )
lastValue=$(echo $lastLog | cut -d \. -f 4 )

#echo $lastMessage
#echo $lastValue
if test $lastMessage = "dl_request" && test $lastValue -eq 1
then
    mv punschRawInput punschRawInput.old
    wget -O punschRawInput "https://www.systembolaget.se/api/assortment/products/xml" 2>punsch.error
    rm punschRawInput.old
    # move RawInput to temp
    # Download new file
    # if allgood : continue; else : restore old Input # to be implemented
elif test $lastMessage = "calc_request" && test $lastValue -eq 1 && ! test -s ppkList.txt
then
    touch ppkList.txt
    echo "run calculation"
    userInput='c'
elif test $lastMessage = "calc_request" && test $lastValue -eq 1 && test -s ppkList.txt
then
    echo "saved output already exits"
    read -p "Calculate new data (c) or show existing data (d)?" choice
    case "$choice" in
	c|C ) echo "running calculation..."
	      userInput='c' ;;
	d|D ) echo "showing data..."
	      userInput='d' ;;
	* ) echo "invalid coice"
	    userInput='i' ;;
    esac
fi
if test $userInput = 'c'
then
    python3 punschProcessing.py
    sed 's/\t/,/g' ppkList.txt >ppk.txt
    echo "calculation complete"
elif test $userInput = 'd'
then
    #python3 punschOutput.py ### not implemented yet
    echo ""
fi
     

     
