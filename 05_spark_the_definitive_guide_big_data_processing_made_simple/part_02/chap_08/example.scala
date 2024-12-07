package spark.chap08

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.expr


object Main {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("chap08-example")
      .master("local")
      .getOrCreate()
    import spark.implicits._ // for using toDF

    // create datasets for examples
    val person = Seq(
      (0, "Bill Chambers", 0, Seq(100)),
      (1, "Matei Zaharia", 1, Seq(500, 250, 100)),
      (2, "Michael Armbrust", 1, Seq(250, 100))
    ).toDF("id", "name", "graduate_program", "spark_status")

    val graduateProgram = Seq(
      (0, "Masters", "School of Information", "UC Berkeley"),
      (2, "Masters", "EECS", "UC Berkeley"),
      (1, "Ph.D.", "EECS", "UC Berkeley")
    ).toDF("id", "degree", "department", "school")

    val sparkStatus = Seq(
      (500, "Vice President"),
      (250, "PMC Member"),
      (100, "Contributor")
    ).toDF("id", "status")

    person.createOrReplaceTempView("person")
    graduateProgram.createOrReplaceTempView("graduateProgram")
    sparkStatus.createOrReplaceTempView("sparkStatus")

    // specify join expression
    val joinExpression = person.col("graduate_program") === graduateProgram.col("id")

    // inner join
    person.join(graduateProgram, joinExpression, joinType = "inner").show(truncate = false)

    // outer join
    person.join(graduateProgram, joinExpression, joinType = "outer").show(truncate = false)

    // left outer join
    person.join(graduateProgram, joinExpression, joinType = "left_outer").show(truncate = false)

    // right outer join
    person.join(graduateProgram, joinExpression, joinType = "right_outer").show(truncate = false)

    // left semi join
    graduateProgram.join(person, joinExpression, joinType = "left_semi").show(truncate = false)
    // left anti join
    graduateProgram.join(person, joinExpression, joinType = "left_anti").show(truncate = false)
    // left anti join
    graduateProgram.join(person, joinExpression, joinType = "left_anti").show(truncate = false)

    // natural join
    spark.sql("SELECT * FROM graduateProgram NATURAL JOIN person").show(truncate = false)

    // cartesian product - cross join
    person.crossJoin(graduateProgram).show(truncate = false)

    // join on complex types
    // Seq (array) in col "spark_status" - person dataFrames
    person.withColumnRenamed("id", "personId") // for not duplicated
      .join(sparkStatus, expr("array_contains(spark_status, id)")).show(truncate = false) // Seq spark_status contain id in sparkStatus

    // handling duplicate column names
    val gradProgramDupe = graduateProgram.withColumnRenamed("id", "graduate_program")
    val joinExpr = gradProgramDupe.col("graduate_program") === person.col("graduate_program")

    // duplicate col, we can not select the duplicate (occur error)
    person.join(gradProgramDupe, joinExpr).show()  // inner join by default

    // approach 1: different join expression
    person.join(gradProgramDupe, "graduate_program").select("graduate_program").show(truncate = false)

    // approach 2: dropping the column after the join
    person.join(gradProgramDupe, joinExpr).drop(person.col("graduate_program"))
      .select("graduate_program").show()

    // approach 3: renaming a column before the join
    val gradProgram = graduateProgram.withColumnRenamed("id", "grad_id")
    val joinExpr1 = person.col("graduate_program") === gradProgram.col("grad_id")
    person.join(gradProgram, joinExpr1).show()
  }
}