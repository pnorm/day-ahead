from abc import ABC, abstractmethod
import pickle

from loguru import logger


class FileHandler(ABC):
    @abstractmethod
    def write(self, data, path):
        pass

    @abstractmethod
    def read(self, path):
        pass

    @property
    @abstractmethod
    def extension(self):
        pass


class PickleHandler(FileHandler):
    @property
    def extension(self):
        return ".pkl"

    def write(self, data, path):
        try:
            with open(path, "wb") as file:
                pickle.dump(data, file)
                logger.debug(f"Data pickled to the file {path}")
        except Exception as e:
            logger.debug(f"Error creating file {path}: {e}")

    def read(self, path):
        with open(path, 'rb') as file:
            data = pickle.load(file)
            logger.debug(f"File: {path} successfully opened.")
        return data


class CSVHandler(FileHandler):
    @property
    def extension(self):
        return ".csv"

    def write(self, data, path, **kwargs):
        data.to_csv(path, **kwargs)
        logger.debug(f"Data successfully saved to {path}")

    def read(self):
        pass


class JSONHandler(FileHandler):
    @property
    def extension(self):
        return ".json"
    
    def write(self, data):
        pass

    def read(self):
        pass