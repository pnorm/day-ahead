import argparse
from datetime import date
import time

from loguru import logger

from utils.date_utility import (
    validate_date_format,
    validate_date_range,
    generate_date_list,
    generate_date_list_n_days_from_today
)
from utils.data_query import (
    PSEDataQuery,
    TGEDataQuery
)
from utils.fetcher import DataFetcher
from utils.file_handler import PickleHandler, CSVHandler
from utils.os_utility import FileManager
from utils.transform import DataProcessor


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''\
    This script fetch historical data from PSE and TGE for the purpose of electricity price prediciton.
        ''')

    # Arguments for historical subparser
    parser.add_argument(
        "-s", "--site", choices=['pse', 'tge'], required=True, dest="site", nargs="?",
        default="pse", type=str, action="store", help="Choose site. PSE - polskie sieci energetyczne, TGE - towarowa giełda energii"    
    )

    # Parse the command-line arguments to get the value of --site
    args, _ = parser.parse_known_args()

    # Based on the value of --site, conditionally add additional arguments
    if args.site == 'pse':
        parser.add_argument('--from_date', type=validate_date_format, dest="from_date", default='2020-01-01', help='Specify the start date')
        parser.add_argument('--to_date', type=validate_date_format, dest="to_date", default=date.today().strftime("%Y-%m-%d"), help='Specify the end date')
        parser.add_argument('--feature', choices=['PL_GEN_WIATR', 'PL_GEN_MOC_JW_EPS'], type=str, dest="feature", default="PL_GEN_WIATR", help='Specify the feature')

    # Parse the command-line arguments
    args = parser.parse_args()

    if args.site == 'pse':
        # if args.feature == 'PL_GEN_WIATR' or:
        raw_file_manager = FileManager(
            feature=args.feature,
            stage="raw",
            file_handler=PickleHandler()
        )

        raw_files = raw_file_manager.show_files()

        interim_file_manager = FileManager(
            feature=args.feature,
            stage="interim",
            file_handler=CSVHandler()
        )

        last_file_date = interim_file_manager.show_last_file_date()

        for file in raw_files:
            current_date = interim_file_manager.find_date_in_filename(file)
            if not interim_file_manager.file_exists(current_date) or current_date == last_file_date:
                data = raw_file_manager.read(filename=file)
                file_date = raw_file_manager.find_date_in_filename(file)
                df = DataProcessor.decode(data)
                if args.feature == 'PL_GEN_WIATR':
                    processed_df = DataProcessor.process_wind(df)
                if args.feature == 'PL_GEN_MOC_JW_EPS':
                    processed_df = DataProcessor.process_power(df)
                interim_file_manager.write(processed_df, file_date)
            

    if args.site == 'tge':
        pass


if __name__ == "__main__":
    main()