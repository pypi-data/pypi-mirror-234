import pytest

from webpageinfo.page import extract_tags_from_words


@pytest.mark.parametrize(
    "words, expected",
    [
        (["vincent"] * 6, ["vincent"]),
        (["123456"] * 6, []),
        (["ou", "et", "or", "ni"] * 6, []),
        (["Title"] * 6, []),
        (["005056A90321"] * 6, []),
        (["6C1Cdb98"] * 6, []),
        (["serait"] * 6, []),
        (["90Cdbf"] * 6, []),
    ],
)
def test_extract_tags_from_words(words, expected):
    assert extract_tags_from_words(words) == expected
