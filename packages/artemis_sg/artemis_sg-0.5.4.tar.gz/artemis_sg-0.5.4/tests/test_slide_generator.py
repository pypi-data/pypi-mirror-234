# ruff: noqa: S101
from unittest.mock import Mock

import pytest
from googleapiclient.discovery import build

from artemis_sg import slide_generator
from artemis_sg.app_creds import app_creds
from artemis_sg.config import CFG
from artemis_sg.gcloud import GCloud
from artemis_sg.items import Items
from artemis_sg.vendor import Vendor


def test_generate(items_collection):
    """
    Given a SlideGenerator object
    When the generate() method is called on it
    Then it returns a slide deck link with the expected ID
    """
    slides_dict = {
        "objectId": "fooSlide",
        "pageElements": [
            {"objectId": "fooElem0"},
            {"objectId": "fooElem1"},
        ],
    }
    gcloud = Mock()
    gcloud.list_image_blobs.return_value = []
    vendor = Mock()
    slides = Mock()
    call_chain1 = "presentations.return_value.create.return_value.execute.return_value"
    call_chain2 = (
        "presentations.return_value."
        "batchUpdate.return_value."
        "execute.return_value."
        "get.return_value"
    )
    config = {
        "name": "mocky_slides",
        call_chain1: {"presentationId": "MyPresId", "slides": [slides_dict]},
        call_chain2: [{"createSlide": {"objectId": "MySlideId"}}],
    }
    slides.configure_mock(**config)

    sg_obj = slide_generator.SlideGenerator(slides, gcloud, vendor)
    link = sg_obj.generate(items_collection, "bucket_pre", "Cool title")

    assert link == "https://docs.google.com/presentation/d/MyPresId"


def test_blacklisted_keys():
    """
    Given a SlideGenerator object
    When the create_slide_text() method is called on it
    Then the object's blacklisted keys do not appear in text
    """

    class MockItem:
        def __init__(self):
            self.data = {"AUTHOR": "Dr. Seuss"}
            self.isbn_key = "ISBN"
            for blacklisted in sg_obj.BLACKLIST_KEYS:
                self.data[blacklisted] = "I should not be here!"

    sg_obj = slide_generator.SlideGenerator("foo", "bar", "baz")
    text = sg_obj.create_slide_text(MockItem(), 99)

    assert "Seuss" in text
    for blacklisted in sg_obj.BLACKLIST_KEYS:
        assert blacklisted not in text


def test_gj_binding_map():
    """
    Given a SlideGenerator object
    When the gj_binding_map() method is called on it
    Then the expected value is returned
    """
    m = {
        "P": "Paperback",
        "H": "Hardcover",
        "C": "Hardcover",
        "C NDJ": "Cloth, no dust jacket",
        "CD": "CD",
    }
    sg_obj = slide_generator.SlideGenerator("foo", "bar", "baz")

    for key, value in m.items():
        assert sg_obj.gj_binding_map(key) == value


def test_gj_type_map():
    """
    Given a SlideGenerator object
    When the gj_type_map() method is called on it
    Then the expected value is returned
    """
    m = {
        "R": "Remainder",
        "h": "Return",
    }
    sg_obj = slide_generator.SlideGenerator("foo", "bar", "baz")

    for key, value in m.items():
        assert sg_obj.gj_type_map(key) == value


def test_get_req_update_artemis_slide(monkeypatch, items_collection, target_directory):
    """
    Given a SlideGenerator object
    When the get_req_update_artemis_slide() method is called on it
    AND global requests is returned
    AND it contains 'createImage' for the `item.image_urls`
    AND it contains 'insertText' for the text objectid
    AND gcloud.upload_cloud_blob is called with text image filepath
    AND gcloud.generate_cloud_signed_url is called
    """
    base_dict = {"placeholder": "here"}
    gcloud = Mock()
    slides = Mock()
    call_chain = (
        "presentations.return_value."
        "batchUpdate.return_value."
        "execute.return_value."
        "get.return_value"
    )
    config = {
        "name": "mocky_slides",
        call_chain: [{"createShape": {"objectId": "foobarbaz"}}],
    }
    slides.configure_mock(**config)
    item = items_collection.get_items()[0]
    item.image_urls = ["foo"]

    sg_obj = slide_generator.SlideGenerator(slides, gcloud, "vendor")
    g_reqs = sg_obj.get_req_update_artemis_slide(
        "deckid", "slideid", item, target_directory, [base_dict]
    )

    assert any(
        d.get("url") == "foo" for d in [d.get("createImage", base_dict) for d in g_reqs]
    )
    assert any(
        d.get("objectId") == "foobarbaz"
        for d in [d.get("insertText", base_dict) for d in g_reqs]
    )
    gcloud.upload_cloud_blob.assert_called  # noqa: B018
    gcloud.generate_cloud_signed_url.assert_called  # noqa: B018


@pytest.mark.database()
@pytest.mark.integration()
def test_slide_generator():
    """
    GIVEN a Vendor object  # for vendor specific slide logic
    AND a Google Sheet ID
    AND a Google Sheet tab
    AND a Slides API object
    AND a GCloud API object
    AND a Items dataset unified from sheet and scraped data
    AND a SlideGenerator object given Vendor, GCloud, and Slides objects
    WHEN we call the generate() method given Items, and title
    THEN a Google slide deck is created with given title and data
    """
    # vendor object
    vendr = Vendor("sample")
    vendr.set_vendor_data()

    # sheet id
    sheet_id = CFG["asg"]["test"]["sheet"]["id"]
    sheet_tab = CFG["asg"]["test"]["sheet"]["tab"]

    creds = app_creds()
    slides = build("slides", "v1", credentials=creds)

    # GCloud object
    bucket_name = CFG["google"]["cloud"]["bucket"]
    cloud_key_file = CFG["google"]["cloud"]["key_file"]
    gcloud = GCloud(cloud_key_file=cloud_key_file, bucket_name=bucket_name)

    # Items dataset
    sheets = build("sheets", "v4", credentials=creds)
    sheet_data = (
        sheets.spreadsheets()
        .values()
        .get(range=sheet_tab, spreadsheetId=sheet_id)
        .execute()
        .get("values")
    )
    sheet_keys = sheet_data.pop(0)
    items_obj = Items(sheet_keys, sheet_data, vendr.isbn_key)
    items_obj.load_scraped_data("scraped_items.json")

    sg = slide_generator.SlideGenerator(slides, gcloud, vendr)

    bucket_prefix = CFG["google"]["cloud"]["bucket_prefix"]
    slide_deck = sg.generate(items_obj, bucket_prefix, "Cool title")

    assert slide_deck
