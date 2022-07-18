#!/bin/sh
/usr/local/bin/aws-ecr-update-credentials.sh > /dev/null
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
IMAGE=""
SOURCE_MOUNT="/data"
BUILD_MOUNT="/data/build"

if [ "$2" = "rust" ]
then
    IMAGE="692527062901.dkr.ecr.eu-west-1.amazonaws.com/rust_gba:latest"
    SOURCE_MOUNT="/data/gba/examples"
    BUILD_MOUNT="/data/gba/target"
else
    IMAGE="692527062901.dkr.ecr.eu-west-1.amazonaws.com/gba-c:latest"
fi

helm install $1-$2 templates/compiler/ --set Project.id=$1 --set Project.compiler=$2 --set Project.image=$IMAGE --set Project.source_mount=$SOURCE_MOUNT --set Project.build_mount=$BUILD_MOUNT --set Project.build_mount=$3 > /dev/null
#kubectl apply -f rust_compiler.yaml > /dev/null
kubectl wait pod/$1-$2 --for=condition=Ready
timeout 60s kubectl logs $1-$2 --follow
helm delete $1-$2 > /dev/null