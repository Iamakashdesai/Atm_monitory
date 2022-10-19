#!/bin/sh


if pgrep -f "/usr/bin/python /home/admin/test2/ATM/count.py" &>/dev/null; then
    echo "it is already running"
    exit
else
    echo "Started"
    /usr/bin/python /home/admin/test2/ATM/count.py
fi
