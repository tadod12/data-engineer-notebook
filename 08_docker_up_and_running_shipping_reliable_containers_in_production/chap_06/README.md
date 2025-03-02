# Chapter 6 - Exploring Dockert

## Print the Docker Version

    docker version

## Server Information

    docker info

## Downloading Image Updates

    docker pull ubuntu: latest
    # very specific image
    docker pull ubuntu@sha256:2f9a...82cf

## Inspecting a Container

Once you have a container created, running or not, you can now use `docker` to see how it was configured

    docker run -d -t ubuntu /bin/bash

    docker ps

    docker inspect 3c4f9166619a5

## Getting inside a Running Container

### docker exec

    docker exec -t -i 589f2ad30138 /bin/bash

### nsenter

Name space Enter - allows you to enter any Linux namespace. `nsenter` can also be used to manipulate things in a container as _root_ on the server

> Most of the time, `docker exec` is all you need

More in page 107

## Exploring the Shell

    ps -ef

## Returning a Result

## Docker Logs

    docker logs 3c4f916619a5

The actual files backing this logging are on the Docker server itself, by default in _/var/lib/docker/containers/`<container_id>`/_

## Monitoring Docker

In the mordern world, we monitor everything and report as many statistics as we can

### Container Stats

    docker stats e64a279663aa

More of `curl` in page 114

### Docker Events

    docker events

### cAdvisor

`docker stats` and `docker events` are useful but don't yet get us graphs to look at. One of ther best open source options today comes from Google, called cAdvisor

    docker run \
    --volume=/:/rootfs:ro \
    --volume=/var/run:/var/run:rw \
    --volume=/sys:/sys:ro \
    --volume=/var/lib/docker/:/var/lib/docker:ro \
    --publish=8080:8080 \
    --detach=true \
    --name=cadvisor \
    google/cadvisor:latest

## Exploration

- Copying files in and out of the container wish `docker cp`
- Saving a container's filesystem to a tarball with `docker export`
- Saving an image to a tarball with `docker save`
- Loading an image from a tarball with `docker import`

> 125/222
