#!/bin/bash

# Prerequisites:
#   - You have sudo privs
#   - The 90-usb-avs4000.rules file has been installed on the docker host
#   - The following has been run on the docker host:
#	- sudo udevadm control --reload-rules
#	- sudo udevadm trigger
#

#
# This script will start a docker container that contains the AVS4000d application inside of
# an Ubuntu 18.04 image.
#

docker container run -it --rm --name avs4000 -p 12900:12900 -p 12901:12901 -p 12701:12701 --privileged -v /dev:/dev avid/avs4000:1.0
