# Chapter 2. MapReduce

## A weather Dataset

### Data Format

The data we will use is from the **National Climatic Data Center**, or NCDC. The data is stored using a line-oriented
ASCII format, in which each line is a record.

For simplicity, we focus on the basic elements, such as temperature, which are always present and are of fixed width.

## Analyzing the Data with Unix Tools

Script to calculate the maximum temperature for each year (42 mins to run all lines and files)

    #! /usr/bin/env bash
    for year in all/*
    do
        echo -ne `basename $year .gz`"\t"
        gunzip -c $year | \
            awk '{  temp = substr($0, 88, 5) + 0;  # temperature, add 0 to turn into integer
                    q = substr($0, 93, 1);  # quality
                    if (temp != 9999 && q ~ /[01459]/ && temp > max) max = temp }
                END { print max }'
    done

To speed up the processing, we need to run parts of the program in parallel. In theory: process different years in
different processes, using all the available hardware threads on a machine. There are a few problems with this:

- Diving the work into equal-size pieces isn't easy. In this case, the file size for different years varies widely, so
  some processes will finish much faster than others. Better approach: Split the input into fixed-size chunks and assign
  each chunk to a process.

- Combining the results from independent processes may require further processing. If using the fixed-size chunk
  approach, the combination is more delicate. For this example, data for a particular year will typically be split into
  several chunks, each processed independently. We'll end up with the maximum temperature for each chunk, so the final
  step is to look for the highest of these maximums for each year.

- You are limited by the processing capacity of a single machine.

Although it's feasible to parallelize the processing, in practice it's messy. Using a framework like Hadoop to take care
of these issues is a great help.

## Analyzing the Data with Hadoop

### Map and Reduce

MapReduce works by breaking the processing into two phases:

- The map phase
- The reduce phase

Each phase has key-value pairs as input and output, the types of which may be chosen by the programmer.

#### Map Phase

The input to our map phase is the raw NCDC data. We choose a text input format that gives us each line in the dataset as
a text value. The key is the offset of the beginning of the line from the beginning of the file, but as we have no need
for this, we ignore it.

Map function: Pull out the year and the air temperature. In this case, the map function is just a data preparation
phase, setting up the data for the reduce function to find the maximum temperature for each year. (drop bad records too)

Sample lines of input data:

    0067011990999991950051507004...9999999N9+00001+99999999999...
    0043011990999991950051512004...9999999N9+00221+99999999999...
    0043011990999991950051518004...9999999N9-00111+99999999999...
    0043012650999991949032412004...0500001N9+01111+99999999999...
    0043012650999991949032418004...0500001N9+00781+99999999999...

As key-value pairs: (the keys are the line offset within the file)

    (0, 0067011990999991950051507004...9999999N9+00001+99999999999...)
    (106, 0043011990999991950051512004...9999999N9+00221+99999999999...)
    (212, 0043011990999991950051518004...9999999N9-00111+99999999999...)
    (318, 0043012650999991949032412004...0500001N9+01111+99999999999...)
    (424, 0043012650999991949032418004...0500001N9+00781+99999999999...)

THe map function merely extracts the year and the air temperature:

    (1950, 0)
    (1950, 22)
    (1950, -11)
    (1959, 111)
    (1949, 78)

The output from the map function is processed by the MapReduce framework before being sent to the reduce function. This
processing sorts and groups the key-value pairs by key. So, our reduce function sees the following input:

    (1949, [111, 78])
    (1950, [0, 22, -11])

All the reduce function has to do is iterate through the list and pick up the maximum reading

    (1949, 111)
    (1950, 22)

![MapReduce logical data flow.png](MapReduce%20logical%20data%20flow.png)

A `Job` object forms the specification of the job and gives you control over how the job is run. When we run this job on
a Hadoop cluster, we will package the code into a JAR file (which Hadoop will distribute around the cluster)

## Scaling Out

To scale out, we need to store the data in a distributed filesystem (typically HDFS). This allows Hadoop to move the
MapReduce computation to each machine hosting a part of the data, using Hadoop's resource management system, call YARN.

### Data Flow

A MapReduce job is a unit of work that the client wants to be performed: it consists of the input data, the MapReduce
program, and configuration information. Hadoop runs the job by dividing it into _tasks_, of which there are two types:
_map tasks_ and _reduce tasks_. The tasks are scheduled using YARN and run on nodes in the cluster. If a task fails, it
will be automatically rescheduled to run on a different node.

Hadoop divides the input to a MapReduce job into fixed-size pieces called _input splits_ (or _splits_). Hadoop creates
one map task for each split, which runs the user-defined map function for each _record_ in the split.

For most jobs, a good split size tends to be the size of an HDFS block, which is 128 MB by default (this can be changed
for the cluster or specified when eah file is created).

_The data locality_: Hadoop does it best to run the map task on a node where the input data resides in HDFS (cuz it
doesn't use valuable cluster bandwidth). Sometimes, however, all the nodes hosting the HDFS block replicas for a map
task's input split are running other map tasks, so the job scheduler will look for a free map slot on a node in the same
rack as one of the blocks.

Map tasks write their output to the local disk, not to HDFS because map output is intermediate output: it's processed by
reduce tasks to produce the final output, and once the job is complete, the map output can be thrown away.

> If the node running the map task fails before the map output has been consumed by the reduce task, then Hadoop will
> automatically rerun the map task on another node to re-create the map output

![rack map task.png](rack%20map%20task.png)
Data local (a), rack-local (b), off-rack (c)

Reduce tasks don’t have the advantage of data locality; the input to a single reduce task is normally the output from
all mappers. The sorted map outputs have to be transferred across the network to the node where the reduce task is
running, where they are merged and then passed to the user-defined reduce function.

> For each HDFS block of the reduce output, the first replica is stored on the local node, with other replicas being
> stored on off-rack nodes for reliability

![dataflow single reduce task.png](dataflow%20single%20reduce%20task.png)

When there are multiple reducers, the map tasks partition their output, each creating one partition for each reduce task
There can be many keys (and their associated values) in each partition, but the records for any given key are all in a
single partition. The partitioning can be controlled by a user-defined partitioning function, but normally the default
partitioner—which buckets keys using a hash function—works very well.

![dataflow multiple reduce task.png](dataflow%20multiple%20reduce%20task.png)

### Combiner Functions

Many MapReduce jobs are limited by the bandwidth available on the cluster, so it pays to minimize the data transferred
between map and reduce tasks. The _combiner function_ is an optimization, runs on the map output to form the input to
the reduce function.

Suppose that for the maximum temperature example, readings for the year 1950 were processed by two maps (because they
were in different splits). Imagine the first map produced the output:

    (1950, 0)
    (1950, 20)
    (1950, 10)

and the second produced:

    (1950, 25)
    (1950, 15)

The reduce function would be called with a list of all the values:

    (1950, [0, 20, 10, 25, 15])

with output:

    (1950, 25)

since 25 is the maximum value in the list. We could use a combiner function that, just like the reduce function, finds
the maximum temperature for each map output. The reduce function would then be called with:

    (1950, [20, 25])

    max(0, 20, 10, 25, 15) = max(max(0, 20, 10), max(25, 15)) = max(20, 25) = 25

> The combiner function doesn’t replace the reduce function. But it can help cut down the amount of data shuffled
> between the mappers and the reducers