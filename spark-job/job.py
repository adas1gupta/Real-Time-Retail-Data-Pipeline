from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, expr
from pyspark.sql.types import StructType,StructField,StringType,IntegerType,DoubleType,TimestampType
import os

spark = (
    SparkSession.builder.appName("RetailIngest")
    .master(os.getenv("SPARK_MASTER","local[*]"))
    .getOrCreate()
)

schema = StructType([
    StructField("InvoiceNo", IntegerType()),
    StructField("StockCode", StringType()),
    StructField("Description", StringType()),
    StructField("Quantity", IntegerType()),
    StructField("InvoiceDate", TimestampType()),
    StructField("UnitPrice", DoubleType()),
    StructField("CustomerID", IntegerType()),
    StructField("Country", StringType()),
])

kafka_df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", os.getenv("KAFKA_BOOTSTRAP_SERVERS"))
    .option("subscribe", "ingestion-topic")
    .option("startingOffsets", "latest")
    .load()
)

json_df = kafka_df.selectExpr("CAST(value AS STRING) as json")
parsed = json_df.select(from_json(col("json"), schema).alias("data")).select("data.*")

processed = parsed.withColumn("total_price", col("Quantity") * col("UnitPrice"))

pg_url = os.getenv("DATABASE_URL").replace("jdbc:", "")  # spark expects pure jdbc string below

query = (
    processed.writeStream.outputMode("append")
    .foreachBatch(lambda df, _: df.write.format("jdbc")
                  .option("url", os.getenv("DATABASE_URL"))
                  .option("dbtable", "invoices")
                  .option("driver", "org.postgresql.Driver")
                  .mode("append").save())
    .start()
)

query.awaitTermination()