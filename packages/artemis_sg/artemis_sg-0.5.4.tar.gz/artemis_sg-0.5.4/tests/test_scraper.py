# ruff: noqa: S101
import logging
import time
from unittest.mock import Mock

from selenium.common.exceptions import NoSuchElementException

from artemis_sg import scraper


def test_get_driver(monkeypatch):
    """
    GIVEN a webdriver object
    WHEN `get_driver` is called
    THEN a `Chrome` is called on the webdriver object
    AND a chrome driver is returned
    """
    driver = Mock(name="mock_driver")
    chrome = Mock(name="mock_chrome")
    driver.Chrome.return_value = chrome
    monkeypatch.setattr(scraper, "webdriver", driver)

    d = scraper.get_driver()

    assert d == chrome


def test_main(monkeypatch, valid_datafile):
    """
    GIVEN a webdriver object
    WHEN `get_driver` is called
    THEN a `Chrome` is called on the webdriver object
    AND a chrome driver is returned
    """
    mock = Mock()
    vendor = Mock(name="mock_vendor")
    vendor.isbn_key = "ISBN"
    mock.Vendor.return_value = vendor
    spreadsheet = Mock(name="mock_spreadsheet")
    spreadsheet.get_sheet_data.return_value = [["ISBN"], ["1234"]]
    monkeypatch.setattr(scraper, "vendor", mock)
    monkeypatch.setattr(scraper, "spreadsheet", spreadsheet)
    driver = Mock(name="mock_driver")
    scrapr = Mock(name="mock_scraper")
    scrapr.scrape_description.return_value = "Be excellent to each other."
    scrapr.scrape_item_image_urls.return_value = ["Bill", "Ted"]
    monkeypatch.setattr(scraper, "get_driver", lambda *args: driver)
    monkeypatch.setattr(scraper, "AmznScraper", lambda *args: scrapr)

    scraper.main("my_vendor", "my_workbook", "worksheet", valid_datafile)

    driver.quit.assert_called  # noqa: B018


class TestBaseScraper:
    def test_create_scraper(self):
        """
        GIVEN BaseScraper class
        WHEN we create Scraper object with driver and url
        THEN object's selenium_driver and base_url attributes
             are set to the given values
        """
        scrapr = scraper.BaseScraper("driver", "baseUrl")

        assert scrapr.selenium_driver == "driver"
        assert scrapr.base_url == "baseUrl"


class TestAmznScraper:
    def test_scrape_description_with_review(self, monkeypatch):
        """
        GIVEN a AmznScraper object with webdriver and amazon url
        AND Amazon item page with editorial review is loaded in browser
        WHEN we call scrape_description() on object
        THEN the result is the editorial review without the first two lines
        """
        review_text = """Editorial Reviews
Review
Praise for Earthlings:
A New York Times Book Review Editors’ Choice
Named a Best Book of the Year by TIME and Literary Hub
Named a Most Anticipated Book by the New York Times, TIME, USA Today, \
Entertainment Weekly, the Guardian, Vulture, Wired, Literary Hub, Bustle, \
Popsugar, and Refinery29
“To Sayaka Murata, nonconformity is a slippery slope . . . Reminiscent of certain \
excellent folk tales, expressionless prose is Murata’s trademark . . . \
In Earthlings, being an alien is a simple proxy for being alienated. The characters \
define themselves not by a specific notion of what they are—other—but by a general \
idea of what they are not: humans/breeders . . . The strength of [Murata’s] voice \
lies in the faux-naïf lens through which she filters her dark view of humankind: \
We earthlings are sad, truncated bots, shuffling through the world in a dream of \
confusion.”—Lydia Millet, New York Times Book Review"""  # noqa: RUF001

        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem", text=review_text)
        driver.find_element.return_value = elem
        scrapr = scraper.AmznScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        scrapr.load_item_page("item_number")
        description = scrapr.scrape_description()

        expected_text = review_text.splitlines()
        expected_text.pop(0)
        expected_text.pop(0)
        expected_text = "\n".join(expected_text)
        assert description == expected_text

    def test_scrape_description_without_review(self, monkeypatch):
        """
        GIVEN Amazon item page without editorial review is loaded
        WHEN scrape_description is executed
        THEN description is returned
        """

        whole_description = (
            "As a child, Natsuki doesn’t fit into her family. "  # noqa: RUF001
            "Her parents favor her sister, and her best friend "
            "is a plush toy hedgehog named Piyyut who has "
            "explained to her that he has come from the planet "
            "Popinpobopia on a special quest to help her save "
            "the Earth."
        )

        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem", text=whole_description)
        driver.find_element.side_effect = [
            NoSuchElementException,
            elem,
        ]
        scrapr = scraper.AmznScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        scrapr.load_item_page("item_number")
        description = scrapr.scrape_description()

        assert "As a child" in description

    def test_scrape_item_image_urls(self, monkeypatch):
        """
        GIVEN Amazon item page with multiple item images
        WHEN scrape_item_image_urls is executed
        THEN a list of urls is returned
        """
        elem_text = (
            "https://m.media-example.com/images/I/image-0._AC_SX75_CR,0,0,75,75_.jpg"
        )

        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem", text=elem_text)
        driver.find_element.side_effect = [
            elem,
            elem,
            elem,
            NoSuchElementException,
        ]
        elem.find_element.return_value = elem
        elem.get_attribute.return_value = "https://m.media-example.com/images/I/image-enterNumberHere._AC_SX75_CR,0,0,75,75_.jpg"
        scrapr = scraper.AmznScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)
        monkeypatch.setattr(scrapr, "timeout", 0)
        monkeypatch.setattr(time, "sleep", lambda x: None)

        scrapr.load_item_page("item_number")
        urls = scrapr.scrape_item_image_urls()

        assert isinstance(urls, list)
        assert (
            "https://m.media-example.com/images/I/image-enterNumberHere.jpg" in urls[0]
        )


class TestTBScraper:
    def test_scrape_description(self, monkeypatch):
        """
        GIVEN TB item page
        WHEN scrape_description is executed
        THEN description is returned
        AND 'NO AMAZON SALES' has been removed from it
        """
        whole_description = """NO AMAZON SALES

Discover the mystery and power of the natural and human worlds in this \
beautifully illustrated coloring book.

Featuring tarot cards, healing herbs and flowers, mandalas, and curious \
creatures of the night, Believe in Magic is a spellbinding celebration \
of modern witchcraft with a focus on healing, mindfulness, and meditation."""

        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem", text=whole_description)
        driver.find_element.return_value = elem
        scrapr = scraper.TBScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        scrapr.load_item_page("item_number")
        description = scrapr.scrape_description()

        assert "NO AMAZON SALES" not in description
        assert description.startswith("Discover the mystery")

    def test_scrape_item_image_urls(self, monkeypatch):
        """
        GIVEN TB item page
        WHEN scrape_item_image_urls is executed
        THEN a URL list is returned
        AND the list contains the expected URL
        """
        url = "http://example.org/foo/bar.jpg"
        style = f'This is a URL "{url}"'

        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem")
        driver.find_element.side_effect = [
            elem,
            elem,
            elem,
            elem,
            elem,
            NoSuchElementException,
            NoSuchElementException,
            NoSuchElementException,
            NoSuchElementException,
            NoSuchElementException,
            NoSuchElementException,
            NoSuchElementException,
        ]
        elem.get_attribute.side_effect = [
            style,
            NoSuchElementException,
        ]
        scrapr = scraper.TBScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)
        monkeypatch.setattr(scrapr, "timeout", 0)
        monkeypatch.setattr(time, "sleep", lambda x: None)

        urls = scrapr.scrape_item_image_urls()

        assert len(urls) > 0
        assert url in urls

    def test_login(self, capsys, monkeypatch):
        """
        GIVEN TB login page is loaded
        WHEN `login` is executed
        THEN user input message is displayed
        """
        expected_output = "USER INPUT REQUIRED"

        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem")
        driver.find_element.return_value = elem
        scrapr = scraper.TBScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        scrapr.load_login_page()

        scrapr.login()
        captured = capsys.readouterr()
        assert expected_output in captured.out

    def test_impersonate(self, monkeypatch):
        """
        GIVEN TBScraper instance
        WHEN `impersonate` is executed with a given valid email
        THEN the result is True
        AND the email has been searched for via the 'customers-grid' XPATH
        """
        email = "foo@example.org"
        email_xpath = (
            f"//div[@id='customers-grid']/table/tbody/tr/td/a[text()='{email}']"
        )

        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem")
        driver.find_element.return_value = elem
        driver.find_elements.return_value = [elem]

        scrapr = scraper.TBScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        res = scrapr.impersonate(email)

        assert res is True
        driver.find_element.assert_any_call("xpath", email_xpath)

    def test_impersonate_multiple_customer_records(self, caplog, monkeypatch):
        """
        GIVEN TBScraper instance
        AND an email associated with multiple customer records
        WHEN `impersonate` is executed with that email
        THEN an exception is thrown
        """
        email = "foo@example.org"
        email_xpath = (
            f"//div[@id='customers-grid']/table/tbody/tr/td/a[text()='{email}']"
        )

        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem")
        driver.find_element.return_value = elem
        driver.find_elements.return_value = [elem, elem]

        scrapr = scraper.TBScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        try:
            res = scrapr.impersonate(email)
            driver.find_element.assert_any_call("xpath", email_xpath)
            assert res is True
        except Exception:
            assert (
                "root",
                logging.ERROR,
                (
                    "TBScraper.impersonate: Found multiple customer records for "
                    f"email '{email}' to impersonate"
                ),
            ) in caplog.record_tuples

    def test_add_to_cart(self, monkeypatch):
        """
        GIVEN TB item page
        WHEN add_to_cart is executed with a given quantity
        THEN the cart contains the given quantity of the item
        """
        qty = "42"
        available = "999"

        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem", text=f"Availability: {available} in stock")
        driver.find_element.return_value = elem
        scrapr = scraper.TBScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        res = scrapr.add_to_cart(qty)

        assert res == int(qty)

    def test_add_to_cart_adjust_qty(self, monkeypatch):
        """
        GIVEN TB item page
        WHEN add_to_cart is executed with a given quantity
             that is greater than available
        THEN the available quantity is returned
        """
        qty = "42"
        available = "10"

        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem", text=f"Availability: {available} in stock")
        driver.find_element.return_value = elem
        scrapr = scraper.TBScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        res = scrapr.add_to_cart(qty)

        assert res == int(available)

    def test_load_cart_page(self, monkeypatch):
        """
        GIVEN an TBScraper object
        WHEN `load_cart_page` is executed on that object
        THEN the result is True
        """
        driver = Mock(name="mock_driver")
        scrapr = scraper.TBScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        res = scrapr.load_cart_page()

        assert res

    def test_search_item_num(self, monkeypatch):
        """
        GIVEN an TBScraper object
        WHEN `search_item_num` is executed on that object
        THEN the expected item number is returned
        """
        driver = Mock(name="mock_driver")
        scrapr = scraper.TBScraper(driver)
        elem = Mock(name="mock_elem")
        elem.get_attribute.return_value = "/p/123456789/"
        driver.find_element.return_value = elem
        driver.find_elements.return_value = [elem, elem, elem]
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        res = scrapr.search_item_num("foo")

        assert res == "123456789"


class TestSDScraper:
    def test_scrape_description(self, monkeypatch):
        """
        GIVEN SD item page
        WHEN scrape_description is executed
        THEN description is returned
        """
        expected_description = "Hello, World!"

        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem", text=expected_description)
        driver.find_element.return_value = elem
        scrapr = scraper.SDScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        scrapr.load_item_page("item_number")
        description = scrapr.scrape_description()

        assert description == expected_description

    def test_scrape_item_image_urls(self, monkeypatch):
        """
        GIVEN SD item page
        WHEN scrape_item_image_urls is executed
        THEN a URL list is returned
        AND the list contains the expected URL
        """

        url = "http://example.org/foo/bar.jpg"

        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem")
        driver.find_element.return_value = elem
        driver.find_elements.return_value = [elem, elem, elem]
        elem.get_attribute.return_value = url
        scrapr = scraper.SDScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        scrapr.load_item_page("item_number")
        urls = scrapr.scrape_item_image_urls()
        assert len(urls) > 0
        assert url in urls

    def test_login(self, capsys, monkeypatch):
        """
        GIVEN SD login page is loaded
        WHEN `login` is executed
        THEN user input message is displayed
        """
        expected_output = "USER INPUT REQUIRED"

        driver = Mock(name="mock_driver")
        scrapr = scraper.SDScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        scrapr.load_login_page()

        scrapr.login()
        captured = capsys.readouterr()
        assert expected_output in captured.out

    def test_add_to_cart(self, monkeypatch):
        """
        GIVEN SD item page
        AND user is logged into SD
        WHEN add_to_cart is executed with a given quantity
        THEN the given quantity is returned
        """
        qty = "42"
        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem", text="Add to cart")
        driver.find_element.return_value = elem
        driver.find_elements.return_value = [elem, elem, elem]
        elem.get_attribute.return_value = "foo"
        scrapr = scraper.SDScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        scrapr.load_login_page()

        res = scrapr.add_to_cart(qty)

        assert res == int(qty)

    def test_add_to_cart_adjust_qty(self, monkeypatch):
        """
        GIVEN SD item page
        AND user is logged into SD
        WHEN add_to_cart is executed with a given quantity
             that is greater than available
        THEN the available quantity is returned
        """
        qty = "42"
        available = 10

        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem", text="Add to cart")
        driver.find_element.return_value = elem
        driver.find_elements.return_value = [elem, elem]
        elem.find_element.return_value = elem
        elem.get_attribute.return_value = f"{available} in stock"
        scrapr = scraper.SDScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        scrapr.load_login_page()

        res = scrapr.add_to_cart(qty)

        assert res == available

    def test_load_cart_page(self, monkeypatch):
        """
        GIVEN an SDScraper object
        WHEN `load_cart_page` is executed on that object
        THEN the result is True
        """
        driver = Mock(name="mock_driver")
        scrapr = scraper.SDScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        res = scrapr.load_cart_page()

        assert res


class TestGJScraper:
    def test_scrape_description(self, monkeypatch):
        """
        GIVEN GJ item page
        WHEN scrape_description is executed
        THEN description is returned
        """
        expected_description = "Hello, World!"

        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem", text=expected_description)
        driver.find_element.return_value = elem
        elem.find_element.return_value = elem
        driver.find_elements.return_value = [elem, elem]
        scrapr = scraper.GJScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        scrapr.load_item_page("item_number")
        description = scrapr.scrape_description()

        assert description == expected_description

    def test_scrape_item_image_urls(self, monkeypatch):
        """
        GIVEN GJ item page
        WHEN scrape_item_image_urls is executed
        THEN a URL list is returned
        AND the list contains the expected URL
        """

        url = "http://example.org/foo/bar.jpg"

        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem", text="foo")

        driver.find_element.return_value = elem
        elem.find_element.return_value = elem
        driver.find_elements.return_value = [elem, elem]
        elem.get_attribute.return_value = url
        scrapr = scraper.GJScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        scrapr.load_item_page("item_number")
        urls = scrapr.scrape_item_image_urls()

        assert len(urls) > 0
        assert url in urls

    def test_login(self, capsys, monkeypatch):
        """
        GIVEN GJ login page
        WHEN login is executed
        THEN user input message is displayed
        """
        expected_output = "USER INPUT REQUIRED"

        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem")
        driver.find_element.return_value = elem
        scrapr = scraper.GJScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        scrapr.load_login_page()

        scrapr.login()
        captured = capsys.readouterr()
        assert expected_output in captured.out

    def test_add_to_cart(self, monkeypatch):
        """
        GIVEN GJ item page
        AND user is logged into GJ
        WHEN add_to_cart is executed with a given quantity
        THEN the cart contains the given quantity of the item
        """
        qty = "42"
        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem", text="foo")

        driver.find_element.return_value = elem
        elem.find_element.return_value = elem
        scrapr = scraper.GJScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        scrapr.load_login_page()

        res = scrapr.add_to_cart(qty)

        assert res == int(qty)

    def test_add_to_cart_adjust_qty(self, monkeypatch):
        """
        GIVEN GJ item page
        AND user is logged into GJ
        WHEN add_to_cart is executed with a given quantity
             that is greater than available
        THEN the cart contains the available quantity of the item
        """
        qty = "42"
        available = 10

        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem", text=f"{available} in stock")
        driver.find_element.return_value = elem
        elem.find_element.return_value = elem
        scrapr = scraper.GJScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        scrapr.load_login_page()

        res = scrapr.add_to_cart(qty)

        assert res == available

    def test_load_cart_page(self, monkeypatch):
        """
        GIVEN an GJScraper object
        WHEN `load_cart_page` is executed on that object
        THEN the result is True
        """
        driver = Mock(name="mock_driver")
        scrapr = scraper.GJScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        res = scrapr.load_cart_page()

        assert res

    def test_scrape_error_msg(self, monkeypatch):
        """
        GIVEN GJScraper instance
        WHEN scrape_error_mgs is executed
        THEN the expected message is returned
        """
        driver = Mock(name="mock_driver")
        elem = Mock(name="mock_elem", text="foo")

        driver.find_element.return_value = elem
        scrapr = scraper.GJScraper(driver)
        monkeypatch.setattr(scrapr, "delay", lambda *args: None)

        result = scrapr.scrape_error_msg()

        assert result == "foo"


def test_scrape_item(monkeypatch):
    """
    GIVEN a scraper object
    AND a item object
    WHEN I call scraper.scrape_item with scraper and item
    THEN the item.image_urls are updated with expected data
    AND the item.description is updated with expected data
    """
    expected_image_urls = ["no", "way"]
    expected_description = "Dude!"

    mock_scraper = Mock()
    mock_scraper.scrape_item_image_urls.return_value = expected_image_urls
    mock_scraper.scrape_description.return_value = expected_description

    description, image_urls = scraper.scrape_item(mock_scraper, "12345")

    assert description == expected_description
    assert image_urls == expected_image_urls
