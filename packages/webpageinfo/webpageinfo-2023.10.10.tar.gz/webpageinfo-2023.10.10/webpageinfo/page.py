"""Page information."""
# TODO get canonical url: <link rel="canonical"
# href="https://leszexpertsfle.com/ressources-fle/raconter-une-histoire-damour-b1-et/"
# />
# TODO regarder dans les iframe pour trouver des liens et du contenu et des PDF

import math
import re
import urllib.parse
import uuid
from collections import Counter
from contextlib import suppress
from pathlib import Path
from collections.abc import Iterable
from string import ascii_letters, digits

import httpx
import pdfminer.pdfparser
from pdfminer.high_level import extract_text
from PIL import Image
from selenium.common.exceptions import StaleElementReferenceException

from webpageinfo.browser import Browser, WebElementNotFound
from webpageinfo.config.ignored_word_in_tags import ignored_word_in_tags
from webpageinfo.safe_html import html2text, safe_html


def get_random_temp_file_name(extension: str = "") -> str:
    """Return a random filename in /tmp."""
    return f"/tmp/{uuid.uuid4()}.{extension}"


def extract_tags_from_words(words: list[str]) -> Iterable[str]:
    counter = Counter(words)
    nb_words = len(words)
    threshold = math.sqrt(nb_words) / 5
    # print(threshold)
    result = []
    result_lower = set()
    for word, nb_apparitions in sorted(
        counter.most_common(),
        key=lambda c: c[1],
        reverse=True,
    ):
        if nb_apparitions < max(threshold, 5.1):
            break
        if len(word) <= 4 and not word[0].isupper():
            continue
        if len(word) <= 2:
            continue
        if word.lower() in ignored_word_in_tags:
            continue
        if len(list(c for c in word if c in digits)) >= len(
            list(c for c in word if c in ascii_letters)
        ):
            continue
        if re.search(r"^\d[\d\w]+$", word) is not None:
            continue
        if word.lower() not in result_lower:
            result_lower.add(word.lower())
            result.append(word)
        # print(word, nb_apparitions)
    return result


class Page:
    """Page information."""

    def _fetch_title(self: "Page", browser: Browser) -> None:
        # wordpress
        with suppress(WebElementNotFound):
            title = browser.find_element_by(class_name="entry-title").text
            if title:
                self.title = title
                return

        with suppress(WebElementNotFound):
            head = browser.find_element_by(tag="head")
            title = title = head.find_element_by(tag="title").text
            if title:
                self.title = title
                return

        self.title = browser.title

    def _fetch_links(self: "Page", browser: Browser) -> None:
        # avoid javascript, read from source
        html = httpx.get(self.url, follow_redirects=True)
        html.raise_for_status()
        for match in re.finditer(r'<a[^>]*href="([^"]+)"', html.text, re.MULTILINE):
            self.links.add(self.to_absolute_url(match[1]))

        # use javascript
        for a_tag in browser.find_elements_by(tag="a"):
            try:
                href = a_tag["href"]
            except StaleElementReferenceException:
                href = ""
            if href:
                self.links.add(self.to_absolute_url(href))

    def _fetch_tags(self: "Page", browser: Browser) -> None:
        for link in browser.find_elements_by(tag="a"):
            try:
                if "tag" in link["rel"]:
                    self.tags.add(link.text)
            except StaleElementReferenceException:
                pass
        for tag in browser.find_elements_by(class_name="tag__link"):
            self.tags.add(tag.text)

    def _fetch_description(self: "Page", browser: Browser) -> None:
        metas = list(browser.find_elements_by(tag="meta"))

        # should be ordered by priority, first is most relevant
        meta_keywords = (
            "description",
            "og:description",
            "twitter:description",
            "keywords",
        )

        for keyword in meta_keywords:
            for meta in metas:
                name = meta["name"] or meta["property"]
                if name == keyword and meta["content"].strip():
                    self.description = meta["content"].strip()
                    return

    def _fetch_content(self: "Page", browser: Browser) -> None:
        content_element = browser.find_element_by(tag="body")
        try:
            content_elements = list(browser.find_elements_by(tag="article"))
            if len(content_elements) == 1:
                content_element = content_elements[0]
        except WebElementNotFound:
            pass

        content_classes = (
            "et_pb_post_content",
            "blog-post-content",
            "entry-content",
            "post-article",
        )
        for class_ in content_classes:
            try:
                content_element = browser.find_element_by(class_name=class_)
                break
            except WebElementNotFound:
                pass

        self.content = content_element.html

    def _fetch_screenshot(self: "Page", browser: Browser) -> None:
        self.screenshot = get_random_temp_file_name(extension="png")
        browser.selenium_driver.save_screenshot(self.screenshot)
        image = Image.open(self.screenshot)
        image.thumbnail((1000, 1000))
        image.save(self.screenshot, optimize=True, quality=40)

    def _fetch_source(self: "Page", browser: Browser) -> None:
        self.source = browser.selenium_driver.page_source

    def _fetch_pdf_content(self: "Page") -> None:
        for pdf_url in self.attached_pdf:
            print("Downloading", pdf_url)
            pdf = httpx.get(pdf_url, follow_redirects=True)
            pdf.raise_for_status()
            tmp_file_path = get_random_temp_file_name(extension="pdf")
            Path(tmp_file_path).write_bytes(pdf.content)
            print("Saved in", tmp_file_path)
            with suppress(pdfminer.pdfparser.PDFSyntaxError):
                self.pdf_content += f"{extract_text(tmp_file_path)} "

    def _fetch_information(self: "Page") -> None:
        browser = Browser(headless=True)
        browser.visit(self.url)
        if not browser.is_element_present_by(tag="title", wait_time=10):
            raise ValueError("No internet access")
        if not browser.is_element_present_by(tag="body", wait_time=10):
            raise ValueError("No internet access")
        self._fetch_title(browser)
        self._fetch_source(browser)
        self._fetch_links(browser)
        self._fetch_tags(browser)
        self._fetch_description(browser)
        self._fetch_content(browser)
        self._fetch_screenshot(browser)
        self._fetch_pdf_content()

        self.safe_html = safe_html(self.content, self.server)
        self.text = html2text(self.safe_html)
        self.total_text = re.sub(
            r"[\n\s\W_]+",
            " ",
            f"{self.text} {self.pdf_content} {self.description} {' '.join(self.tags)}",
            flags=re.DOTALL | re.MULTILINE,
        )
        self.words = self.total_text.split()
        self.words_tags = extract_tags_from_words(self.words)
        browser.quit()

    def __init__(self: "Page", url: str) -> None:
        self.url: str = url
        url = urllib.parse.urlparse(self.url)
        self.server = f"http://{url.netloc}"
        self.title: str = ""
        self.links: set[str] = set()
        self.tags: set[str] = set()
        self.description: str = ""
        self.content: str = ""
        self.safe_html: str = ""
        self.text: str = ""
        self.total_text: str = ""
        self.words: list[str] = []
        self.words_tags: list[str] = []
        self.screenshot: str = ""
        self.pdf_content: str = ""
        self.source: str = ""
        self._fetch_information()

    def to_absolute_url(self, url: str) -> str:
        if url.startswith("/") and not url.startswith("//"):
            return self.server + url
        if url.startswith(("#", "?")):
            return (
                self.url + url
            )  # TODO remove fragment + query from self.url (urlparse)
        # return url.replace("http://", "https://") # some sites don't support HTTPS!
        return url

    @property
    def attached_pdf(self) -> Iterable[str]:
        return [
            self.to_absolute_url(link) for link in self.links if link.endswith(".pdf")
        ]

    @property
    def all_tags(self) -> list[str]:
        result = []
        result_lower = set()
        for tag in self.tags:
            if tag.lower() not in result_lower:
                result_lower.add(tag.lower())
                result.append(tag)
        for tag in self.words_tags:
            if tag.lower() not in result_lower:
                result_lower.add(tag.lower())
                result.append(tag)
        return result


if __name__ == "__main__":
    pages = [
        # "https://leszexpertsfle.com/ressources-fle/raconter-une-histoire-damour-b1-et/",
        # "https://littefle.wordpress.com/2019/10/16/le-prix-nobel-de-litterature-en-5-minutes/",
        # "https://jancovici.com/changement-climatique/aspects-physiques/variation-du-climat-et-augmentation-de-leffet-de-serre-due-a-lhomme-cest-pareil/",
        # "https://adamj.eu/tech/2022/03/30/how-to-make-django-error-for-undefined-template-variables/",
        # "https://realpython.com/pypi-publish-python-package/",
        "https://agi.to/enseigner/ressource/carte-didentite-de-super-heros/",
    ]
    for url in pages:
        print("=" * 80)
        page = Page(url)
        print("URL", page.url)
        print("title", page.title)
        # print("links", page.links)
        print("tags", page.tags)
        print("words tags", page.words_tags)
        print("all_tags", page.all_tags)
        print("description:")
        print(page.description)
        print("pdfs", page.attached_pdf)
        print("screenshot", page.screenshot)
        # print("pdf content", page.pdf_content)
        print("text", page.total_text[:2000].replace("\n", " "))

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(
            '<html><head><link rel="stylesheet" '
            'href="https://www.lecalamar.fr/css/main.css"></head>'
            '<body style="max-width: 17cm;">'
        )
        f.write(page.safe_html)
        f.write("</body></html>")
