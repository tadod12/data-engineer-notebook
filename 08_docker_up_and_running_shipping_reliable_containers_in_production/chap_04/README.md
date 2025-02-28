# Chapter 4 - Working with Docker Images

## Anatomy of a Dockerfile

A typical Dockerfile

    FROM node:0.10                          # Base image

    MAINTAINER Anna Doe <anna@example.com>  # Populate author in metadata
    
    LABEL "rating"="Five Stars" "class"="First Class"
    
    USER root                               # run process as root
    
    # Environment shell variables
    ENV AP /data/app
    ENV SCPATH /etc/supervisor/conf.d
    
    RUN apt-get -y update
    
    # The daemons
    RUN apt-get -y install supervisor
    RUN mkdir -p /var/log/supervisor
    
    # Supervisor Configuration
    ADD ./supervisord/conf.d/* $SCPATH/
    
    # Application Code
    ADD *.js* $AP/
    
    # Change the working directory
    WORKDIR $AP
    
    RUN npm install
    
    CMD ["supervisord", "-n"]               # run supervisord -n after container start

The `ENV` instruction allows you to set shell variables that can be used during the build process to symplify the Dockerfile

The `ADD` instruction is used to copy files from the local filesystem into your Images

> Every instruction creates a new Docker image layer, so it often makes sense to combine a few logically grouped commands onto a single line. It is even possible to use the `ADD` instruction in combination with the `RUN` instruction to copy a complex script to your image and then execute that script with only two commands in the Dockerfile

## Building an Image

    git clone https://github.com/spkane/docker-node-hello.git

    cd docker-node-hello

    tree -a -I .git
    .
    ├── .dockerignore
    ├── .gitignore
    ├── Dockerfile
    ├── Makefile
    ├── README.md
    ├── Vagrantfile
    ├── index.js
    ├── package.json
    └── supervisord
        └── conf.d
            ├── node.conf
            └── supervisord.conf

The _.dockerignore_ file allows you to define files and directories that you do not want uploaded to the Docker host when building the image

    # -t for tag name, . for current directory
    docker build -t example/docker-node-hello:latest .

> To improve the speed of builds, Docker will use a local cache when it thinks it is safe. This can sometimes lead to unexpected issues. You can disable the cache for a build by using the `--no-cache` argument to the `docker build` command

## Running Your Image

Once you have successfully built the image, you can run it on your Docker host with the following command

    docker run -d -p 8080:8080 example/docker-node-hello:latest

Create a running container in the background (`-d`) from the image with the `example/docker-node-hello:latest` tag, and map (`-p`) port 8080 in the container to port 8080 on the Docker host

Checking container 

    docker ps

You can usually determine the Docker host IP address by simply printing out the value of the DOCKER_HOST environment variable unless you are only running Docker locally, in which case `127.0.0.1` should work

    echo $DOCKER_HOST
    # tcp://172.17.41.10:2376

Get the IP address and enter something like `http://172.17.42.10:8080/` into your web browser address bar. You should see the following text:
    
    Hello World. Wish you were here.

### Environment Variables

File `index.js`

    var DEFAULT_WHO = "World";
    var WHO = process.env.WHO || DEFAULT_WHO;

You can configure this application by passing in environment variables

    docker ps
    
    docker stop b7145e06083f
    
    # use -e
    docker run -d -p 8080:8080 -e WHO="Sean and Karl" \
    example/docker-node-hello:latest

## Custom Base Images

## Storing Images

Storing your images into a central repository for easy retrieval
