import argparse

from loguru import logger
import pandas as pd

from utils.file_handler import CSVHandler
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
        interim_file_manager = FileManager(
            feature=args.feature,
            stage="interim",
            file_handler=CSVHandler()
        )

        files = interim_file_manager.show_files()

        dfs = []

        for file in files:
            df = interim_file_manager.read(file)
            dfs.append(df)

        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df.fillna(0.0, inplace=True)

        logger.debug(f"combined df shape: {combined_df.shape}")

        processed_file_manager = FileManager(
            feature=args.feature,
            stage="processed",
            file_handler=CSVHandler()
        )

        processed_file_manager.write(combined_df, f"{args.feature}.csv".lower(), index=False)

    if args.site == 'tge':
        feature="TGE"
        interim_file_manager = FileManager(
            feature="TGE",
            stage="interim",
            file_handler=CSVHandler()
        )

        files = interim_file_manager.show_files()

        processed_file_manager = FileManager(
            feature="TGE",
            stage="processed",
            file_handler=CSVHandler()
        )

        historical_fixing = processed_file_manager.read("fixing.csv", index_col='date')

        # Initialize a list to store all dataframes including the historical one
        all_dataframes = [historical_fixing]

        # Loop through the list of files and read each dataframe
        for file in files:
            df = interim_file_manager.read(file, index_col='date')
            all_dataframes.append(df)

        # Concatenate all dataframes
        concatenated_df = pd.concat(all_dataframes)

        # Remove duplicate dates, keep the last (most recent) entry
        updated_df = concatenated_df[~concatenated_df.index.duplicated(keep='last')].copy()

        # Sort the data by date (index)
        updated_df.sort_index(inplace=True)

        processed_file_manager.write(updated_df, "fixing.csv")



if __name__ == "__main__":
    main()