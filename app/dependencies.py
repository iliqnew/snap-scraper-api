from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from typing import List, Dict, AsyncGenerator
from uuid import uuid4


from .database import get_db


from .schemas import Screenshot, SeleniumScreenshotScraperCreate


class SeleniumScreenshotScraper(SeleniumScreenshotScraperCreate):
    start_url: str
    max_urls: int

    async def scrape(self) -> AsyncGenerator[Screenshot, None]:
        scrape_id = str(uuid4())

        # setup the driver
        driver_options = webdriver.FirefoxOptions()
        driver_options.add_argument("--headless")
        driver = webdriver.Firefox(options=driver_options)

        # save screenshot
        yield self.__process_url(driver, scrape_id, self.start_url)

        # extract links
        child_urls = self.__get_first_n_links(driver, self.max_urls)

        # screenshot child urls
        for child_url in child_urls:
            yield self.__process_url(driver, scrape_id, child_url)

        # get rid of the driver properly
        driver.quit()

    def __process_url(self, driver: WebDriver, scrape_id: str, url: str):
        # visit the url
        driver.get(url)
        self.__maximize_window(driver)
        screenshot = driver.find_element(By.TAG_NAME, "body")

        # save screenshot and return it
        return self.__save_screenshot(scrape_id, url, screenshot)

    def __maximize_window(self, driver: WebDriver) -> None:
        driver.set_window_size(
            1920, driver.execute_script("return document.body.scrollHeight")
        )

    @staticmethod
    def __get_first_n_links(driver: WebDriver, n: int) -> List[str]:
        return list(
            {
                e.get_attribute("href")
                for e in driver.find_elements(By.TAG_NAME, "a")
                if e.get_attribute("href") is not None
            }
        )[:n]

    @staticmethod
    def __save_screenshot(
        scrape_id: str, url: str, screenshot: WebElement
    ) -> Dict[str, str]:
        file_name = f"{scrape_id}-{url.split('://')[-1].replace('/', '__')}.png"
        screenshot_path = f"data/{file_name}"
        screenshot.screenshot(screenshot_path)

        return Screenshot(name=file_name, path=screenshot_path, scrape_id=scrape_id)
