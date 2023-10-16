#!/bin/bash
# This file is part of pdu-control
# Copyright (C) 2023 Safran
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <https://www.gnu.org/licenses/>.

echo y | pip uninstall pducontrol
python setup.py clean
rm -rf dist
python setup.py sdist
pip install dist/pducontrol*
eval "$(register-python-argcomplete pducontrol)"