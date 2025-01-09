# Chapter 14. Distributed Shared Variables

The second kind of low-level API in Spark is two types of "distributed shared variables"

- Broadcast variables
- Accumulators

Specificially, _accumulators_ let you add together data from all tasks into a shared result (e.g, to implement a counter so you can see how many of your job's input records failed to parse), while _broadcast_ variables let you save a large value on all the worker nodes and reuse it across many Spark actions without re-sending it to the cluster

