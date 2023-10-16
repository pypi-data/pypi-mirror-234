from abc import ABC, abstractmethod


class Pipeline(ABC):
    INPUT_DATA_LOADER = "input_data_loader"
    OUTPUT_DATA_LOADER = "output_data_loader"
    INPUT_DATA_CONFIG = {}

    @abstractmethod
    def run(self):
        """
        Base method for running the pipeline.
        """
        raise NotImplementedError()

    @abstractmethod
    def read_sources(self):
        """
        Base method for reading data from the data sources.
        """
        raise NotImplementedError()

    @abstractmethod
    def write_sources(self):
        """
        Base method for writing data to the data sources.
        """
        raise NotImplementedError()

    @abstractmethod
    def transform(self):
        """
        Base method for transforming the data.
        """
        raise NotImplementedError()
