# Chapter 3 - Pods: running containers in Kubernetes

## 3.1. Introducing pods

Instead of deploying containers individually, you always deploy and operate on a pod of containers. The key thing about pods is that when a pod does contain multiple containers, all of them are always run on a single worker node

### 3.1.1. Understanding why we need pods

### 3.1.2. Understanding pods

**UNDERSTANDING THE PARTIAL ISOLATION BETWEEN CONTAINERS OF THE SAME POD**

Isolate groups of containers instead pf individual ones. You want containers inside each group to share certain resources, although not all, so that they’re not fully isolated

> Configure Docker to have all containers of a pod share the same set of Linux namespaces instead of each container having its own set. All containers of a pod share the same hostname and network interfaces.

**UNDERSTANDING HOW CONTAINERS SHARE THE SAME IP AND PORT SPACE**

One thing to stress here is that because containers in a pod run in the same Network namespace, they share the same IP address and port space. All the containers in a pod also have the same loopback network interface, so a container can communicate with other containers in the same pod through `localhost`

**INTRODUCING THE FLAT INTER-POD NETWORK**

All pods in a Kubernetes cluster reside in a single flat, shared, network-address space, which means every pod can access every other pod at the other pod’s IP address

### 3.1.3. Organizing containers across pods properly

Blah Blah Blah

## 3.2. Creating pods from YAML or JSON descriptors

Pods and other Kubernetes resources are usually created by posting a JSON or YAML manifest to the Kubernetes REST API endpoint.

TO configure all aspects of each type of resources, you'll need to know and understand the Kubernetes API object definitions: http://kubernetes.io/docs/reference/

### 3.2.1. Examining a YAML descriptor of an existing pod

**INTRODUCING THE MAIN PARTS OF A POD DEFINITION**

- _Metadata_ includes name, namespace, labels, and other information about the pod
- _Spec_ contains the actual description of the pod's contents, such as the pod's containers, volumes, and other data
- _Status_ contains the current information about the running pod, such as what condition the pod is in, the description and status of each container, and the pod’s internal IP and other basic info.

### 3.2.2. Creating a simple YAML descriptor for a pod

    apiVersion: v1              # Descriptor conforms to version v1 of Kubernetes API
    kind: Pod                   # You're describing a pod
    metadata:
      name: kubia-manual        # The name of the pod
    spec:
      containers:
      - image: luksa/kubia      # Container image to create the container from
        name: kubia             # Name of the container
        ports:
        - containerPort: 8080   # The port the app is listening on
          protocol: TCP

### 3.2.3. Using kubectl create to create the pod

### 3.2.4. Viewing application logs

### 3.2.5. Sending requests to the pod

## 3.3. Organizing pods with labels

### 3.3.1. Introducing labels

### 3.3.2. Specifying labels when creating a pod

### 3.3.3. Modifying labels of existing pods

## 3.4. Listing subsets of pods through label selectors

### 3.4.1. Listing pods using a label selector

### 3.4.2. Using multiple conditions in a label selector

## 3.5. Using labels and selectors to constrain pod scheduling

### 3.5.1. Using labels for categorizing worker nodes

### 3.5.2. Scheduling pods to specific nodes

    apiVersion: v1
    kind: Pod
    metadata:
      name: kubia-gpu
    spec:
      nodeSelector:
        gpu: "true"         # deploy this pod only to nodes containing the gpu=true label
      containers:
      - image: luksa/kubia
        name: kubia

### 3.5.3. Scheduling to one specific node

## 3.6. Annotating pods

In addition to labels, pods and other objects can also contain annotations. Annotations are also key-value pairs, so in essence, they’re similar to labels, but they aren’t meant to hold identifying information.

On the other hand, annotations can hold much larger pieces of infomation and are primarily meant to be used by tools. Certain annotations are automatically added to objects by Kubernetes, but others are added by users manually.

## 3.7. Using namespaces to group resources

Kubernetes namespaces provide a scope for objects names. Instead of having all your resources in one single namespace, you can split them into multiple namespaces, which also allows you to use the same resource names multiple times (across different namespaces).

### 3.7.1. Understanding the need for namespaces

### 3.7.2. Discovering other namespaces and their pods

List all namespaces in cluster:

    kubectl get ns

List pods in specific namespace:

    kubectl get pods -n kube-system

Namespaces enable you to separate resources that don’t belong together into nonoverlapping groups. If several users or groups of users are using the same Kubernetes cluster, and they each manage their own distinct set of resources, they should each use their own namespace.

### 3.7.3. Creating a namespace

**CREATING A NAMESPACE FROM A YAML FILE**

    apiVersion: v1
    kind: Namespace             # Defining a namespace
    metadata:
      name: custom-namespace    # The name of the namespace

Use `kubectl` to post the file to the Kubernetes API server

    kubectl create -f custom-namespace.yaml

**CREATING A NAMESPACE WITH KUBECTL CREATE NAMESPACE**

    kubectl create namespace custom-namespace

### 3.7.4. Managing objects in other namespaces

To create resources in the namespace you’ve created, either add a namespace: custom-namespace entry to the metadata section, or specify the namespace when creating the resource with the kubectl create command:

    kubectl create -f kubia-manual.yaml -n custom-namespace

When listing, describing, modifying, or deleting objects in other namespaces, you need to pass the `--namespace` (or `-n`) flag to `kubectl`

### 3.7.5. Understanding the isolation provided by namespaces

## 3.8. Stopping and removing pods
