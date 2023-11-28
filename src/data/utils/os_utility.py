from datetime import date
import os
import re


class FileManager:
    """
        Class 
    """
    def __init__(self, feature, stage, file_handler, date_format: str = "%Y-%m-%d", base_path: str = '../../data'):
        self.feature = feature
        self.stage = stage
        self.file_handler = file_handler
        self.date_format = date_format
        self.base_path = base_path
        self.stage_path = os.path.join(self.base_path, self.stage)
        self.feature_path = self._get_feature_path()

    def _get_feature_path(self) -> str:
        if self.stage == 'raw' or self.stage == 'interim':
            return os.path.join(self.stage_path, self.feature)
        else:
            return self.stage_path
        
    def _create_filename(self, current_date: str):
        return f"{self.feature}_{current_date}{self.file_handler.extension}"
    
    def _create_full_path(self, current_date: str):
        return os.path.join(self.feature_path, self._create_filename(current_date))
    
    def _ensure_directories_exist(self):
        """
            Ensures that the base, stage, and feature directories exist.
            Creates them if they don't.
        """
        os.makedirs(self.base_path, exist_ok=True)
        os.makedirs(self.stage_path, exist_ok=True)
        os.makedirs(self.feature_path, exist_ok=True)

    def file_exists(self, current_date: str) -> bool:
        """
        Check if a file for the given date already exists.
        """
        full_path = self._create_full_path(current_date)
        return os.path.isfile(full_path)

    def write(self, data, current_date: str, **kwargs):
        self._ensure_directories_exist()
        full_path = self._create_full_path(current_date)

        self.file_handler.write(data, full_path, **kwargs)

    def read(self, filename):
        self._ensure_directories_exist()
        path = os.path.join(self.feature_path, filename)
        return self.file_handler.read(path)

    def find_by_date(self, date):
        pass

    def find_date_in_filename(self, filename: str):
        pattern = r"\d{4}-\d{2}-\d{2}"
        match = re.search(pattern, filename)

        if match:
            date_str = match.group()
            # return date.fromisoformat(date_str)
            return date_str
        
    def find_by_feature(self, feature):
        pass

    def show_files(self):
        files = os.listdir(self.feature_path)
        files.sort()
        return files
    
    def show_files_after_date(self, from_date: date):
        files = self.show_files()
        filtered_files = [file for file in files if self.find_date_in_filename(file) >= from_date]
        return filtered_files
    
    def show_range(self, from_date, to_date):
        files = self.show_files()
        filtered_files = [file for file in files 
                          if self.find_date_in_filename(file) >= from_date and 
                          self.find_date_in_filename(file) <= to_date]
        return filtered_files

    def show_last_file(self):
        try:
            return self.show_files()[-1]
        except IndexError:
            return None
    
    def show_last_file_date(self):
        self._ensure_directories_exist()
        filename = self.show_last_file()
        if filename is not None:
            return self.find_date_in_filename(filename)
        return None