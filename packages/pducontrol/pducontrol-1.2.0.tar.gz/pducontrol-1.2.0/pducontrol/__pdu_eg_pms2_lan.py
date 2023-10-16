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

from typing import List, Optional
import socket
import select


class PDUEgPms2Lan():
    def __connect(self, ip):
        """
        """
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port_result = self.__sock.connect_ex((ip, 5000))
        if port_result != 0:
            raise Exception("Connection failed")
        for _ in range(0, 4):
            self.__sock.send(b"\x11")
            r, _, _ = select.select([self.__sock.fileno()], [], [], 0.125)
            if r:
                return
        raise Exception("No response from the PDU")

    def __authenticate(self):
        """
        """
        k = self.__key
        c = self.__challenge = self.__sock.recv(4)
        # key is password padded with spaces and truncated to 8 chars
        lw = ((c[0] ^ k[2]) * k[0]) ^ (k[6] | k[4] << 8) ^ c[2]
        hw = ((c[1] ^ k[3]) * k[1]) ^ (k[7] | k[5] << 8) ^ c[3]
        lwle = lw.to_bytes(2, byteorder="little")
        hwle = hw.to_bytes(2, byteorder="little")
        self.__sock.send(lwle + hwle)
        r, _, _ = select.select([self.__sock.fileno()], [], [], 4)
        if not r:
            raise Exception("Authentication failure")

    def __init__(self, ip: str, user: str = "", password: str = "1") -> None:
        """
        """
        self.__connect(ip)
        # TODO notify the truncation?
        self.__key = (password + " " * (8 - len(password)))[:8].encode()
        self.__authenticate()
        # eg PDUs don't like very well being queried multiple times.
        # so we cache the statuses
        self.__cached_status = None

    def get_total_outlets(self) -> Optional[int]:
        """Gets the total number of controllable outputs

        Returns
        An integer representing the total number of controllable
        outlets, or None on error
        """
        return 4

    def get_outlet_status(self, outlet: int, timeout=None) -> Optional[str]:
        """Gets the active state of a controllable outlet

        Keyword Arguments:
        outlet -- The outlet number

        Returns:
        A string representing the active state of the outlet,
        or None on error
        """
        return self.get_all_outlet_statuses()[outlet]

    def __status_to_state(self, status):
        if status in [0x11, 0x41]:
            return "on"
        if status in [0x22, 0x82]:
            return "off"

        raise Exception(f"status {status} not handled")

    def get_all_outlet_statuses(self) -> Optional[List[str]]:
        """Gets the active state of all controllable outlets

        Returns
        A list of strings representing the active state of all the
        outlets, or None on error
        """
        if self.__cached_status is None:
            d = self.__sock.recv(4)
            k = self.__key
            c = self.__challenge
            status = [(((d[3 - i] - k[1]) ^ k[0]) - c[3]) ^ c[2]
                      for i in range(0, 4)]

            self.__cached_status = [self.__status_to_state(s % 256)
                                    for s in status]

        return self.__cached_status

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
        if state == "reboot":
            raise Exception("Reboot not implemented")

        statuses = self.get_all_outlet_statuses()
        statuses[outlet - 1] = state
        self.__do_toggle_all_outlets(statuses)

        return state

    def __do_toggle_all_outlets(self, states):
        int_states = [1 if s == "on" else 2 for s in states]
        int_states.reverse()
        k = self.__key
        c = self.__challenge
        e = [((((i ^ c[2]) + c[3]) ^ k[0]) + k[1]) % 256 for i in int_states]
        self.__sock.send(bytearray(e))
        self.__cached_status = None
        self.get_all_outlet_statuses()

    def toggle_all_outlets(self, state: str) -> Optional[str]:
        """Sets the active state of a controllable outlet

        Keyword Arguments:
        state -- The active state to set the outlets to
                 (on, off, reboot)

        Returns:
        A string representing the new active state of all
        the outlets, or None on error
        """
        if state == "reboot":
            raise Exception("Reboot not implemented")

        self.__do_toggle_all_outlets(4 * [state])

        return state

    def get_name(self, outlet: int) -> Optional[str]:
        """Gets the name of an outlet

        Keyword Arguments:
        outlet - The outlet number

        Returns:
        A string containing the name of the outlet
        """
        return self.get_all_names()[int(outlet)]

    def set_name(self, outlet: int, name: str) -> Optional[str]:
        """Sets the name of an outlet

        Args:
            outlet: the outlet number
            name: the name to set (under 32 characters)
        """
        raise NotImplementedError("name accessors not implemented yet")

    def get_all_names(self) -> List[str]:
        """Gets the name of all outlets"""
        # get_all_names is called when choosing the pdu implementation, so we
        # need at leats a dummy implementation
        return ["dummy 1", "dummy 2", "dummy 3", "dummy 4"]

    def __del__(self):
        self.__sock.send(b'\x11')


if __name__ == "__main__":
    pdu = PDUEgPms2Lan("192.168.10.202")
    print(pdu.get_all_outlet_statuses())
