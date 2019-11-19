import getpass
import logging
from ruamel.yaml import YAML
from datetime import datetime


def main():
    # Load configuration file
    yaml = YAML(typ='safe')
    settings = yaml.load(open("../config/settings.yml"))

    # Setup basic logging
    logging.basicConfig(filename="../log/script.log", filemode="a", level=logging.INFO,
                        format=str(datetime.now()) + " - %(levelname)s - %(message)s")

    # Get connection info
    if settings.get("connection"):
        api_key = settings.get("connection").get("api_key")
        region = settings.get("connection").get("region", "us")
    else:
        api_key = None
        region = "us"

    # Prompt user for API key if there isn't one configured
    if api_key is None:
        api_key = getpass.getpass("Please enter your InsightAppSec API key:")

    logging.info(f'Region: {region}')


main()
