"""Define scrape_glosbe_dict."""
# pylint: disable=invalid-name
import os
from pathlib import Path

import httpx
import logzero
from joblib import Memory
from logzero import logger
from pyquery import PyQuery as pq
from set_loglevel import set_loglevel
from tenacity import (
    retry,
    stop_after_attempt,
    stop_after_delay,
    wait_exponential,
    wait_random,
)

logzero.loglevel(set_loglevel())

# set CACHEOFF=1  or os.environ["CACHEOFF"] = "1" during test
# set CACHEOFF= or del os.environ["CACHEOFF"]
cacheoff = os.environ.get("CACHEOFF", False)

if "__file__" not in globals():
    __file__ = "temp"
location = (
    None if cacheoff else Path("~/.cache/joblib", Path(__file__).stem).expanduser()
)

# turn on during dev: set VERBOSE=1 or os.environ["VERBOSE"] = "1"
verbose = 0 if not os.environ.get("VERBOSE", False) else 1

memory = Memory(location=location, verbose=verbose)
if location:
    location.mkdir(exist_ok=True)
    logger.info("joblib memory cached to %s", location)
else:
    logger.info("joblib cache is off")


url = "https://glosbe.com/"


@memory.cache
@retry(
    stop=stop_after_delay(120) | stop_after_attempt(20),
    wait=wait_exponential(max=36000) + wait_random(0, 2),
)
def scrape_glosbe_dict(
    word: str,
    from_lang: str = "en",
    to_lang: str = "zh",
):
    """Define scrape_glosbe_dict.

    Args:
        word: str
        from_lang: source language
        to_lang: dest language
    Returns:
        translation + less frequent translation
    """
    logger.debug("word: %s", word)
    try:
        resp = httpx.get(f"{url}{from_lang}/{to_lang}/{word}")
    except Exception as e:
        logger.error(e)
        raise

    doc = pq(resp.text)

    # machine translation, need to render with playwright or similar
    # mt = doc('.flex-1>.dense').text()

    try:
        trtext = doc(".translation.dense").text()
    except Exception as e:
        logger.error(e)
        raise

    try:
        trtext_lf = doc(
            ".px-2.text-sm.font-medium.less-frequent-translations__list-compact.dense"
        ).text()
    except Exception as e:
        logger.error(e)
        raise
    _ = f"{trtext}, {trtext_lf}"
    return _.strip()
