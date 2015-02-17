#!/bin/bash

chmod 644 slim.conf
mv slim.conf /etc/slim.conf -f
rm set_slim.sh

exit 0
