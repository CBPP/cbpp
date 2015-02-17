#!/bin/bash
# ----------
# Simple script to restart tint2

if [ "$(pidof tint2)" ]; then
    killall tint2 && sleep 1s && tint2 &
    exit 0
else
    tint2 &
    exit 0
fi
