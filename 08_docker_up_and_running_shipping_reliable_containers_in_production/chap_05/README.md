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

A new command was added that allows the root volume of your container to be mounted read-only so that processes within the container cannot write anything to the root filesystem

    docker run -rm -ti --read-only=true -v /mnt/session_data:/data \
        ubuntu:latest /bin/bash

### Resource Quotas

The `docker create` command directly supports configuring CPU and memory restrictions when you create a container

**CPU shares**

Docker thinks of CPU in terms of “cpu shares.” The computing power of all the CPU cores in a system is considered to be the full pool of shares. 1024 is the number that Docker assigns to represent the full pool

> Note that these are not exclusive shares, meaning that assigning all 1024 shares to a container does not prevent all other containers from running

`stress` command - When we run `stress` without ant cgroup constraints, it will use as many resources as we tell it to

    docker run --rm -ti progrium/stress \
        --cpu 2 --io 1 --vm 2 --vm-bytes 128M --timeoue 120s

> More in page 92

**CPU pinning**

This means that work for this container will only be scheduled on the cores that been assigned to this container

    docker run --rm -ti -c 512 --cpuset=0 progrium/stress \
        --cpu 2 --io 1 --vm 2 --vm-bytes 128M --timeout 120s

The `--cpuset` argument is zero-indexed, so your first CPU core is 0 (Another example: `cpuset=0,1,2`)

**Memory**

While constraining the CPU only impacts the application's priority CPU time, the memory limit is _hard_ limit

    docker run --rm -ti -m 512m progrium/stress \
        --cpu 2 --io 1 --vm 2 --vm-bytes 128M --timeout 120s

> Docker supports `b`, `k`, `m`, `g`, representing bytes, kilobytes, megabytes, or gigabytes

The `--memory-swap` option defines the total amount of memory and swap available to the container

    docker run --rm -ti -m 512m --memory-swap=768m progrium/stress \
        --cpu 2 --io 1 --vm 2 --vm-bytes 128M --timeout 120s

This container can have access to 512 MB of memory and 256 MB of additional swap space

**ulimits** - Page 94

## Starting a Container

`docker run`
- `docker create` to create the container
- `docker start` to start the container

Run separately

    docker create -p 6379:6379 redis:2.8

    docker ps -a

    docker start 6b785f78b75e

## Auto Restarting a Container

In many cases, we want our containers to restart if they exit. THe way we tell Docker to do that is by passing the `--restart` argument to the `docker run` command. It takes three values: `no`, `always`, `on-failure:#`

    docker run -ti --restart=on-failure:3 -m 200m --memory-swap=300m \
        progrium/stress --cpu 2 --io 1 --vm 2 --vm-bytes 128M --timeout 120s

## Stopping a Container

When stopped, the process is not paused; it actually exits. On reboot, docker will attempt to start all of the containers that were running at shutdown. We can pause a Docker container with `docker pause` and `unpause`

    docker stop 6b785f78b75e

> Although memory contents will have been lost, all of the container’s filesystem contents and metadata, including environment variables and port bindings, are saved and will still be in place when you restart the container

    docker stop -t 6b785f78b75e

This tells Docker to initially send a `SIGTERM` signal as before, but then if the container has not stopped within 25 seconds, to send a `SIGKILL` signal to forcefully kill it

## Killing a Container

Exit immediately

    docker kill 6b785f78b75e

## Pausing and Unpausing a Container

Pausing leverages the `cgroup` freezer, which essentially just prevent your process from being scheduled until you unfreeze it

## Cleaning Up Containers and Images

List all the containers and delete

    docker ps -a

    docker rm 92b797f12af1

List all the images and delete
    
    docker images

    docker rmi 873c28292d23

> If you try to delete an image that is in use by a container, you will get a _Conflict, cannot delete_ error. You should stop and delete the container(s) first

Delete all of the containers

    docker rm $(docker ps -a -q)

Delete all the images

    docker rmi $(docker images -q -)

To remove all containers that exited with a nonzero state, you can use this filter

    docker rm $(docker ps -a -q --filter 'exited!=0')

And to remove all untagged images, you can type:

    docker rmi $(docker images -q -f "dangling=true")
