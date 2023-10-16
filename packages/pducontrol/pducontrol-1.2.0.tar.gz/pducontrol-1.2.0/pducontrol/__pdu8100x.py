#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

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

import re
from typing import List, Optional

from pducontrol.__snmp import SNMPClient


class PDU8100X(SNMPClient):
    """Interface class for controlling the Cyberpower PDU8100X family of
    devices via SNMP.

    Notes
     - Datasheet can be found in the downloads section of the following
       page:
       https://www.cyberpowersystems.com/product/pdu/switched-mbo/pdu81006/
     - Only works on linux (as this package uses the 'snmpwalk' bash
       command)
     - Ensure the 'snmp' system package is installed
    """

    OID_base = "SNMPv2-SMI::enterprises.3808"

    # OID to get number of total outlets in the PDU
    ePDUOutletDevNumTotalOutlets_OID = "1.1.3.3.1.4"

    # OID to control all outlets simultaneously
    ePDUOutletDevCommand_OID = "1.1.3.3.1.1.0"
    # Valid commands for controlling all outlets simultaneously
    ePDUOutletDevCommand_VALUES = {
        "on": 2,
        "off": 3,
        "reboot": 4,
    }
    ePDUOutletDevCommand_VALUES_REVERSE = {2: "on", 3: "off", 4: "reboot"}

    # OID to control individual outlets
    ePDUOutletControlCommand_OID = "1.1.3.3.3.1.1.4"
    # Valid commands for controlling each outlets individually
    ePDUOutletControlCommand_VALUES = {"on": 1, "off": 2, "reboot": 3}
    ePDUOutletControlCommand_VALUES_REVERSE = {1: "on", 2: "off", 3: "reboot"}

    # OID to get state of individual outlets
    ePDUOutletStatusOutletState_OID = "1.1.3.3.5.1.1.4"
    # Dictionary that maps returned outlet status to a human readable form
    ePDUOutletStatusOutletState_RESULTS = {1: "on", 2: "off"}

    # OID to control outlet names
    ePDUOutletControlOutletName_OID = "1.1.3.3.3.1.1.2"
    # OID to configure outlet names
    ePDUOutletConfigOutletName_OID = "1.1.3.3.4.1.1.2"

    def __init__(self, ip: str, user: str = "", password: str = "",
                 version: str = "2c") -> None:
        """Constructor for the PDU8100X class

        Keyword Arguments:
        ip -- IPv4 address of the PDU8100X device
        version -- SNMP version to use ('1' or '2c')
        user -- unused, here for cross-compatibility
        password -- unused, here for cross-compatibility
        """
        if version not in ("1", "2c"):
            raise ValueError(
                "PDU8100X SNMP version must be either 1 or 2c "
                "(representing v1 & v2c protocols)"
            )
        super().__init__(ip=ip, version=version)

    def get_total_outlets(self) -> Optional[int]:
        """Gets the total number of controllable outputs

        Returns
        An integer representing the total number of controllable
        outlets, or None on error
        """
        oid = f"{self.OID_base}.{self.ePDUOutletDevNumTotalOutlets_OID}"
        value_type = "i"
        result = self.snmpwalk(oid=oid)
        if result is None:
            return None

        return int(self.parse_by_type(line=result, value_type=value_type))

    def get_outlet_status(self, outlet: int, timeout=None) -> Optional[str]:
        """Gets the active state of a controllable outlet

        Keyword Arguments:
        outlet -- The outlet number

        Returns:
        A string representing the active state of the outlet,
        or None on error
        """
        if type(outlet) != int or outlet <= 0:
            raise ValueError("outlet must be a positive integer")

        o = f"{self.OID_base}.{self.ePDUOutletStatusOutletState_OID}.{outlet}"
        value_type = "i"
        result = self.snmpwalk(oid=o, timeout=timeout)
        if result is None:
            return None

        return self.ePDUOutletStatusOutletState_RESULTS[
            int(self.parse_by_type(line=result, value_type=value_type))
        ]

    def get_all_outlet_statuses(self) -> Optional[List[str]]:
        """Gets the active state of all controllable outlets

        Returns
        A list of strings representing the active state of all the
        outlets, or None on error
        """
        oid = f"{self.OID_base}.{self.ePDUOutletStatusOutletState_OID}"
        value_type = "i"
        result = self.snmpwalk(oid=oid)
        if result is None:
            return None

        return [
            self.ePDUOutletStatusOutletState_RESULTS[
                int(self.parse_by_type(line=line, value_type=value_type))
            ]
            for line in result.splitlines()
        ]

    def toggle_outlet(self, outlet: int, state: str) -> Optional[str]:
        """Sets the active state of a controllable outlet

        Keyword Arguments:
        outlet -- The outlet number
        state -- The active state to set the outlet to
                 (on, off, reboot)

        Returns:
        A string representing the new active state of the
        outlet, or None on error
        """
        if type(outlet) != int or outlet <= 0:
            raise ValueError("outlet must be a positive integer")
        values = self.ePDUOutletControlCommand_VALUES
        if type(state) != str or state not in values:
            raise ValueError(f"state must be one of {values.keys()}")

        oid = f"{self.OID_base}.{self.ePDUOutletControlCommand_OID}.{outlet}"
        value_type = "i"
        result = self.snmpset(
            oid=oid, value_type=value_type, value=str(values[state])
        )
        if result is None:
            return None
        return self.ePDUOutletControlCommand_VALUES_REVERSE[
            int(self.parse_by_type(line=result, value_type=value_type))
        ]

    def toggle_all_outlets(self, state: str) -> Optional[str]:
        """Sets the active state of a controllable outlet

        Keyword Arguments:
        state -- The active state to set the outlets to
                 (on, off, reboot)

        Returns:
        A string representing the new active state of all
        the outlets, or None on error
        """
        if type(state) != str or state not in self.ePDUOutletDevCommand_VALUES:
            raise ValueError(
                "state must be one of "
                f"{self.ePDUOutletDevCommand_VALUES.keys()}"
            )

        oid = f"{self.OID_base}.{self.ePDUOutletDevCommand_OID}"
        value_type = "i"
        result = self.snmpset(
            oid=oid,
            value_type=value_type,
            value=str(self.ePDUOutletDevCommand_VALUES[state]),
        )
        if result is None:
            return None

        return self.ePDUOutletDevCommand_VALUES_REVERSE[
            int(self.parse_by_type(line=result, value_type=value_type))
        ]

    def get_name(self, outlet: int) -> Optional[str]:
        """Gets the name of an outlet

        Keyword Arguments:
        outlet - The outlet number

        Returns:
        A string containing the name of the outlet
        """
        o = f"{self.OID_base}.{self.ePDUOutletControlOutletName_OID}.{outlet}"
        result = self.snmpwalk(oid=o)
        if result is None:
            return None
        return re.sub(r'.*STRING: "(.*)"', r"\1", result).strip()

    def set_name(self, outlet: int, name: str) -> Optional[str]:
        """Sets the name of an outlet

        Args:
            outlet: the outlet number
            name: the name to set (under 32 characters)
        """
        if type(outlet) != int or outlet <= 0:
            raise ValueError("outlet must be a positive integer")
        if len(name) > 32 or len(name) > 32:
            raise ValueError("name should be under 32 characters")
        oid = f"{self.OID_base}.{self.ePDUOutletConfigOutletName_OID}.{outlet}"
        value_type = "s"
        result = self.snmpset(
            oid=oid, value_type=value_type, value=str(name)
        )
        if result is None:
            return None
        else:
            return f"Successfully renamed outlet {outlet} to {name}"

    def get_all_names(self) -> List[str]:
        """Gets the name of all outlets"""
        return list(map(self.get_name, range(1, self.get_total_outlets() + 1)))


if __name__ == "__main__":
    pdu = PDU8100X("10.15.226.55")
    pdu.set_name(16, "test")
