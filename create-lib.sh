#!/bin/sh
rm -rf /mnt/project_storage/libs/$1 > /dev/null
cp -rf /mnt/project_storage/sources/$1/latest /mnt/project_storage/libs/$1 > /dev/null
mkdir /mnt/project_storage/libs/$1/.info
echo $2 >> /mnt/project_storage/libs/$1/.info/.name
echo $3 >> /mnt/project_storage/libs/$1/.info/.description
echo "Success"