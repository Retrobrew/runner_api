#!/bin/sh
(sleep 600 && helm delete $1-vnc)& > /dev/null