#!/bin/bash

docker build -t ghcr.io/acarling/arma3server:latest .
docker push ghcr.io/acarling/arma3server:latest
