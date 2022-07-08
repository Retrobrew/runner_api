#!/bin/sh
/usr/local/bin/aws-ecr-update-credentials.sh > /dev/null
helm install  $1-vnc templates/vnc/ -f templates/compiler/values.yaml --set Project.id=$1 --set Project.version=$2 > /dev/null
#kubectl apply -f rust_compiler.yaml > /dev/null
sleep 5
echo http://$1.retrobrew.fr
#kubectl delete -f rust_compiler.yaml > /dev/null