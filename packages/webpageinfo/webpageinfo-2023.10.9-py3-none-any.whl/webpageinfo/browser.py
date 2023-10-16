from collections.abc import Iterable

import splinter
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver
from splinter.driver.webdriver import BaseWebDriver


class WebElementNotFound(Exception):
    pass


def _find_elements_by(
    root,
    tag: str = "",
    class_name: str = "",
    css: str = "",
    xpath: str = "",
    wait_time: float = 0,
) -> Iterable["WebElement"]:
    if tag:
        for elem in root.find_by_tag(tag, wait_time):
            yield WebElement(elem)
    if class_name:
        for elem in root.find_by_css(f".{class_name}", wait_time):
            yield WebElement(elem)
    if css:
        for elem in root.find_by_css(css, wait_time):
            yield WebElement(elem)
    if xpath:
        for elem in root.find_by_xpath(xpath, wait_time):
            yield WebElement(elem)


class _Findable:
    @property
    def _root(self):
        raise NotImplementedError

    def find_elements_by(
        self,
        tag: str = "",
        class_name: str = "",
        css: str = "",
        xpath: str = "",
        wait_time: float = 0,
    ) -> Iterable["WebElement"]:
        yield from _find_elements_by(self._root, tag, class_name, css, xpath, wait_time)

    def find_element_by(
        self,
        tag: str = "",
        class_name: str = "",
        css: str = "",
        xpath: str = "",
        wait_time: float = 0,
    ) -> "WebElement":
        try:
            return next(
                iter(
                    _find_elements_by(
                        self._root, tag, class_name, css, xpath, wait_time
                    )
                )
            )
        except StopIteration:
            raise WebElementNotFound

    def is_element_present_by(self, tag: str = "", wait_time: float = 0) -> bool:
        if tag:
            return self._root.is_element_present_by_tag(tag)


class WebElement(_Findable):
    def __init__(self, implementation_element):
        self._element = implementation_element

    @property
    def _root(self):
        return self._element

    def __getattr__(self, name):
        """Proxy for internal implementation."""
        return getattr(self._element, name)

    def __getitem__(self, key):
        """Proxy for internal implementation."""
        return self._element[key]


class Browser(_Findable):
    def __init__(self, *args, **kwargs):
        profile_preferences = {"intl.accept_languages": "fr-FR,en-US,en-GB"}
        self.driver: BaseWebDriver = splinter.Browser(
            "firefox",
            *args,
            incognito=True,
            profile_preferences=profile_preferences,
            **kwargs,
        )
        self.selenium_driver.set_window_size(1024, 1024)
        self.selenium_driver.implicitly_wait(10)  # seconds

    @property
    def _root(self) -> BaseWebDriver:
        return self.driver

    @property
    def selenium_driver(self) -> SeleniumWebDriver:
        return self.driver.driver

    def __getattr__(self, name):
        """Proxy for internal implementation."""
        return getattr(self.driver, name)
