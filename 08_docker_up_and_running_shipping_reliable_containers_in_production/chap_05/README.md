# Chapter 5 - Working with Docker Containers

## What Are Containers

Containers are a fundamentally different approach where all containers share a single kernel and isolation is implemented entirely within that single kernel

> A container is a self-contained execution environment that shares the kernel of the host system and which is (optionally) isolated from other containers in the system

## Creating a Container

`docker run` wraps two separate steps into one
- Create a container from the underlying image (`docker create`)
- Execute the container (`docker start`)

### Basic Configuration

**Container name** 

By default, Docker randomly names your container by combining an adjective with the name of a famous person. If you want to give your container a specific name, you can do so using the `--name` argument

    docker create --name="awesome-service" ubuntu:latest

**Labels**

Labels are key-value pairs that can be applied to Docker images and containers as metadata. When new Docker containers are created, they automatically inherit all the labels from their parent image

Add new labels to the containers

    docker run -d --name labels -l deployer=Ahmed -l tester=Asako \
        ubuntu:latest sleep 1000

You can then search for and filter containers based on this metadata

    docker ps -a -f label=deployer=Ahmed

Using `docker inspect` to see all the labels that a container has

    docker inspect 845731631ba4

**Hostname**

When you start a container, Docker will copy certain system files on the host, including _/etc/hostname/_, into the container's configuration directory on the host, and then use a bind mount to link that copy of the file into the container

Launch a default container with no special configuration

    docker run --rm -ti ubuntu:latest /bin/bash

> The `--rm` argument tells Docker to delete the container when it exits, the `-t` argument tells Docker to allocate a psuedo-TTY (color formatting, ...), and the `-i` argument tells Docker that this is going to be an interactive session, and we want to keep STDIN open. The final argument in the command is the exectuable that we want to run within the container, which in this case is the ever useful `/bin/bash`

> Don't forget to `exit` the container shell so that we return to the Docker host when finished

If we now run the mount command from within the resulting container, we will seesomething similar to this:

    root@ebc8cf2d8523:/# mount
    overlay on / type overlay (rw,relatime,lowerdir=...,upperdir=...,workdir...)
    proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
    tmpfs on /dev type tmpfs (rw,nosuid,mode=755)
    shm on /dev/shm type tmpfs (rw,nosuid,nodev,noexec,relatime,size=65536k)
    mqueue on /dev/mqueue type mqueue (rw,nosuid,nodev,noexec,relatime)
    devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,...,ptmxmode=666)
    sysfs on /sys type sysfs (ro,nosuid,nodev,noexec,relatime)
    /dev/sda9 on /etc/resolv.conf type ext4 (rw,relatime,data=ordered)
    /dev/sda9 on /etc/hostname type ext4 (rw,relatime,data=ordered)
    /dev/sda9 on /etc/hosts type ext4 (rw,relatime,data=ordered)
    devpts on /dev/console type devpts (rw,nosuid,noexec,relatime,...,ptmxmode=000)
    proc on /proc/sys type proc (ro,nosuid,nodev,noexec,relatime)
    proc on /proc/sysrq-trigger type proc (ro,nosuid,nodev,noexec,relatime)
    proc on /proc/irq type proc (ro,nosuid,nodev,noexec,relatime)
    proc on /proc/bus type proc (ro,nosuid,nodev,noexec,relatime)
    tmpfs on /proc/kcore type tmpfs (rw,nosuid,mode=755)
    root@ebc8cf2d8523:/#

> Lệnh mount trong Linux hiển thị danh sách các filesystem được gắn kết (mounted). Khi chạy trong Docker container, nó giúp hiểu cách Docker ánh xạ các file hệ thống giữa host và containerr

Set the hostname specifically

    docker run --rm -ti --hostname="mycontainer.example.com" ubuntu:latest /bin/bash
    
    root@mycontainer:/# hostname -f
    mycontainer.example.com

**Domain Name Service (DNS)**

The _resolv.conf_ file is managed via a bind mount between the host and container

    /dev/sda9 on /etc/resolv.conf type ext4 (rw,relatime,data=ordered)

**Media Access Control (MAC) address**

### Storage Volumes

Mounting `/mnt/session_data` to `/data` within the container

    docker run --rm -ti -v /mnt/session_data:/data ubuntu:latest /bin/bash

If the container application is designed to write into `/data`, then this data will be visible on the host filesystem in `/mnt/session_data` and would remain available when this container was stopped and a new container started with the same volume mounted

> 89/222