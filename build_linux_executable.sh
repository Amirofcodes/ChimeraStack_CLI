#!/bin/bash

# Build the Docker image
docker build -t chimera-build -f Dockerfile.build .

# Create a temporary container
CONTAINER_ID=$(docker create chimera-build)

# Copy the executable from the container
docker cp $CONTAINER_ID:/app/dist/chimera-stack-cli ./releases/chimera-stack-cli-linux

# Remove the temporary container
docker rm $CONTAINER_ID

# Make the Linux executable executable
chmod +x ./releases/chimera-stack-cli-linux

# Generate checksum
cd releases && shasum -a 256 chimera-stack-cli-linux >> SHA256SUMS.txt

echo "Linux executable built and placed in releases/chimera-stack-cli-linux"
