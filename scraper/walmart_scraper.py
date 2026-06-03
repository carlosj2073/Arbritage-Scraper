from logger import get_logger
import logging
from playwright.sync_api import sync_playwright

class WalmartScraper:

    website = "Walmart"

    def __init__(self, url: str, logger: logging.Logger) -> None:
        self.url = url
        self.logger = logger  
        self.browser = None
        self.page = None
        self.playwright = None

    def launch(self) -> None:
        self.logger.info(f"Initiating playwright and launching {self.website}.com")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()
        self.page.goto(self.url)
        self.logger.info(f"Launched browser and navigated to {self.url}")
    