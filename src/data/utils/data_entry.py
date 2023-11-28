from abc import ABC, abstractmethod


class DataEntry(ABC):
    """
        Abstract class for storing data from different sources.
    """
    def __init__(self, data, handler):
        self.data = data
        self.handler = handler

    @abstractmethod
    def decode(self):
        pass

    
    def parse(delf):
        pass


class PSEDataEntry(DataEntry):
    """
        Class for storing data from pse.pl
    """
    pass


class TGEDataEntry(DataEntry):
    """
        Class for storing data 
    """
    pass