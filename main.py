import yaml
import sys
from data_importer.api_client import APIClient
from data_importer.db import Database
from data_importer.logger import get_logger

# Print Python path to ensure the script can find the data_importer package
print("Python path:", sys.path)

logger = get_logger()

def main():
    try:
        # Load configuration
        with open("config/config.yaml", "r") as file:
            config = yaml.safe_load(file)

        # Validate configuration
        if not config.get("api_url") or not config.get("database_url"):
            raise ValueError("Invalid configuration: 'api_url' or 'database_url' is missing.")

        # Initialize API Client and Database
        api_client = APIClient(config["api_url"])
        db = Database(config["database_url"])

        # Create table if not exists
        logger.info("Creating table if it doesn't exist...")
        db.create_table()

        # Fetch data from API
        logger.info("Fetching data from API...")
        mobile_data = api_client.fetch_mobile_data()
        if not mobile_data:
            logger.warning("No data fetched from the API.")
            return

        # Insert data into database
        logger.info("Inserting data into the database...")
        for item in mobile_data:
            phone_id = item.get("id")
            phone_name = item.get("name")
            phone_data = item.get("data")

            if phone_id and phone_name and phone_data:
                db.insert_phone_data(phone_id, phone_name, phone_data)
                logger.info(f"Inserted phone data: {phone_id}")
            else:
                logger.warning(f"Skipping invalid record: {item}")

        logger.info("Data import completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
