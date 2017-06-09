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

# This file used to contain more stuff that has become more and more obsolete.

### Create data dir

if ! [ -d "./data" ]
then
    mkdir ./data
fi
mv download.sh gpl.txt README.md welcomemsg.txt ./data

echo "Setup complete! Run 'python3 ppk-calculator.py' to start the actual prgoram."
echo -e "Make sure that the following modules are installed to avoid problems:\n- os, re, sys\n- time, datetime\n- BeautifulSoup\n- shutil\n- pathlib\n- operator"

mv setup.sh ./data
