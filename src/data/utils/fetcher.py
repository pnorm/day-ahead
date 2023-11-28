from loguru import logger
import requests
import time
from typing import Type

from .data_query import BaseDataQuery


class DataFetcher:
    def __init__(self, query: Type[BaseDataQuery], max_retries: int = 5, timeout: int = 300, delay: int = 60) -> None:
      self.query = query
      self.max_retries = max_retries
      self.timeout = timeout
      self.delay = delay

    def fetch_data(self):
        """
            Get response.content from external server with retry mechanism for any exception.
        """
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                response = requests.get(self.query.complete_url, timeout=self.timeout)
                response.raise_for_status()
                
                if response.status_code == 200:
                    logger.debug(f"Data successfully fetched. Date: {self.query.current_date}, Url: {self.query.complete_url}.")
                    logger.debug(f"Length of data fetched {len(response.content)}")
                    return response.content
                else:
                    logger.warning(f"Unexpected status code {response.status_code} for URL: {self.complete_url}")
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")
            
            # Increment the retry count and wait for some time before retrying
            retry_count += 1
            if retry_count < self.max_retries:
                logger.debug(f"Retrying ({retry_count}/{self.max_retries}) after a {self.delay} seconds delay...")
                time.sleep(60)

        logger.error(f"Failed to fetch data after {self.max_retries} retries. URL: {self.complete_url}")


    def fetch_historical_data(self):
        """
            Utility for fetching raw data.
        """
        data = self.fetch_data()
        if data is not None:
            return data
        else:
            logger.error("Unable to retrieve data. :(")