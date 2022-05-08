"""Prep __main__.py."""
# pylint: disable=invalid-name
from pathlib import Path
from typing import Optional

import cchardet
import logzero
import typer
from logzero import logger
from set_loglevel import set_loglevel
from tqdm import tqdm

from scrape_glosbe_dict import __version__, scrape_glosbe_dict

logzero.loglevel(set_loglevel())

app = typer.Typer(
    name="scrape-glosbe-dict",
    add_completion=False,
    help="scrape-glosbe-dict help",
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{app.info.name} v.{__version__} -- ...")
        raise typer.Exit()


@app.command()
def main(
    hw_file: str = typer.Argument(
        ...,
        metavar="head-word-file",
        help="Head word file, one word/phrase per line, each will be used to fetch corresponding definitons from https://glosbe.com/.",
    ),
    from_lang: str = typer.Option(
        "en",
        "--from-lang",
        "-f",
        help="Source language, check https://glosbe.com/ for valid value, e.g. https://glosbe.com/en/zh implies from_lang='en'.",
    ),
    to_lang: str = typer.Option(
        "zh",
        "--to-lang",
        "-t",
        help="Target language, check https://glosbe.com/ for valid value, e.g. https://glosbe.com/en/zh implies to_lang='zh'.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        is_flag=True,
        help="Show output in the process.",
    ),
    version: Optional[bool] = typer.Option(  # pylint: disable=(unused-argument
        None,
        "--version",
        # "-v",
        "-V",
        help="Show version info and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
):
    r"""Scrape a glosbe dict.

    Args:
        hw_file: head word file
        from_lang: source lang
        to_lang: dest lang
        verbose: flag
        version: show version info
    """
    # logger.info("head word file: %s", hw_file)
    typer.echo(f" head word file: {hw_file}")
    if not Path(hw_file).is_file():
        typer.echo(f" File {hw_file} does not exist or is not a file, exiting... ")
        raise typer.Exit()

    _ = cchardet.detect(Path(hw_file).read_bytes())
    encoding = _.get("encoding")
    if encoding is None:
        typer.echo(
            f" Can't determine {hw_file}'s encoding, is it a binary file? Make sure you provide a text file."
        )
        raise typer.Exit()

    lines = []
    try:
        lines = Path(hw_file).read_text(encoding=encoding).splitlines()
    except Exception as e:
        logger.error(e)
        typer.Exit()

    words = [word.strip() for word in lines if word.strip()]

    typer.echo(
        f" from_lang: {from_lang}, to_lang: {to_lang}, total no. of head words: {len(words)} "
    )

    output = []
    for word in tqdm(words):
        logger.debug("word: %s", word)
        try:
            res = scrape_glosbe_dict(word, from_lang, to_lang)
        except Exception as e:
            logger.error("word: %s, error: %s", word, e)
            res = ""
        if verbose:
            typer.echo(f"\n{word}: {res}")
        output.append(f"{word}\t{res}")

    outfile = Path(f"{from_lang}-{to_lang}.tsv")
    try:
        outfile.write_text("\n".join(output), encoding="utf8")
        typer.echo(f" File written to {outfile}")
    except Exception as e:
        logger.error(" Unable to save: %s", e)


if __name__ == "__main__":
    app()
