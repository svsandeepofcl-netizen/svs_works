import sys
import argparse
from naukri_updater import NaukriUpdater
from logger import setup_logger

logger = setup_logger("Main")


def main():
    parser = argparse.ArgumentParser(description="Headless Naukri Profile Updater")
    parser.add_argument(
        "--headful",
        action="store_true",
        help="Run browser in headful (visible) mode for debugging.",
    )
    args = parser.parse_args()

    # Headless by default as requested
    headless = not args.headful

    logger.info("Initializing Naukri Profile Updater...")
    updater = NaukriUpdater(headless=headless)
    result = updater.run()

    if result["success"]:
        logger.info(f"SUCCESS: {result['message']}")
        sys.exit(0)
    else:
        logger.error(f"FAILURE: {result['message']}")
        sys.exit(1)


if __name__ == "__main__":
    main()

