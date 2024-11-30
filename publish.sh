#!/bin/bash

# Variables comunes
IMAGE_TAG="8h"

# Backend
BACKEND_IMAGE_NAME="backend-users-img"
BACKEND_DOCKERFILE="./Dockerfile" # Ruta al Dockerfile del backend, si está en el root
BACKEND_CONTEXT="."              # Contexto del backend (generalmente root)

# Frontend
FRONTEND_IMAGE_NAME="frontend-users-img"
FRONTEND_DOCKERFILE="./client/Dockerfile" # Ruta al Dockerfile del frontend
FRONTEND_CONTEXT="./client"              # Contexto del frontend

# Build and push backend image
echo "Building backend image..."
docker build -t ttl.sh/$BACKEND_IMAGE_NAME:$IMAGE_TAG -f $BACKEND_DOCKERFILE $BACKEND_CONTEXT
echo "Pushing backend image..."
docker push ttl.sh/$BACKEND_IMAGE_NAME:$IMAGE_TAG

# Build and push frontend image
echo "Building frontend image..."
docker build -t ttl.sh/$FRONTEND_IMAGE_NAME:$IMAGE_TAG -f $FRONTEND_DOCKERFILE $FRONTEND_CONTEXT
echo "Pushing frontend image..."
docker push ttl.sh/$FRONTEND_IMAGE_NAME:$IMAGE_TAG

echo "Images pushed successfully!"
echo "Backend image: ttl.sh/$BACKEND_IMAGE_NAME:$IMAGE_TAG"
echo "Frontend image: ttl.sh/$FRONTEND_IMAGE_NAME:$IMAGE_TAG"