#!/usr/bin/env python

import json
import logging
import os
import tempfile

import isbnlib
import puremagic
import requests
from rich.console import Console
from rich.text import Text

from artemis_sg.config import CFG

MODULE = os.path.splitext(os.path.basename(__file__))[0]
console = Console()


class ImgDownloader:
    def is_image(self, path):
        """Check given filepath to see if it is an image.
        If so, return extension type, else return None."""
        try:
            kind = puremagic.from_file(path)
        except (puremagic.main.PureError, ValueError):
            kind = None
        if kind not in [".jpg", ".png"]:
            kind = None
        return kind

    def download(self, image_dict, target_dir=""):
        namespace = f"{type(self).__name__}.{self.download.__name__}"

        if not target_dir:
            target_dir = tempfile.mkdtemp(prefix="ImgDownloader-")
            logging.warning(f"{namespace}: Creating target directory at {target_dir}")
        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)

        for key in image_dict:
            for i, url in enumerate(image_dict[key]):
                isbn = isbnlib.to_isbn13(key)
                if not isbn:
                    isbn = key
                suffix = "" if i == 0 else f"-{i}"
                image = f"{isbn}{suffix}.jpg"
                image_path = os.path.join(target_dir, image)
                if not os.path.isfile(image_path) or not self.is_image(image_path):
                    logging.debug(f"{namespace}: Downloading '{url}' to '{target_dir}'")
                    with open(image_path, "wb") as fp:
                        r = requests.get(url, timeout=10)
                        fp.write(r.content)

                    # validate file and name it in accordance with its type
                    fmt = self.is_image(image_path)
                    if fmt == ".jpg":
                        pass
                    elif fmt == ".png":
                        # rename file with png suffix
                        old_path = image_path
                        image_path = os.path.splitext(old_path)[0] + ".png"
                        os.rename(old_path, image_path)
                    else:
                        os.remove(image_path)
                        logging.warning(
                            f"{namespace}: Skipping unsupported file type in '{url}'"
                        )
                    logging.info(f"{namespace}: Saved '{image_path}")

        return target_dir


def main():
    scraped_datafile = CFG["asg"]["data"]["file"]["scraped"]
    saved_images_dir = CFG["asg"]["data"]["dir"]["images"]
    if not os.path.isdir(saved_images_dir):
        dest = None

    dloader = ImgDownloader()

    def get_json_data_from_file(datafile):
        namespace = f"{MODULE}.main.{get_json_data_from_file.__name__}"
        try:
            with open(datafile) as filepointer:
                data = json.load(filepointer)
            filepointer.close()
            return data
        except FileNotFoundError:
            logging.error(f"{namespace}: Datafile '{datafile}' not found")
            return {}
        except json.decoder.JSONDecodeError:
            logging.error(
                f"{namespace}: Datafile '{datafile}' did not contain valid JSON"
            )
            return {}

    def get_image_url_dict(data):
        url_dict = {}
        for key in data:
            url_dict[key] = data[key]["image_urls"]
        return url_dict

    scraped_data = get_json_data_from_file(scraped_datafile)
    img_dict = get_image_url_dict(scraped_data)
    dest = dloader.download(img_dict, saved_images_dir)
    dest_text = Text(f"Images downloaded to {dest}.")
    dest_text.stylize("green")
    console.print(dest_text)


if __name__ == "__main__":
    main()
