# Chapter 1 - Introduction to High Performance Spark

## What is Spark and Why Performance Matters

Uniquely, Spark allows us to write the logic of data transformations and machine learning algorithms in a way that is parallelizable, but relatively system agnostic

Some techniques can work well on certain data sizes or even certain key distributions, but not all. The simplest example of this can be how for many problems, using groupByKey in Spark can very easily cause the dreaded out-of-memory exceptions, but for data with few duplicates this operation can be just as quick as the alternatives that we will present

Learning to understand your particular use case and system and how Spark will interact with it is a must to solve the most complex data science problems with Spark

## What You Can Expect to Get from This Book

Make your Spark queries
- Run faster
- Able to handle larger data sizes
- Use fewer resources

> The structure of this book is intentional and reading  the sections in order should give you not only a few scattered tips, but a comprehensive understanding of Apache Spark and how to make it sing

## Why Scala?

It is the belief of the authors that “serious” performant Spark development is most easily achieved in Scala

### To Be a Spark Expert You Have to Learn a Little Scala Anyway

The methods in the _Resilient Distributed Datasets_ (RDD) class closely mimic those in the Scala collections API. RDD functions, such as `map`, `filter`, `flatMap`, `reduce`, and `fold`, have nearly identical specifications to their Scala equivalents

### The Spark Scala API Is Easier to Use Than the Java API

- Writing Spark in Scala is significantly more concise than writing Spark in Java since Spark relies heavily on inline function definitions and lambda expressions, which are much more naturally supported in Scala (especially before Java 8)
- The Spark shell can be a powerful tool for debugging and development, and is only available in languages with existing REPLs (Scala, Python, and R)

### Scala Is More Performant Than Python

Spark code written in Python is often slower than equivalent code written in the JVM, since Scala is statically typed, and the cost of JVM communication (from Python to Scala) can be very high

### Why Not Scala?

- Developer/team reference

### Learning Scala

For books: Programming Scala, 2nd Edition, by Dean Wampler and Alex Payne

## Conclusion

Working in Spark does not require a knowledge of Scala