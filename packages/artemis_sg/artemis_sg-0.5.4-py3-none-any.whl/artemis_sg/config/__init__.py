import logging
import os

from flatten_dict import flatten, unflatten

import artemis_sg

namespace = "artemis_sg.config"

# Everyghing that can be configured is here.
CFG = {
    "asg": {
        "vendors": [
            {"code": "sample", "name": "Sample Vendor", "isbn_key": "ISBN-13"},
            {"code": "sample2", "name": "Another Vendor", "isbn_key": "ISBN"},
        ],
        "spreadsheet": {
            "sheet_image": {
                "image_row_height": 105,
                "image_col_width": 18,
                "isbn_col_width": 13,
                "max_col_width": 50,
                "col_buffer": 1.23,
            },
            "mkthumbs": {
                "width": 130,
                "height": 130,
            },
        },
        "scraper": {
            "headless": False,
        },
        "data": {
            "file": {
                "scraped": os.path.join(artemis_sg.data_dir, "scraped_items.json"),
            },
            "dir": {
                "images": os.path.join(artemis_sg.data_dir, "downloaded_images"),
                "upload_source": os.path.join(artemis_sg.data_dir, "downloaded_images"),
            },
        },
        "test": {
            "sheet": {"id": "GOOGLE_SHEET_ID_HERE", "tab": "GOOGLE_SHEET_TAB_HERE"}
        },
    },
    "google": {
        "cloud": {
            "bucket": "my_bucket",
            "bucket_prefix": "my_bucket_prefix",
            "key_file": os.path.join(
                artemis_sg.data_dir, "google_cloud_service_key.json"
            ),
        },
        "docs": {
            "api_creds_file": os.path.join(artemis_sg.data_dir, "credentials.json"),
            "api_creds_token": os.path.join(
                artemis_sg.data_dir, "app_creds_token.json"
            ),
        },
    },
}

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

conf_file = "config.toml"

conf_path = os.path.join(artemis_sg.conf_dir, conf_file)

try:
    with open(conf_path, mode="rb") as fp:
        f_config = tomllib.load(fp)
except FileNotFoundError:
    import tomli_w

    logging.warning(f"{namespace}: Config file not found at {conf_path}.")
    logging.warning(f"{namespace}: Creating new config file at {conf_path}.")
    logging.warning(
        f"{namespace}: IMPORTANT: Edit file to set proper values for google_cloud."
    )

    d = os.path.dirname(conf_path)
    if not os.path.exists(d):
        os.makedirs(d)
    with open(conf_path, mode="wb") as fp:
        tomli_w.dump(CFG, fp)
    with open(conf_path, mode="rb") as fp:
        f_config = tomllib.load(fp)

# Update CFG with contents of f_config
flat_cfg = flatten(CFG)
flat_f_config = flatten(f_config)
flat_merged = flat_cfg | flat_f_config
CFG = unflatten(flat_merged)

# Create all defined data_dir subdirectories
for key in CFG["asg"]["data"]["dir"]:
    d = CFG["asg"]["data"]["dir"][key]
    if not os.path.exists(d):
        logging.warning(f"{namespace}: Creating new directory at {d}.")
        os.makedirs(d)

# Create all defined data_dir files
for key in CFG["asg"]["data"]["file"]:
    f = CFG["asg"]["data"]["file"][key]
    if not os.path.exists(f):
        d = os.path.dirname(f)
        if not os.path.exists(d):
            logging.warning(f"{namespace}: Creating new directory at {d}.")
            os.makedirs(d)
        logging.warning(f"{namespace}: Creating new file at {f}.")
        _root, ext = os.path.splitext(f)
        with open(f, "w") as fp:
            # Seed JSON files with valid empty JSON.
            if ext.lower() == ".json":
                fp.write("{ }")
            pass
