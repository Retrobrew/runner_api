#!/bin/sh
helm delete $1-vnc > /dev/null
/usr/local/bin/aws-ecr-update-credentials.sh > /dev/null
helm install  $1-vnc templates/vnc/ -f templates/compiler/values.yaml --set Project.id=$1 --set Project.version=$2 > /dev/null
#kubectl apply -f rust_compiler.yaml > /dev/null
#kubectl wait --for=condition=available deployment/$1-deployment > /dev/null
echo http://$1.retrobrew.fr
#kubectl delete -f rust_compiler.yaml > /dev/null
