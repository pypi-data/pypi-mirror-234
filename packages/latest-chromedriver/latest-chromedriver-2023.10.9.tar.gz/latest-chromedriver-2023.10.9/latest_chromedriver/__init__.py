"""The latest_chromedriver is a module for python scripts in order to
find the correct version of the ChromeDriver depending on Google Chrome version."""

from latest_chromedriver.download_driver import download_only_if_needed
from latest_chromedriver.enviroment import safely_set_chromedriver_path

__version__ = '2023.10.09'
__all__ = ['chrome_info', 'download_driver', 'enviroment']
