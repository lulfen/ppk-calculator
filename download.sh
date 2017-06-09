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
