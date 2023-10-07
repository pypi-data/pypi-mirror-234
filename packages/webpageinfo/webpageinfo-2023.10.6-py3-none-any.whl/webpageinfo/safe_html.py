import bs4

from webpageinfo.config.ignored_html_tags import ignored_html_tags
from webpageinfo.config.rejected_content_class import rejected_content_class
from webpageinfo.config.rejected_content_id import rejected_content_id
from webpageinfo.config.removed_html_tags import removed_html_tags
from webpageinfo.config.simple_html_tags import simple_html_tags
from webpageinfo.config.svg_tags import svg_tags

# TODO mettre in id sur les titres si pas déjà existant
# TODO conserver les id (pour les liens intradocuments)
# TODO display none https://stackoverflow.com/questions/47862023/splinter-find-by-style

_result = ""
_server_url = ""

BS4Element = (
    bs4.element.Tag
    | bs4.BeautifulSoup
    | bs4.element.NavigableString
    | bs4.element.Comment
)


def _manage_element_start(element: BS4Element) -> bool:
    """Return False to ignore."""
    global _result
    if isinstance(element, bs4.element.Tag):
        if "class" in element.attrs and any(
            class_ in element["class"] for class_ in rejected_content_class
        ):
            return False
        if "id" in element.attrs and any(
            id_ == element["id"] for id_ in rejected_content_id
        ):
            return False
        if element.name == "a" and "href" in element.attrs:
            url = element["href"]
            if url.startswith("/"):
                url = _server_url + url
            _result += f'<a href="{url}">'
        elif element.name == "img":
            url = element.attrs.get("src")
            if url is not None:
                if url.startswith("/"):
                    url = _server_url + url
                _result += f'<img src="{url}"'
                if "alt" in element.attrs:
                    _result += f' alt="{element["alt"]}"'
                if "width" in element.attrs:
                    _result += f' width="{element["width"]}"'
                if "height" in element.attrs:
                    _result += f' height="{element["height"]}"'
                _result += ">"
        elif element.name in simple_html_tags:
            _result += f"<{element.name}>"
        elif element.name in svg_tags:
            False
        elif element.name == ("iframe"):
            return False  # TODO utiliser son contenu
        elif element.name in removed_html_tags:
            return False
        elif element.name in ignored_html_tags:
            return True
        elif element.name == "[document]":
            pass  # Beautiful soup root
        else:
            raise ValueError(f"Unknown tag: {element.name}, {element}, {element.attrs}")
    elif isinstance(element, bs4.element.Comment):
        return False
    elif isinstance(element, bs4.element.NavigableString):
        _result += str(element)
        return False
    return True


def _manage_element_end(element: BS4Element):
    global _result
    if isinstance(element, bs4.element.Tag):
        if element.name == "a" and "href" in element.attrs:
            _result += "</a>"
        elif element.name in simple_html_tags:
            _result += f"</{element.name}>"


def _visit(element):
    if _manage_element_start(element):
        for child in getattr(element, "children", []):
            _visit(child)
        _manage_element_end(element)


def safe_html(html: str, server_url: str) -> str:
    global _result, _server_url
    _server_url = server_url
    _result = ""
    soup = bs4.BeautifulSoup(html, features="html.parser")
    _visit(soup)
    return _result.replace("<div></div>", "").replace("<p></p>", "")


def html2text(safe_html: str) -> str:
    return bs4.BeautifulSoup(safe_html, features="html.parser").text
