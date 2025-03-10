#!/bin/bash

set -e

sudo apt update -y && sudo apt install -y --no-install-recommends curl ca-certificates libsqlite3-mod-spatialite libspatialite-dev git build-essential
sudo ln -sf /usr/lib/x86_64-linux-gnu/mod_spatialite.so /usr/lib/x86_64-linux-gnu/mod_spatialite
