import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def remove_prefix(s, p):
    return s[s.startswith(p) and len(p) :]


class ShipmentsSpider(scrapy.Spider):
    name = "shipments"
    start_urls = ["https://www.msc.com/track-a-shipment"]

    def __init__(self, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        chrome_options = chrome.options.Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.number = number

    def number_response(self, response):
        self.driver.get(response.url)
        country_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.CSS_SELECTOR, ".modalButtonPanel > .button-primary")
            )
        )
        country_button.click()
        number_input = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.CSS_SELECTOR, ".search-input input")
            )
        )
        number_input.send_keys(self.number)
        search_button = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.CSS_SELECTOR, ".search-button > a")
            )
        )
        self.driver.execute_script("arguments[0].click()", search_button)
        WebDriverWait(self.driver, 10).until(
            lambda _: "link" in self.driver.current_url
        )
        _ = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(
                (By.CSS_SELECTOR, "dl.accordion")
            )
        )
        body = self.driver.page_source
        url = self.driver.current_url
        return HtmlResponse(url, body=body, encoding="utf-8")

    def parse(self, response, *_args, **_kwargs):
        response = self.number_response(response)
        is_bill_of_lading = bool(response.css("[class='bolToggle']").get())
        if is_bill_of_lading:
            yield self.parse_bol(response, self.number)
        else:
            yield self.parse_container(response, self.number)

    @staticmethod
    def parse_container(response, number):
        container = response.css(".containerAccordion > dd")
        pol = (
            container.css(
                "[class='resultTable'] > tbody > *:last-child > [data-title='Location'] > span::text"
            )
            .get()
            .strip()
        )
        pod = (
            container.css("[data-title='Final POD'] > span::text")
            .get()
            .strip()
        )
        eta = (
            container.css(
                "[data-title='Price calculation date*'] > span::text"
            )
            .get()
            .strip()
        )
        return {"number": number, "pol": pol, "pod": pod, "eta": eta}

    @staticmethod
    def parse_bol(response, number):
        pol = (
            response.css("[data-title='Port of load'] > span::text")
            .get()
            .strip()
        )
        pod = (
            response.css("[data-title='Port of discharge'] > span::text")
            .get()
            .strip()
        )
        eta = response.css(
            "[data-title='Price calculation date*'] > span::text"
        ).get()
        containers = response.css(".containerAccordion > dd")
        container_numbers = []
        for container in containers:
            container_number = remove_prefix(
                container.css(".containerToggle::text").get(),
                "Container: ",
            )
            container_numbers.append(container_number)
        return {
            "number": number,
            "pol": pol,
            "pod": pod,
            "eta": eta,
            "container_numbers": container_numbers,
        }

    def closed(self, reason):
        self.driver.close()
