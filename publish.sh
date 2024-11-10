#!/bin/bash

IMAGE_NAME="ncerpa-inf326-demo-app-users"
IMAGE_TAG="8h"

# Build the Docker image
docker build -t ttl.sh/$IMAGE_NAME:$IMAGE_TAG .

# Push the image to ttl.sh
docker push ttl.sh/$IMAGE_NAME:$IMAGE_TAG

echo "Image pushed successfully: ttl.sh/$IMAGE_NAME:$IMAGE_TAG"%