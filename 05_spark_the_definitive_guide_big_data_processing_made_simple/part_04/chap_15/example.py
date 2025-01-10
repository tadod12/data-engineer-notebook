from pyspark.sql import SparkSession

if __name__ == "__main__":
    spark = SparkSession.builder \
        .master("local") \
        .appName("Example") \
        .getOrCreate()

    #  Stage 1
    df1 = spark.range(2, 10000000, 2)

    #  Stage 2
    df2 = spark.range(2, 10000000, 4)

    #  Stage 3
    step1 = df1.repartition(5)

    #  Stage 4
    step12 = df2.repartition(6)

    #  Stage 5
    step2 = step1.selectExpr("id * 5 as id")
    step3 = step2.join(step12, ["id"])
    step4 = step3.selectExpr("sum(id)")

    # Stage 6
    step4.collect()

    step4.explain()
    spark.stop()

# pip install pyspark==3.1.2
