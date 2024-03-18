#!/bin/bash

cmd=$1

# Constants
IMAGE_TAG="$(git describe --always)"

usage() {
    echo "deploy.sh <command>"
    echo "Available commands:"
    echo " build        Build the docker image"
    echo " push         Push the docker image to the registry"
    echo " build_push   Build and push the docker image to the registry"
}

if [[ -z "$cmd" ]]; then
    echo "Missing command"
    usage
    exit 1
fi

build() {
    docker build --tag "$IMAGE_NAME":"$IMAGE_TAG" -f deployment/Dockerfile .
    docker tag "$IMAGE_NAME":"$IMAGE_TAG" "$IMAGE_NAME":latest
}

push() {
    docker push "$IMAGE_NAME":"$IMAGE_TAG"
    docker push "$IMAGE_NAME":latest
}

shift

case "$cmd" in
    build)
        build "$@"
        ;;
    push)
        push "$@"
        ;;
    build_push)
        build "$@"
        push "$@"
        ;;
    *)
        echo -n "Unknown command: $cmd"
        usage
        exit 1
        ;;
esac
