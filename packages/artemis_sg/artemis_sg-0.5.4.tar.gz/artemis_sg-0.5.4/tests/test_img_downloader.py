# ruff: noqa: S101
import glob
import logging
import os
import shutil
import tempfile
from unittest.mock import Mock

import pytest

from artemis_sg import img_downloader


def teardown_function():
    img_dloader_temp_dirs = glob.glob(
        os.path.join(tempfile.gettempdir(), "ImgDownloader-*")
    )
    for d in img_dloader_temp_dirs:
        shutil.rmtree(d)


@pytest.fixture()
def populated_target_directory(tmp_path_factory, isbn13, jpg_filepath):
    path = tmp_path_factory.mktemp("data")
    shutil.copyfile(jpg_filepath, os.path.join(path, f"{isbn13}.jpg"))
    shutil.copyfile(jpg_filepath, os.path.join(path, f"{isbn13}-1.jpg"))
    yield path


@pytest.fixture()
def mock_jpg_response(jpg_filepath):
    with open(jpg_filepath, mode="rb") as file:
        file_content = file.read()

    class MockResponse:
        pass

    mock_response = MockResponse()
    mock_response.content = file_content

    return mock_response


@pytest.fixture()
def mock_png_response(png_filepath):
    with open(png_filepath, mode="rb") as file:
        file_content = file.read()

    class MockResponse:
        pass

    mock_response = MockResponse()
    mock_response.content = file_content

    return mock_response


@pytest.fixture()
def mock_txt_response():
    class MockResponse:
        pass

    mock_response = MockResponse()
    mock_response.content = b"Hello, World!\n"

    return mock_response


def test_download_via_isbn13(monkeypatch, isbn13, mock_jpg_response, target_directory):
    """
    Given an ImgDownloader object
    AND a dictionary of images whose key is an isbn13
    AND an existing target directory
    WHEN we run the download method with the dictionary and target directory
    THEN the image urls are downloaded to the target directory
    """
    dloader = img_downloader.ImgDownloader()
    key = isbn13
    img_dict = {
        key: [
            "https://example.org/foo.jpg",
            "https://example.org/bar.jpg",
        ]
    }

    mock = Mock(return_value=mock_jpg_response)
    monkeypatch.setattr(img_downloader.requests, "get", mock)

    dest = dloader.download(img_dict, str(target_directory))

    dest_files = os.listdir(dest)
    assert f"{key}.jpg" in dest_files
    assert f"{key}-1.jpg" in dest_files
    for f in dest_files:
        assert dloader.is_image(os.path.join(dest, f))


def test_download_via_isbn10(monkeypatch, mock_jpg_response, target_directory):
    """
    Given an ImgDownloader object
    AND a dictionary of images whose key is an isbn10
    AND an existing target directory
    WHEN we run the download method with the dictionary and target directory
    THEN the image urls are downloaded to the target directory
    """
    dloader = img_downloader.ImgDownloader()
    key = "1680508601"
    key = "069102555X"
    isbn13 = img_downloader.isbnlib.to_isbn13(key)
    img_dict = {
        key: [
            "https://example.org/foo.jpg",
            "https://example.org/bar.jpg",
        ]
    }

    mock = Mock(return_value=mock_jpg_response)
    monkeypatch.setattr(img_downloader.requests, "get", mock)

    dest = dloader.download(img_dict, str(target_directory))

    dest_files = os.listdir(dest)
    assert f"{isbn13}.jpg" in dest_files
    assert f"{isbn13}-1.jpg" in dest_files
    for f in dest_files:
        assert dloader.is_image(os.path.join(dest, f))


def test_download_no_target_directory(monkeypatch, isbn13, mock_jpg_response):
    """
    Given an ImgDownloader object
    AND a dictionary of images
    AND an existing target directory
    WHEN we run the download method without a target directory
    THEN the image urls are downloaded to a created target directory
    """
    dloader = img_downloader.ImgDownloader()
    key = isbn13
    img_dict = {
        key: [
            "https://example.org/foo.jpg",
            "https://example.org/bar.jpg",
        ]
    }

    mock = Mock(return_value=mock_jpg_response)
    monkeypatch.setattr(img_downloader.requests, "get", mock)

    dest = dloader.download(img_dict)

    dest_files = os.listdir(dest)
    assert f"{key}.jpg" in dest_files
    assert f"{key}-1.jpg" in dest_files
    for f in dest_files:
        assert dloader.is_image(os.path.join(dest, f))


def test_download_idempotent(
    monkeypatch, isbn13, mock_jpg_response, populated_target_directory
):
    """
    Given an ImgDownloader object
    AND a dictionary of images
    AND an existing target directory
    AND an existing product image is in the target directory
    WHEN we run the download method with the dictionary and target directory
    THEN the image urls are not re-downloaded to the target directory
    """
    dloader = img_downloader.ImgDownloader()
    key = isbn13
    img_dict = {
        key: [
            "https://example.org/foo.jpg",
            "https://example.org/bar.jpg",
        ]
    }

    mock = Mock(return_value=mock_jpg_response)
    monkeypatch.setattr(img_downloader.requests, "get", mock)

    dest = dloader.download(img_dict, str(populated_target_directory))

    mock.assert_not_called()
    dest_files = os.listdir(dest)
    assert f"{key}.jpg" in dest_files
    assert f"{key}-1.jpg" in dest_files
    for f in dest_files:
        assert dloader.is_image(os.path.join(dest, f))


def test_download_invalid_isbn(monkeypatch, mock_jpg_response, target_directory):
    """
    Given an ImgDownloader object
    AND a dictionary of images whose key is an invalid isbn
    AND an existing target directory
    WHEN we run the download method with the dictionary and target directory
    THEN the image urls are downloaded to the target directory
    """
    dloader = img_downloader.ImgDownloader()
    key = "672125069899"
    img_dict = {
        key: [
            "https://example.org/foo.jpg",
            "https://example.org/bar.jpg",
        ]
    }

    mock = Mock(return_value=mock_jpg_response)
    monkeypatch.setattr(img_downloader.requests, "get", mock)

    dest = dloader.download(img_dict, str(target_directory))

    dest_files = os.listdir(dest)
    mock.assert_called_with("https://example.org/bar.jpg", timeout=10)
    assert f"{key}.jpg" in dest_files
    assert f"{key}-1.jpg" in dest_files
    for f in dest_files:
        assert dloader.is_image(os.path.join(dest, f))


def test_download_png(monkeypatch, isbn13, mock_png_response, target_directory):
    """
    Given an ImgDownloader object
    AND a dictionary of images whose key is an isbn13
    AND contains URI for 'PNG' images
    AND an existing target directory
    WHEN we run the download method with the dictionary and target directory
    THEN the image urls are downloaded to the target directory
    """
    dloader = img_downloader.ImgDownloader()
    key = isbn13
    img_dict = {
        key: [
            "https://example.org/foo.png",
            "https://example.org/bar.png",
        ]
    }

    mock = Mock(return_value=mock_png_response)
    monkeypatch.setattr(img_downloader.requests, "get", mock)

    dest = dloader.download(img_dict, str(target_directory))

    dest_files = os.listdir(dest)
    assert f"{key}.png" in dest_files
    assert f"{key}-1.png" in dest_files
    for f in dest_files:
        assert dloader.is_image(os.path.join(dest, f))


def test_download_unsupported(
    caplog, monkeypatch, isbn13, mock_txt_response, target_directory
):
    """
    Given an ImgDownloader object
    AND a dictionary of images whose key is an isbn13
    AND contains URI for 'PNG' images
    AND an existing target directory
    WHEN we run the download method with the dictionary and target directory
    THEN the image urls are downloaded to the target directory
    """
    dloader = img_downloader.ImgDownloader()
    key = isbn13
    img_dict = {
        key: [
            "https://example.org/foo.txt",
            "https://example.org/bar.txt",
        ]
    }

    mock = Mock(return_value=mock_txt_response)
    monkeypatch.setattr(img_downloader.requests, "get", mock)

    dest = dloader.download(img_dict, str(target_directory))

    dest_files = os.listdir(dest)
    for url in img_dict[key]:
        assert (
            "root",
            logging.WARNING,
            f"ImgDownloader.download: Skipping unsupported file type in '{url}'",
        ) in caplog.record_tuples
    assert f"{key}.txt" not in dest_files
    assert f"{key}-1.txt" not in dest_files
    for f in dest_files:
        assert dloader.is_image(os.path.join(dest, f))
