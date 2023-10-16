from pyspark.sql import SparkSession
from pyspark.sql import Row

# Create a Spark session
spark = SparkSession.builder.appName("PySparkTest").getOrCreate()

# Define data as a list of lists
data = [
    [1, "Alice", 28, 50000],
    [2, "Bob", 35, 60000],
    [3, "Charlie", 22, 45000],
    [4, "David", 29, 55000],
    [5, "Eve", 31, 70000],
]

# Convert the list of lists to a list of Row objects
rows = [Row(id=row[0], name=row[1], age=row[2], salary=row[3]) for row in data]

# Create a DataFrame from the list of Row objects
df = spark.createDataFrame(rows)

# Show the schema of the DataFrame
df.printSchema()

# Show the content of the DataFrame
df.show()

# Perform some basic operations
num_rows = df.count()
avg_salary = df.selectExpr("avg(salary)").collect()[0][0]

print(f"Number of rows: {num_rows}")
print(f"Average salary: {avg_salary}")

# Stop the Spark session
spark.stop()
