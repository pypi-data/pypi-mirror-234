import os
import sys
import unittest
from pyspark.sql import SparkSession


class SparkETLTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["PYSPARK_PYTHON"] = sys.executable
        os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
        cls.spark = (
            SparkSession.builder.master("local[*]")
            .appName("Unit-tests")
            .getOrCreate()
        )

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()
