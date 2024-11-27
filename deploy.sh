#!/bin/bash

KUBECONFIG=/mnt/c/Users/mazip/Downloads/k8s-inf326-kubeconfig.yaml

kubectl apply -f manifests/statefulset.yaml --kubeconfig "$KUBECONFIG"
kubectl apply -f manifests/volume.yaml --kubeconfig "$KUBECONFIG"
kubectl apply -f manifests/rabbitmq.yaml --kubeconfig "$KUBECONFIG"
kubectl apply -f manifests/secret.yaml --kubeconfig "$KUBECONFIG"
kubectl apply -f manifests/deployment.yaml --kubeconfig "$KUBECONFIG"
kubectl apply -f manifests/service.yaml --kubeconfig "$KUBECONFIG"
kubectl apply -f manifests/loadbalancer.yaml --kubeconfig "$KUBECONFIG"
kubectl apply -f manifests/hpa.yaml --kubeconfig "$KUBECONFIG"
kubectl apply -f manifests/ingress.yaml --kubeconfig "$KUBECONFIG"


if [[ $? -ne 0 ]]; then
  echo "Error applying manifests. Exiting."
  exit 1
fi

echo "Manifests applied successfully."
