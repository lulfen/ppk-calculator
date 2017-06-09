#!/bin/bash

# This file is part of Ulfen's PPK-Calculator.
# 
# Ulfen's PPK-Calculator is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# Ulfen's PPK-Calculator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Ulfen's PPK-Calculator.  If not, see
# <http://www.gnu.org/licenses/>.

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
