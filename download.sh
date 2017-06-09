#!/bin/bash
url='https://www.systembolaget.se/api/assortment/products/xml'
if [ -f ./data/punschRawInput ] ; then
    mv ./data/punschRawInput ./data/oldInput
    wget "$url" >./data/punschRawInput
    mv ./xml ./data/punschRawInput
    rm ./data/oldInput
else
    wget "$url" >./data/punschRawInput
    mv ./xml ./data/punschRawInput
fi
