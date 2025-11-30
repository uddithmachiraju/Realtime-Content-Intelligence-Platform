FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install essential build tools, python dev packages, and pip
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git

WORKDIR /workspaces
