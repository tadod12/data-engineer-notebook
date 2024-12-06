# Chapter 4. YARN

Apache YARN (Yet Another Resource Negotiator) is Hadoop’s cluster resource management system. YARN provides APIs for
requesting and working with cluster resources, but these APIs are not typically used directly by user code. Instead,
users write to higher-level APIs provided by distributed computing frameworks, which themselves are built on YARN and
hide the resource management details from the user.

![yarn application.png](yarn%20application.png)

There is also a layer of application that build on the frameworks shown above. Pig, Hive, and Crunch are all examples of
processing frameworks that run on MapReduce, Spark, or Tez (or on all three), and don't interact with YARN directly.

## Anatomy of a YARN Application Run

YARN provides its core services via two types of long-running daemon: a _resource manager_ (one per cluster) to manage
the use of resources across the cluster, and _node managers_ running on all the nodes in the cluster to launch and
monitor _containers_ (A container executes an application-specific process with a constrained set of resource: memory,
CPU and so on).

![yarn runs application.png](yarn%20runs%20application.png)

- Step 1. To run an application on YARN, a client contacts the resource manager and asks it to run an _application
  master_ process
- Step 2a & 2b. The resource manager finds a node manager that can launch the application master in a container.
  Application master could run a computation in the container it is running in and return the result to the client.
- Step 3. Or it could request more containers from the resource managers.
- Step 4a & 4b. And use them to run a distributed computation.

### Resource Requests

A request for a set of containers can express the amount of computer resources required for each container (memory and
CPU), as well as locality constraints for the containers in that request.

Locality is critical in ensuring that distributed data processing algorithms use the cluster bandwidth efficiently, so
YARN allows an application to specify locality constraints for the containers it is requesting. Locality constraints can
be used to request a container on a specific node or rack, or anywhere on the cluster (off-rack). Sometimes the locality
constraint cannot be met, in which case either no allocation is made or, optionally, the constraint can be loosened.

> A YARN application can make resource requests at any time while it is running.

### Application Lifespan

Categorizing applications in terms of how they map to the jobs that users run:

- One application per user job (Approach **MapReduce** takes)
- One application per workflow or user session of job (**Spark** uses this model). This approach can be more efficient
  than the first, since containers can be reused between jobs, and there is also the potential to cache intermediate
  data between jobs.
- A long-running application that is shared by different users (**Apache Slider**, **Impala**)

### Building YARN Applications

If you are interested in running a directed acyclic graph (DAG) of jobs, then Spark or Tez is appropriate; or for stream
processing, Spark, Samza, or Storm works

## YARN Compared to MapReduce 1

Page 111

- _Scalability_
- _Availability_
- _Utilization_
- _Multitenancy_

## Scheduling in YARN

### Scheduler Options

Three schedulers are available in YARN: The FIFO, Capacity, and Fair Scheduler

![scheduler option.png](scheduler%20option.png)

> Capacity Scheduler Configuration on page 116, Fair Scheduler Configuration on page 118
