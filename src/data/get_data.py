import argparse
from datetime import date

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
from utils.file_handler import PickleHandler
from utils.os_utility import FileManager


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
        logger.debug(f"Historical subcommand invoked for site: {args.site}, feature: {args.feature} and date from {args.from_date} to {args.to_date}")
        
        file_manager = FileManager(
            feature=args.feature,
            stage="raw",
            file_handler=PickleHandler(),
        )
        date_list = generate_date_list(from_date=args.from_date, to_date=args.to_date)
        
        last_file_date = file_manager.show_last_file_date()

        for current_date in date_list:
            if not file_manager.file_exists(current_date) or current_date == last_file_date:
                query = PSEDataQuery(current_date=current_date, feature=args.feature)
                fetcher = DataFetcher(query=query)
                data = fetcher.fetch_historical_data()
                file_manager.write(data, current_date)
            else:
                logger.debug(f"Data for {current_date} already exists, skipping fetch.")
            

    if args.site == 'tge':
        logger.debug(f"Historical subcommand invoked for site: {args.site}")

        file_manager = FileManager(
            feature="TGE",
            stage="raw",
            file_handler=PickleHandler(),
        )
        date_list = generate_date_list_n_days_from_today(day_lag=60)
        last_file_date = file_manager.show_last_file_date()

        for current_date in date_list:
            if not file_manager.file_exists(current_date) or current_date == last_file_date:
                query = TGEDataQuery(current_date=current_date)
                fetcher = DataFetcher(query=query)
                data = fetcher.fetch_historical_data()
                file_manager.write(data, current_date)
            else:
                logger.debug(f"Data for {current_date} already exists, skipping fetch.")


if __name__ == "__main__":
    main()