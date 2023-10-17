import sys
import os
import json

here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, ".."))

from .pipeline import Pipeline  # noqa: E402
from datalake import Datalake  # noqa: E402
from core.data_access_service.data_loaders import (  # noqa: E402
    create_data_loader,
)
from loguru import logger  # noqa: E402


class IngestAccountData(Pipeline):
    INPUT_DATA_LOADER = "nordigen"
    OUTPUT_DATA_LOADER = "s3"
    OUTPUT_LAYER = "ingest"
    OUTPUT_TABLES_KEYS = ["balances", "transactions", "details", "metadata"]

    def __init__(self, partition_id: str) -> None:
        self.datalake = Datalake()
        self.partition_id = partition_id
        self.input_loader = create_data_loader(self.INPUT_DATA_LOADER)
        self.output_loader = create_data_loader(self.OUTPUT_DATA_LOADER)

    def read_sources(self):
        """
        Reads the data from the data sources.
        """
        nordigen_raw_data = self.input_loader.read(self.partition_id)
        return nordigen_raw_data

    def write_sources(self, nordigen_data):
        """
        Writes the data to the data sources.
        """
        account_ids = list(nordigen_data.keys())
        for key in self.OUTPUT_TABLES_KEYS:
            datalake_config = self.datalake[self.OUTPUT_LAYER][key]
            for account_id in account_ids:
                partition_config = {
                    "partition_id": self.partition_id,
                    "account_id": account_id,
                }
                data = nordigen_data[account_id][key]
                self.output_loader.write(
                    json.dumps(data), datalake_config, partition_config
                )

    def transform(self):
        """
        Transforms the data.
        """
        raise NotImplementedError(
            "Transform method not needed for ingestion pipeline!"
        )

    def run(self):
        """
        Runs the pipeline.
        """
        logger.info("Running the ingestion pipeline...")
        nordigen_raw_data = self.read_sources()
        logger.info("Writing the data to the datalake...")
        self.write_sources(nordigen_raw_data)
        logger.info("Finished running the ingestion pipeline!")
