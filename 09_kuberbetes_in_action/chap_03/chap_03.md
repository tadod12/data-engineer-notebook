# Chapter 3 - Pods: running containers in Kubernetes

## 3.1. Introducing pods

Instead of deploying containers individually, you always deploy and operate on a pod of containers. The key thing about pods is that when a pod does contain multiple containers, all of them are always run on a single worker node

### 3.1.1. Understanding why we need pods

### 3.1.2. Understanding pods

**UNDERSTANDING THE PARTIAL ISOLATION BETWEEN CONTAINERS OF THE SAME POD**

Isolate groups of containers instead pf individual ones. You want containers inside each group to share certain resources, although not all, so that they’re not fully isolated

> Configure Docker to have all containers of a pod share the same set of Linux namespaces instead of each container having its own set

**UNDERSTANDING HOW CONTAINERS SHARE THE SAME IP AND PORT SPACE**

One thing to stress here is that because containers in a pod run in the same Network namespace, they share the same IP address and port space. All the containers in a pod also have the same loopback network interface, so a container can communicate with other containers in the same pod through `localhost`

**INTRODUCING THE FLAT INTER-POD NETWORK**

All pods in a Kubernetes cluster reside in a single flat, shared, network-address space, which means every pod can access every other pod at the other pod’s IP address