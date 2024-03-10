import logging
import time

import undetected_chromedriver as uc
from retry import retry

from settings import CHROMEDRIVER_PATH

LOGGER = logging.getLogger(__name__)


class SmartDriver:
    """Driver that resets itself after a certain amount of actions or time passed."""

    def __init__(
        self, refresh_rate: int = 10, refresh_timer: int = 60, headless: bool = True
    ):
        """Initialize the driver with a refresh rate and timer."""
        self.actions = 0
        self.last_refresh = time.time()
        self.refresh_rate = refresh_rate
        self.refresh_timer = refresh_timer
        self.headless = headless
        self.driver = self.initialize_chromedriver()

    def get_options(self):
        """Get the options for the chromedriver."""
        options = uc.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--incognito')
        if self.headless:
            options.add_argument('--headless')
        return options

    def initialize_chromedriver(self):
        """Initialize the chromedriver."""
        self.last_refresh = time.time()
        return uc.Chrome(options=self.get_options(), executable_path=CHROMEDRIVER_PATH)

    def refresh(self):
        """Refresh the chromedriver."""
        self.driver.quit()
        self.driver = self.initialize_chromedriver()

    def increment(self):
        """Increments the actions and refreshes if needed."""
        self.actions += 1
        if (self.actions % self.refresh_rate == 0) or (
            time.time() - self.last_refresh > self.refresh_timer
        ):
            self.refresh()

    @retry(Exception, tries=3, delay=2, backoff=2, logger=LOGGER)
    def get_html(self, url: str, delay: int = 2) -> str:
        """Get the html content from the url."""
        self.driver.get(url)
        html_content = self.driver.page_source
        self.increment()
        return html_content
