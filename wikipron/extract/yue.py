"""Word and pron extraction for Cantonese."""

import itertools
import typing

import requests

from wikipron.extract.default import yield_pron, IPA_XPATH_SELECTOR


if typing.TYPE_CHECKING:
    from wikipron.config import Config
    from wikipron.typing import Iterator, Word, Pron, WordPronPair


# Select pron from within this li
_PRON_XPATH_TEMPLATE = """
    //div[@class="vsHide"]
        //ul
            //li[(a[@title="w:Cantonese"])]
"""


def yield_yue_pron(
    request: requests.Response, config: "Config"
) -> "Iterator[Pron]":
    for li_container in request.html.xpath(_PRON_XPATH_TEMPLATE):
        yield from yield_pron(li_container, IPA_XPATH_SELECTOR, config)


def extract_word_pron_yue(
    word: "Word", request: requests.Response, config: "Config"
) -> "Iterator[WordPronPair]":
    words = itertools.repeat(word)
    prons = yield_yue_pron(request, config)
    yield from zip(words, prons)
