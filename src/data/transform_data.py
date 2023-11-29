import argparse

from loguru import logger

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
        "-s", "--site", choices=['pse', 'tge', 'external'], required=True, dest="site", nargs="?",
        default="pse", type=str, action="store", help="Choose site. PSE - polskie sieci energetyczne, TGE - towarowa giełda energii"    
    )

    # Parse the command-line arguments to get the value of --site
    args, _ = parser.parse_known_args()

    # Based on the value of --site, conditionally add additional arguments
    if args.site == 'pse':
        parser.add_argument('--feature', choices=['PL_GEN_WIATR', 'PL_GEN_MOC_JW_EPS'], type=str, dest="feature", default="PL_GEN_WIATR", help='Specify the feature')

    # Parse the command-line arguments
    args = parser.parse_args()

    if args.site == 'pse':
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


    if args.site == 'external':
        external_file_manager = FileManager(
            feature="TGE",
            stage="external",
            file_handler=CSVHandler()
        )
        processed_file_manager = FileManager(
            feature="TGE",
            stage="processed",
            file_handler=CSVHandler()
        )
        
        df = external_file_manager.read("day-ahead-prices.csv", index_col='date')
        processed_df = DataProcessor.process_external(df=df)
        logger.debug(f"{processed_df.head()}")
        processed_file_manager.write(processed_df, "fixing.csv")

    if args.site == 'tge':
        feature = "TGE"
        raw_file_manager = FileManager(
            feature=feature,
            stage="raw",
            file_handler=PickleHandler()
        )

        raw_files = raw_file_manager.show_files()

        interim_file_manager = FileManager(
            feature=feature,
            stage="interim",
            file_handler=CSVHandler()
        )

        last_file_date = interim_file_manager.show_last_file_date()

        for file in raw_files:
            current_date = interim_file_manager.find_date_in_filename(file)
            if not interim_file_manager.file_exists(current_date) or current_date == last_file_date:
                data = raw_file_manager.read(filename=file)
                file_date = raw_file_manager.find_date_in_filename(file)
                df = DataProcessor.parse_tge(data)
                processed_df = DataProcessor.process_tge(df, current_date)
                interim_file_manager.write(processed_df, file_date)


if __name__ == "__main__":
    main()