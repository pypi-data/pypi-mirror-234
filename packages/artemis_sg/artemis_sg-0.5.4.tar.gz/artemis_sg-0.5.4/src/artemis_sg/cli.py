#!/usr/bin/env python

import logging
import os
import sys
from time import sleep

import click
from rich.console import Console
from rich.progress import track
from rich.text import Text
from selenium.common.exceptions import NoSuchWindowException

from artemis_sg import scraper, spreadsheet
from artemis_sg.config import CFG

MODULE = os.path.splitext(os.path.basename(__file__))[0]
console = Console()

v_skip = "{}: skipping due to lack of VENDOR"
b_skip = "{}: skipping due to lack of WORKBOOK"


@click.group(chain=True)
@click.option("-V", "--verbose", is_flag=True, help="enable verbose mode")
@click.option("-D", "--debug", is_flag=True, help="enable debug mode")
@click.option("-v", "--vendor", default=None, help="Vendor code")
@click.option(
    "-b", "--workbook", default=None, help="Workbook (Sheets Doc ID or Excel File)"
)
@click.option("-s", "--worksheet", default=None, help="Worksheet within Sheets Doc")
@click.pass_context
def cli(ctx, verbose, debug, vendor, workbook, worksheet):
    """artemis_sg is a tool for processing product spreadsheet data.
    Its subcommands are designed to be used to facilitate the follow primary
    endpoint conditions:

    \b
    * A Google Slide Deck of products
    * An enhanced Excel spreadsheet
    * A website order

    The subcommands can be combined into desired workflows.

    The base command includes --vendor, --workbook, and --worksheet options.
    These are used to pass context information to the subcommands.  Some
    subcommands expect --vendor and --workbook values to perform as designed.

    Example of Google Slide Deck workflow:

        $ artemis_sg -v sample -b tests/data/test_sheet.xlsx \\
                scrape download upload generate -t "Cool Deck"

    Example of Sheet Image workflow:

        $ artemis_sg -v sample -b tests/data/test_sheet.xlsx \\
                scrape download mkthumbs sheet-image -o "NewFile.xlsx"
    """
    namespace = f"{MODULE}.cli"
    if debug:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
        logging.debug(f"{namespace}: Debug mode enabled.")

    elif verbose:
        logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
        logging.info(f"{namespace}: Verbose mode enabled.")
    else:
        logging.basicConfig(format="%(levelname)s: %(message)s")

    # load up context object (ctx)
    ctx.ensure_object(dict)
    ctx.obj["VENDOR"] = vendor
    ctx.obj["WORKBOOK"] = workbook
    ctx.obj["WORKSHEET"] = worksheet


@cli.command()
@click.pass_context
def scrape(ctx):
    """Scrape web data for vendor from workbook:worksheet

    Iterates over the item rows in the spreadsheet provided by the
    --workbook:--worksheet values passed by the base command.  The ISBN field
    is idenfied by the --vendor value passed by the base command.  For each
    ISBN in the WORKBOOK:WORKSHEET, it searches for item descriptions and
    images in a web browser.  It collects this information and stores it in the
    file defined by the configuration field [asg.data.file.scraped].  If data
    for an ISBN already exists in the datafile, the ISBN is skipped and does
    not result in re-scraping data for that record.

    Scrape supports both Google Sheet ID and Excel file paths for the WORKBOOK
    value.

    If a --worksheet is not defined, the first sheet in the WORKBOOK will be
    used.  If the given WORKBOOK contains multiple sheets and the sheet
    containing the desired data is not the first sheet in the WORKBOOK, the
    --worksheet will need to be specified for the base command.

    The command utilizes configuration variables stored in "config.toml" to set
    the vendor from [asg.vendors] and scraped items database from
    [asg.data.file.scraped].
    """
    cmd = "scrape"
    if ctx.obj["VENDOR"]:
        if ctx.obj["WORKBOOK"]:
            sdb = CFG["asg"]["data"]["file"]["scraped"]
            msg = (
                f"Scraping web data for '{ctx.obj['VENDOR'] or ''!s}' "
                f"using '{ctx.obj['WORKBOOK'] or ''!s}':"
                f"'{ctx.obj['WORKSHEET'] or ''!s}', "
                f"saving data to '{sdb}'..."
            )
            click.echo(msg)
            scraper_wrapper(
                ctx.obj["VENDOR"], ctx.obj["WORKBOOK"], ctx.obj["WORKSHEET"], sdb
            )
        else:
            click.echo(b_skip.format(cmd), err=True)
    else:
        click.echo(v_skip.format(cmd), err=True)


@cli.command()
def download():
    """
    Download scraped images

    Iterates over the data records in the file defined by the configuration
    field [asg.data.file.scraped].  For each record, it downloads the image
    files associated with the record to a local directory as defined by the
    configuration field [asg.data.dir.images].
    """
    namespace = f"{MODULE}.download"

    download_path = CFG["asg"]["data"]["dir"]["images"]
    click.echo("Downloading images...")
    logging.debug(f"{namespace}: Download path is: {download_path}")

    img_downloader_wrapper()


@cli.command()
def upload():
    """
    Upload local images to Google Cloud Storage Bucket

    Uploads the files in the directory defined by the configuration field
    [asg.data.dir.upload_source] to the Google Cloud bucket defined by the
    configuration field [google.cloud.bucket].  Only the first level of the
    source directory is uploaded.  Subdirectories of the source directory are
    not traversed for the upload.  All uploaded files are prefixed with value
    defined by the configuration field [google.cloud.bucket_prefix].
    """
    namespace = f"{MODULE}.upload"

    upload_source = CFG["asg"]["data"]["dir"]["upload_source"]
    click.echo("Uploading images to Google Cloud...")
    logging.debug(f"{namespace}: Upload source path is: {upload_source}")

    gcloud_wrapper()


@cli.command()
@click.option("-t", "--title", default="New Arrivals", help="Slide deck title")
@click.pass_context
def generate(ctx, title):
    """
    Generate a Google Slide Deck


    The slide deck will be given a title based on the values supplied by VENDOR
    and --title.  The title slide will be in the following format:

        Artemis Book Sales Presents...
        Vendor Name, Title

    Iterates over item rows in the spreadsheet provided by the
    --workbook:--worksheet values passed by the base command.  The ISBN field
    is idenfied by the --vendor value passed by the base command.  For each
    ISBN in the WORKBOOK:WORKSHEET
    for which it has image data it creates a slide containing the
    spreadsheet data, the description saved in the file defined by the configuration
    field [asg.data.file.scraped], and the images saved in the
    [google.cloud.bucket].  The Google sheet will be saved to the root of the
    Google Drive associated with the credentials created during initial
    installation.

    Generate supports both Google Sheet ID and Excel file paths for the WORKBOOK
    value.

    If a --worksheet is not defined, the first sheet in the WORKBOOK will be
    used.  If the given WORKBOOK contains multiple sheets and the sheet
    containing the desired data is not the first sheet in the WORKBOOK, the
    --worksheet will need to be specified for the base command.

    The command utilizes configuration variables stored in "config.toml" to set
    the vendor from [asg.vendors] and scraped items database from
    [asg.data.file.scraped].
    """
    cmd = "generate"
    namespace = f"{MODULE}.{cmd}"

    sdb = CFG["asg"]["data"]["file"]["scraped"]
    msg = (
        f"Creating Google Slides deck '{title}' for '{ctx.obj['VENDOR'] or ''!s}' "
        f"using '{ctx.obj['WORKBOOK'] or ''!s}':'{ctx.obj['WORKSHEET'] or ''!s}'..."
    )
    click.echo(msg)
    logging.debug(f"{namespace}: Scraped Items Database is: {sdb}")

    try:
        slide_generator_wrapper(
            ctx.obj["VENDOR"], ctx.obj["WORKBOOK"], ctx.obj["WORKSHEET"], sdb, title
        )
    except Exception as e:
        click.echo(f"Could not generate slide deck:{e}", err=True)
        if not ctx.obj["VENDOR"]:
            click.echo("\tVENDOR not provided", err=True)
        if not ctx.obj["WORKBOOK"]:
            click.echo("\tWORKBOOK not provided", err=True)


@cli.command()
@click.option("-o", "--output", "out", default="out.xlsx", help="Output file")
@click.pass_context
def sheet_image(ctx, out):
    """
    Insert item thumbnail images into spreadsheet

    Iterates over item rows in the spreadsheet provided by the
    --workbook:--worksheet values passed by the base command.  The ISBN field
    is idenfied by the --vendor value passed by the base command.  For each

    Modifies a local XLSX spreadsheet file provided by the
    --workbook:--worksheet values passed by the base command to include
    thumbnail images in the second column for ISBN items (field itentified by
    --vendor) in which local thumbnail image files are available and saves a
    new XLSX file.

    By default, the thumbnail images are obtained from
    [asg.data.dir.images]/thumbnails and the new XLSX file is saved as
    "out.xlsx" in the current working directory.

    NOTE: Currently, the command does not support Google Sheet IDs as a valid
    WORKBOOK type.

    If a --worksheet is not defined, the first sheet in the WORKBOOK will be
    used.  If the given WORKBOOK contains multiple sheets and the sheet
    containing the desired data is not the first sheet in the WORKBOOK, the
    --worksheet will need to be specified for the base command.

    The command utilizes configuration variables stored in "config.toml" to set
    the vendor from [asg.vendors].
    """
    cmd = "sheet-image"
    namespace = f"{MODULE}.sheet_image"

    if ctx.obj["VENDOR"]:
        if ctx.obj["WORKBOOK"]:
            download_path = CFG["asg"]["data"]["dir"]["images"]
            image_directory = os.path.join(download_path, "thumbnails")
            msg = (
                f"Creating image enhanced spreadsheet for "
                f"'{ctx.obj['VENDOR'] or ''!s}' "
                f"using '{ctx.obj['WORKBOOK'] or ''!s}':"
                f"'{ctx.obj['WORKSHEET'] or ''!s}', "
                f"saving Excel file to '{out}'..."
            )
            click.echo(msg)
            logging.debug(
                f"{namespace}: Thumbnail Image Directory is: {image_directory}"
            )

            sheet_image_wrapper(
                ctx.obj["VENDOR"],
                ctx.obj["WORKBOOK"],
                ctx.obj["WORKSHEET"],
                image_directory,
                out,
            )
        else:
            click.echo(b_skip.format(cmd), err=True)
    else:
        click.echo(v_skip.format(cmd), err=True)


@cli.command()
@click.option(
    "--image-directory",
    default=CFG["asg"]["data"]["dir"]["images"],
    help="Image directory",
)
def mkthumbs(image_directory):
    """
    Create thumbnails of images in IMAGE_DIRECTORY

    Creates thumbnail images from images located in a given directory.  These
    thumbnail images are saved to a "thumbnails" subdirectory in the original
    image directory.  These files are given the same names as their originals.

    By default, the command will use the directory defined by the configuration
    field [asg.data.dir.images] and size them to the dimensions defined by
    [asg.spreadsheet.mkthumbs.width] and [asg.spreadsheet.mkthumbs.height].
    """
    namespace = f"{MODULE}.mkthumbs"

    click.echo(f"Creating thumbnails of images in '{image_directory}'...")
    logging.debug(f"{namespace}: Image Directory is: {image_directory}")

    mkthumbs_wrapper(image_directory)


@cli.command()
@click.option("--email", "email", default="", help="TB Customer email to impersonate")
@click.option(
    "--timeout", "timeout", default="600", help="Maximum time to hold browser open"
)
@click.pass_context
def order(ctx, email, timeout):
    """
    Add items to be ordered to website cart of vendor from spreadsheet

    Populates the website cart for a given --vendor with items from a
    --workbook:--worksheet.  The WORKSHEET MUST contain an "Order" column from
    which the command will get the quantity of each item to put into the cart.

    The browser instance with the populated cart is left open for the user to
    review and manually complete the order.  The user will be asked to manually
    login during the execution of this command.

    NOTE: Currently, this command does not support Google Sheet IDs as a valid
    WORKBOOK type.

    If a --worksheet is not defined, the first sheet in the WORKBOOK will be
    used.  If the given WORKBOOK contains multiple sheets and the sheet
    containing the desired data is not the first sheet in the WORKBOOK, the
    --worksheet will need to be specified for the base command.

    NOTE: The browser opened by this command is controlled by this command.
    The browser will automatically close and the session will be terminated at
    the end of the defined waiting period.  If the web order has not been
    completed by the end of the waiting period, the cart may be lost depending
    on how the website handles its session data.

    The command utilizes configuration variables stored in "config.toml" to set
    the vendor from [asg.vendors].
    """
    cmd = "order"
    timeout = int(timeout)
    if ctx.obj["VENDOR"]:
        if ctx.obj["WORKBOOK"]:
            msg = (
                f"Creating web order for '{ctx.obj['VENDOR'] or ''!s}' "
                f"using '{ctx.obj['WORKBOOK'] or ''!s}':"
                f"'{ctx.obj['WORKSHEET'] or ''!s}', "
                f"Adding items to cart..."
            )
            click.echo(msg)

            order_wrapper(
                email,
                ctx.obj["VENDOR"],
                ctx.obj["WORKBOOK"],
                ctx.obj["WORKSHEET"],
                timeout,
            )
        else:
            click.echo(b_skip.format(cmd), err=True)
    else:
        click.echo(v_skip.format(cmd), err=True)


# wrappers to make the cli testable
def slide_generator_wrapper(vendor, sheet_id, worksheet, sdb, title):
    from artemis_sg import slide_generator

    slide_generator.main(vendor, sheet_id, worksheet, sdb, title)


def gcloud_wrapper():
    from artemis_sg import gcloud

    gcloud.main()


def img_downloader_wrapper():
    from artemis_sg import img_downloader

    img_downloader.main()


def scraper_wrapper(vendor, sheet_id, worksheet, sdb):
    from artemis_sg import scraper

    scraper.main(vendor, sheet_id, worksheet, sdb)


def sheet_image_wrapper(vendor, workbook, worksheet, image_directory, out):
    spreadsheet.sheet_image(vendor, workbook, worksheet, image_directory, out)


def mkthumbs_wrapper(image_directory):
    spreadsheet.mkthumbs(image_directory)


def order_wrapper(email, vendor, workbook, worksheet, timeout=600):
    order_items = spreadsheet.get_order_items(vendor, workbook, worksheet)
    driver, scrapr = get_driver_scraper(vendor, email)
    if scrapr:
        scrapr.load_login_page()
        scrapr.login()
        if vendor == "tb":
            scrapr.impersonate(email)
        for item, qty in order_items:
            if vendor == "tb":
                item_num = scrapr.search_item_num(item)
                if not item_num:
                    continue
            else:
                item_num = item
            res = scrapr.load_item_page(item_num)
            if res:
                scrapr.add_to_cart(qty)
        scrapr.load_cart_page()
        input_text = Text(
            """
        ********    USER INPUT REQUIRED    ********
        Locate the selenium controlled browser
        and manually review and complete your order.
        ********  WAITING FOR USER INPUT   ********
        """
        )
        input_text.stylize("bold cyan")
        console.print(input_text)
        warn_text = Text(
            f"WARNING:  The browser session will terminate in {timeout} seconds!!!!"
        )
        warn_text.stylize("bold red")
        console.print(warn_text)
        for _i in track(
            range(timeout), description="[red]COUNTING DOWN TIME REMAINING..."
        ):
            if not is_browser_alive(driver):
                break
            sleep(1)
    else:
        logging.error(
            f"order: VENDOR '{vendor}' is not supported by the order command."
        )
        sys.exit(1)


def get_driver_scraper(vendor, email=None):
    if vendor == "tb":
        if not email:
            logging.error(
                f"order: VENDOR '{vendor}' requires the '--email' option to be set."
            )
            sys.exit(1)
        driver = scraper.get_driver()
        scrapr = scraper.TBScraper(driver)
    elif vendor == "gj":
        driver = scraper.get_driver()
        scrapr = scraper.GJScraper(driver)
    elif vendor == "sd":
        driver = scraper.get_driver()
        scrapr = scraper.SDScraper(driver)
    else:
        driver = scrapr = None
    return driver, scrapr


def is_browser_alive(driver):
    try:
        url = driver.current_url
        if url:
            return True
    except (AttributeError, NoSuchWindowException):
        return False


if __name__ == "__main__":
    cli()
