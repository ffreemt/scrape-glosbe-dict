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
from ratelimit import limits, sleep_and_retry
from tenacity import (
    retry,
    stop_after_attempt,
    stop_after_delay,
    wait_exponential,
    wait_random,
)

from scrape_glosbe_dict.config import Settings

# calls = 150
# fifteen_minutes = 900  # 600/hr
# period = 900  # 600/hr

config = Settings()
calls, period = config.calls, config.period

logzero.loglevel(set_loglevel())

# set CACHEOFF=1  or os.environ["CACHEOFF"] = "1" during test
# set CACHEOFF= or del os.environ["CACHEOFF"]
cacheoff = os.environ.get("CACHEOFF", False)

if "__file__" not in globals():
    __file__ = "temp"
location = (
    # None if cacheoff else Path("~/.cache/joblib", Path(__file__).stem).expanduser()
    None if cacheoff else Path("~/.cache/joblib").expanduser()
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
@sleep_and_retry
@limits(calls=calls, period=period)
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

    if "Human test" in resp.text:
        logger.error(" Human test/solving the CAPTCHA required...")
        raise Exception("Human test")

    doc = pq(resp.text)

    # machine translation, need to render with playwright or similar
    # mt = doc('.flex-1>.dense').text()

    trlist = []
    try:
        trtext = doc(".translation.dense").text()
        if trtext:
            trlist.append(trtext)
    except Exception as e:
        logger.error(e)
        raise

    try:
        trtext_lf = doc(
            ".px-2.text-sm.font-medium.less-frequent-translations__list-compact.dense"
        ).text()
        if trtext_lf:
            trlist.append(trtext_lf)
    except Exception as e:
        logger.error(e)
        raise

    return ", ".join(trlist)
