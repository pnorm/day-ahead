import argparse
from datetime import date

from loguru import logger

from utils.date_utility import (
    validate_date_format,
    validate_date_range
)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''\
    This script fetch historical data from PSE and TGE for the purpose of electricity price prediciton.
        ''')
    
    # Subparsers are invoked based on the value of the first positional argument
    subparser = parser.add_subparsers(dest="command")

    # Positional arguments
    historical = subparser.add_parser(
        'historical',
        help='get historical data for a given site (pse or tge)'
    )

    # For backfills it looks only on most recent date in 'data/raw' and updates the data accordingly
    # If necessary we can implement more advanced backfilling mechanism, e.g.
    # https://dagster.io/blog/backfills-in-ml
    backfill = subparser.add_parser(
        'backfill',
        help="update data for a given site (pse or tge)"
    )

    # historical/backfill option triggers the appropriate subparser

    # Arguments for historical subparser
    historical.add_argument(
        "-s", "--site", choices=['pse', 'tge'], required=True, dest="site", nargs="?",
        default="pse", type=str, action="store", help="Choose site. PSE - polskie sieci energetyczne, TGE - towarowa giełda energii"    
    )

    # Parse the command-line arguments to get the value of --site
    args, _ = historical.parse_known_args()

    # Based on the value of --site, conditionally add additional arguments
    if args.site == 'pse':
        historical.add_argument('--from_date', type=validate_date_format, dest="from_date", default='2020-01-01', help='Specify the start date')
        historical.add_argument('--to_date', type=validate_date_format, dest="to_date", default=date.today().strftime("%Y-%m-%d"), help='Specify the end date')
        historical.add_argument('--feature', choices=['PL_GEN_WIATR', 'PL_GEN_MOC_JW_EPS'], type=str, dest="feature", default="PL_GEN_WIATR", help='Specify the feature')

    # Arguments for backfill subparser
    backfill.add_argument(
        "-s", "--site", choices=['pse', 'tge'], required=True, dest="site", nargs="?",
        default="pse", type=str, action="store", help="Choose site. PSE - polskie sieci energetyczne, TGE - towarowa giełda energii"  
    )

    args, _ = backfill.parse_known_args()

    if args.site == 'pse':
        backfill.add_argument('--feature', choices=['PL_GEN_WIATR', 'PL_GEN_MOC_JW_EPS'], type=str, dest="feature", default="PL_GEN_WIATR", help='Specify the feature')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Use args.command to determine which subcommand was invoked
    if args.command == 'historical':
        logger.debug("Historical data command selected")

        if args.site == 'pse':
            logger.debug(f"Historical subcommand invoked for site: {args.site}, feature: {args.feature} and date from {args.from_date} to {args.to_date}")

        if args.site == 'tge':
            logger.debug(f"Historical subcommand invoked for site: {args.site}")

    elif args.command == 'backfill':
        logger.debug("Backfill command selected")

        if args.site == 'pse':
            logger.debug(f"Backfill subcommand invoked for site: {args.site} and feature: {args.feature}")

        if args.site == 'tge':
            feature = 'TGE'
            logger.debug(f"Backfill subcommand invoked for site: {args.site} and feature: {feature}")


if __name__ == "__main__":
    main()