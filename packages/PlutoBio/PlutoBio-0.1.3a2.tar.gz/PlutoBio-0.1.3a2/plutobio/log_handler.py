import logging

# Configure the logging module
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

download_upload_logger = logging.getLogger("Download Upload Logger")
