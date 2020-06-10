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
docker container run -it --rm --name avs4000-demo --privileged -v /dev:/dev -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix avid/avs4000-demo:1.0
