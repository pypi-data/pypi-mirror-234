#!/bin/bash


if command -v register-python-argcomplete3; then
	argcomplete=register-python-argcomplete3
else
	argcomplete=register-python-argcomplete
fi
eval "$("${argcomplete}" pducontrol)"
