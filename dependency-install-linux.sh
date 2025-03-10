#!/bin/bash

set -e

sudo apt update -y && sudo apt install -y --no-install-recommends curl ca-certificates libsqlite3-mod-spatialite libspatialite-dev git build-essential
sudo ln -sf /usr/lib/x86_64-linux-gnu/mod_spatialite.so /usr/lib/x86_64-linux-gnu/mod_spatialite

UV_VERSION="0.6.5"
if ! [ -x "$(command -v uv)" ]; then
    echo "UV is not installed. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
else
    echo "UV is already installed."
fi
