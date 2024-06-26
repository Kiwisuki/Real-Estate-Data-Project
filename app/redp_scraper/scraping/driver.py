import logging
import time
import os

import undetected_chromedriver as uc
from retry import retry

LOGGER = logging.getLogger(__name__)
DOCKER_RUN = os.environ.get('DOCKER_RUN', False)
INITIAL_SLEEP = 5
DRIVER_EXECUTABLE_PATH = '/usr/lib/chromium/chromedriver' if DOCKER_RUN else None


class SmartDriver:
    """Driver that resets itself after a certain amount of actions or time passed."""

    def __init__(
        self,
        refresh_rate: int = 10,
        refresh_timer: int = 60,
        wait_to_load: int = 3,
        headless: bool = False,
    ):
        """Initialize the driver with a refresh rate and timer."""
        self.actions = 0
        self.last_refresh = time.time()
        self.refresh_rate = refresh_rate
        self.refresh_timer = refresh_timer
        self.wait_to_load = wait_to_load
        self.headless = headless
        self.initialize_chromedriver()

    def get_options(self):
        """Get the options for the chromedriver."""
        options = uc.ChromeOptions()
        options.add_argument('--start-maximized')
        return options

    def initialize_chromedriver(self):
        """Initialize the chromedriver."""
        self.driver = uc.Chrome(
            options=self.get_options(),
            headless=self.headless,
            use_subprocess=False,
            driver_executable_path=DRIVER_EXECUTABLE_PATH,
        )

    def refresh(self):
        """Refresh the chromedriver."""
        self.driver.quit()
        self.initialize_chromedriver()
        self.last_refresh = time.time()

    def increment(self):
        """Increments the actions and refreshes if needed."""
        self.actions += 1
        if (self.actions % self.refresh_rate == 0) or (
            time.time() - self.last_refresh > self.refresh_timer
        ):
            self.refresh()

    @retry(Exception, tries=3, delay=2, backoff=2, logger=LOGGER)
    def get_html(self, url: str) -> str:
        """Get the html content from the url."""
        self.driver.get(url)
        time.sleep(self.wait_to_load)
        html_content = self.driver.page_source
        self.increment()
        return html_content
