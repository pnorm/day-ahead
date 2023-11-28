from abc import ABC, abstractmethod
import pickle

from loguru import logger


class FileHandler(ABC):
    @abstractmethod
    def write(self, data, path):
        pass

    @abstractmethod
    def read(self):
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

    def read(self):
        pass


class CSVHandler(FileHandler):
    @property
    def extension(self):
        return ".csv"

    def write(self, data):
        pass

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