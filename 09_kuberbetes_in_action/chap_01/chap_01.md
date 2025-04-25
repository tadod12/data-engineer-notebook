# Chapter 1 - Introducing Kubernetes

## 1.1. Understanding the need for a system like Kubernetes

### 1.1.1. Moving from monolithic apps to microvervices

Microservices communicate through
- Synchronous protocols: HTTP, RESTful (Representational State Transfer) APIs
- Asynchronous protocols: such as AMQP (Advanced Message Queueing Protocol)

**SCALING MICROSERVICES** - only those services that require more resources

![Each microservice can be scaled individually](../assets/chap_01/scaling.png)

**DEPLOYING MICROSERVICES**

> Drawbacks: number of inter-dependencies between the components increases

![Multiple applications running on the same host may have conflicting dependencies](../assets/chap_01/dependencies.png)

Debug and trace execution calls: Using distributed tracing systems such as Zipkin

The bigger the number of components you need to deploy on the same host, the harder it will be to manage all their dependencies to satisfy all their requirements

### 1.1.2. Providing a consistent environment to applications

It would be ideal if applications could run in the exact same environment during development and in production so they have the exact same operating system, libraries, system configuration, networking environment, and everything els

### 1.1.3. Moving to continuous delivery: DevOps and NoOps

- Developers: creating new features and improving the user experience, don’t normally want to be the ones making sure that the underlying operating system is up to date with all the security patches and things like that

- Ops team: care about system security, utilization, and other aspects that aren’t a high priority for developers. The ops people don’t want to deal with the implicit interdependencies of all the application components and don’t want to think about how changes to either the underlying operating system or the infrastructure can affect the operation of the application as a whole, but they must

> Kubernetes enables us to achieve all of this. By abstracting away the actual hardware and exposing it as a single platform for deploying and running apps, it allows developers to configure and deploy their applications without any help from the sysadmins and allows the sysadmins to focus on keeping the underlying infrastructure up and running, while not having to know anything about the actual applications running on top of it

## 1.2. Introducing container technologies

