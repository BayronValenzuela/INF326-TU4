#!/bin/bash

KUBECONFIG=/mnt/c/Users/mazip/Downloads/k8s-inf326-kubeconfig.yaml

# Eliminar los recursos en orden inverso
kubectl delete -f manifests/statefulset.yaml --kubeconfig "$KUBECONFIG"
kubectl delete -f manifests/volume.yaml --kubeconfig "$KUBECONFIG"
kubectl delete -f manifests/rabbitmq.yaml --kubeconfig "$KUBECONFIG"
kubectl delete -f manifests/secret.yaml --kubeconfig "$KUBECONFIG"
kubectl delete -f manifests/deployment.yaml --kubeconfig "$KUBECONFIG"
kubectl delete -f manifests/service.yaml --kubeconfig "$KUBECONFIG"
kubectl delete -f manifests/loadbalancer.yaml --kubeconfig "$KUBECONFIG"
kubectl delete -f manifests/hpa.yaml --kubeconfig "$KUBECONFIG"
kubectl delete -f manifests/ingress.yaml --kubeconfig "$KUBECONFIG"

# Verificar si hubo errores
if [[ $? -ne 0 ]]; then
  echo "Error deleting manifests. Some resources may not have been removed. Exiting."
  exit 1
fi

echo "Manifests deleted successfully."
