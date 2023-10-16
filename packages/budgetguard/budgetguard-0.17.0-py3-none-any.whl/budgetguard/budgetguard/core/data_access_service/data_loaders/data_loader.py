from abc import ABC, abstractmethod
from typing import Dict


class DataLoader(ABC):
    @abstractmethod
    def read(self):
        """
        Base method for loading data.
        """
        raise NotImplementedError()

    @abstractmethod
    def write(self):
        """
        Base method for writing data.
        """
        raise NotImplementedError()

    def build_partition_path(self, partition_config: Dict[str, str]):
        partition_id = ""
        for partition_name, partition_value in partition_config.items():
            partition_id += "{0}={1}/".format(partition_name, partition_value)
        return partition_id[:-1]
