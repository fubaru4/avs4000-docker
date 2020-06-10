#!/bin/bash

#
# This command will create a new container that contains the AVS4000d software pulled
# from the AVID debian repository
#
docker build -f ./avs4000-demo.df --tag avid/avs4000-demo:1.0 .
