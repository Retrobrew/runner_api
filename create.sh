#!/bin/sh
mkdir /mnt/project_storage/sources/$1
mkdir /mnt/project_storage/sources/$1/latest
unzip templates/project/$2.zip -d /mnt/project_storage/sources/$1/latest