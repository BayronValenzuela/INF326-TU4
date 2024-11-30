#!/bin/bash

KUBECONFIG=/mnt/c/Users/mazip/Downloads/k8s-inf326-kubeconfig.yaml

# Function to delete resources
delete_resource() {
  local resource_file=$1
  echo "Deleting $resource_file..."
  kubectl delete -f "$resource_file" --ignore-not-found --grace-period=0 --force --kubeconfig "$KUBECONFIG"
  if [[ $? -ne 0 ]]; then
    echo "Error deleting $resource_file. Some resources may not have been removed."
  else
    echo "$resource_file deleted successfully."
  fi
}

# Resources to delete in reverse order
resources=(
  manifests/ingress.yaml
  manifests/hpa.yaml
  manifests/loadbalancer.yaml
  manifests/frontend-service.yaml
  manifests/frontend-deployment.yaml
  manifests/service.yaml
  manifests/deployment.yaml
  manifests/secret.yaml
  manifests/rabbitmq.yaml
  manifests/volume.yaml
  manifests/statefulset.yaml
)

for resource in "${resources[@]}"; do
  delete_resource "$resource"
done

echo "Undeploy completed."


