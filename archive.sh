#!/bin/sh
[ -d "/mnt/project_storage/sources/$1/$2" ] && echo "Version $2 exist" || cp -r /mnt/project_storage/sources/$1/latest /mnt/project_storage/sources/$1/$2 > /dev/null