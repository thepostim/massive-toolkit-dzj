import logging
import os
from pathlib import Path
from typing import Optional
import win32com.client

class MassiveForClient:
    """Main interface class for the Massive for Windows toolkit."""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initializes the MassiveForClient with an optional configuration file.

        Args:
            config_path (Optional[Path]): Path to the configuration file.
        """
        self.config_path = config_path
        self.connection = None
        self.logger = self.setup_logging()

    def setup_logging(self) -> logging.Logger:
        """Sets up the logging configuration.

        Returns:
            logging.Logger: Configured logger.
        """
        logger = logging.getLogger('MassiveForClient')
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler('massive_for_client.log')
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def connect(self) -> bool:
        """Connects to the Massive application.

        Returns:
            bool: True if connection is successful, False otherwise.
        """
        try:
            self.logger.debug("Attempting to connect to the Massive application.")
            self.connection = win32com.client.Dispatch("Massive.Application")
            self.logger.info("Successfully connected to the Massive application.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to connect to the Massive application: {e}")
            return False

    def disconnect(self) -> None:
        """Disconnects from the Massive application."""
        if self.connection:
            self.logger.debug("Disconnecting from the Massive application.")
            self.connection = None
            self.logger.info("Successfully disconnected from the Massive application.")
        else:
            self.logger.warning("No active connection to disconnect.")

    def get_version(self) -> str:
        """Retrieves the version of the Massive application.

        Returns:
            str: The version of the Massive application.
        """
        if self.connection:
            version = self.connection.Version
            self.logger.info(f"Retrieved version: {version}")
            return version
        else:
            self.logger.error("Cannot retrieve version; not connected to the application.")
            return "Not connected"

    def is_installed(self) -> bool:
        """Checks if the Massive application is installed.

        Returns:
            bool: True if installed, False otherwise.
        """
        try:
            installed = win32com.client.Dispatch("Massive.Application")
            self.logger.info("Massive application is installed.")
            return True
        except Exception:
            self.logger.warning("Massive application is not installed.")
            return False

if __name__ == "__main__":
    client = MassiveForClient()
    if client.is_installed():
        if client.connect():
            print(f"Connected to Massive version: {client.get_version()}")
            client.disconnect()
    else:
        print("Massive application is not installed.")
