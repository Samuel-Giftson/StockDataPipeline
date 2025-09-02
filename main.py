from loguru import logger
from GetMeData import DataGather, Status
from CSVHandler import CSVHandler
import os
from datetime import datetime
import pytz

# Set Eastern Time timezone
ET = pytz.timezone("US/Eastern")

# Configure loguru to log to file with Eastern Time
logger.add(
    "pipeline.log",
    rotation="7 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO"
)

def main():
    # Log the current Eastern Time at the start of every run
    logger.info(f"Current ET time: {datetime.now(ET).strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("Starting stock fetch job...")

    data = DataGather()
    data.fetch_and_update()

    if data.get_status() == Status.SUCCESS:
        logger.info("Data fetch successful.")
        csv_handler = CSVHandler("stock_data.csv")

        if not os.path.exists("stock_data.csv"):
            headers = ["ticker"] + list(next(iter(data.get_information().values())).keys())
            csv_handler.create_file_with_headers(headers)
            logger.info("CSV file created with headers.")

        csv_handler.append_dict_of_dicts(data.get_information())
        logger.info("Data appended to CSV successfully.")
    else:
        logger.error("Data fetch failed. No data written to CSV.")

if __name__ == "__main__":
    main()
