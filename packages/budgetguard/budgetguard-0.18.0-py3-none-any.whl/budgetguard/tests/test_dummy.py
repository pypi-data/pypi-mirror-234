from . import SparkETLTestCase
import pyspark.sql.types as T


class TestDummy(SparkETLTestCase):
    def test_base(self):
        input_schema = T.StructType(
            [
                T.StructField("StoreID", T.IntegerType(), True),
                T.StructField("Location", T.StringType(), True),
                T.StructField("Date", T.StringType(), True),
                T.StructField("ItemCount", T.IntegerType(), True),
            ]
        )
        input_data = [
            (1, "Bangalore", "2021-12-01", 5),
            (2, "Bangalore", "2021-12-01", 3),
            (5, "Amsterdam", "2021-12-02", 10),
            (6, "Amsterdam", "2021-12-01", 1),
            (8, "Warsaw", "2021-12-02", 15),
            (7, "Warsaw", "2021-12-01", 99),
        ]
        input_df = self.spark.createDataFrame(
            data=input_data, schema=input_schema
        )
        input_df.collect()
