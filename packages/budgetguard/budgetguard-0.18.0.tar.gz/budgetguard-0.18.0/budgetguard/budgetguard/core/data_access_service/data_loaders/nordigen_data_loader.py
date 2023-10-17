from .data_loader import DataLoader
from ..data_connections import connect, NordigenConnection
from loguru import logger
from datetime import datetime
from tqdm import tqdm


class NordigenDataLoader(DataLoader):
    NAME = "nordigen"

    def __init__(self):
        """
        Constructor for NordigenDataLoader class.
        """
        self.nordigen_connection: NordigenConnection = connect(self.NAME)
        self.accounts = self.nordigen_connection.accounts

    def read(self, partition_id: str = None):
        """
        Method for reading data from the Nordigen API.
        """
        logger.info("Reading data from Nordigen...")
        output = {}
        partition_id = self._format_partition_id_for_transactions(partition_id)
        pbar = tqdm(self.accounts, desc="Reading accounts data...")
        for account in pbar:
            meta_data = account.get_metadata()
            pbar.set_description(
                "Reading data for account {0}...".format(meta_data["id"])
            )
            details = account.get_details()
            balances = account.get_balances()
            transactions = account.get_transactions(
                date_from=partition_id, date_to=partition_id
            )
            output[meta_data["id"]] = {
                "details": details,
                "balances": balances,
                "transactions": transactions,
                "metadata": meta_data,
            }
        logger.info("Finished reading {0} accounts data!".format(len(output)))
        return output

    def write(self):
        """
        Method for writing data to the Nordigen API.
        """
        raise NotImplementedError(
            "Nordigen data loader doesn't support writing data."
        )

    def _format_partition_id_for_transactions(
        self, partition_id: str = None
    ) -> str:
        """
        Method for formatting the partition id for transactions.
        """
        if partition_id:
            return datetime.strptime(partition_id, "%Y%m%d").strftime(
                "%Y-%m-%d"
            )
        else:
            return partition_id
