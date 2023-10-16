# pducontrol

## NAME
pdu_settings.cfg - configuration file for pducontrol, a cli executable for controlling power delivery units

## SYNOPSIS
`~/.config/pducontrol/pdu_settings.cfg`

## DESCRIPTION
The `pducontrol` config file is used to configure the settings for a PDU (Power Distribution Unit).
It contains the IP address, username, and password necessary to connect to the PDU and manage its settings.

## CONFIGURATION OPTIONS
 The general format of `pdu_settings.cfg` is as follows:

- `[name]`: Specifies the name of the PDU. Only used as a section name by the parser.
- `ip_address`: Specifies the IP address of the PDU. 
- `username`: Specifies the username to use when connecting to the PDU.
- `password`: Specifies the password to use when connecting to the PDU.

## EXAMPLES
 Here is a short example of a configuration file:


        [pdu.example1]
        
        ip_address = 192.168.2.23  
        username = ntp  
        password = 9ABC  

This example configures the PDU with the IP address `192.168.2.23`, the username "ntp" and the password "9ABC".


## AUTHOR

pdu-control was written by Pol Bodet <pol.bodet@nav-timing.safrangroup.com>.


## DISTRIBUTION
The latest version of pdu-control may be downloaded from (https://bitbucket.org/spectracom/pdu-control/)
