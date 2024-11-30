#!/bin/bash

KUBECONFIG=/mnt/c/Users/mazip/Downloads/k8s-inf326-kubeconfig.yaml

# List of manifests to apply
manifests=(
  manifests/statefulset.yaml
  manifests/volume.yaml
  manifests/rabbitmq.yaml
  manifests/secret.yaml
  manifests/deployment.yaml
  manifests/service.yaml
  manifests/frontend-deployment.yaml
  manifests/frontend-service.yaml
  manifests/loadbalancer.yaml
  manifests/hpa.yaml
  manifests/ingress.yaml
)

# Apply manifests
for manifest in "${manifests[@]}"; do
  echo "Applying $manifest..."
  kubectl apply -f "$manifest" --kubeconfig "$KUBECONFIG"
  if [[ $? -ne 0 ]]; then
    echo "Error applying $manifest. Exiting."
    exit 1
  fi
done

echo "All manifests applied successfully."

