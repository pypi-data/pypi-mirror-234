import json
import logging
import string

from artemis_sg.item import Item


class Items:
    """
    Collection object for artemis_slide_generaor.Item objects.
    """

    # Constants
    ALPHA_LIST = tuple(string.ascii_uppercase)

    # methods
    def __init__(self, keys, value_list, isbn_key):
        """
        Instantiate Items object

        Arguments:
        keys -- list of strings to use as item keys
        value_list -- list of value lists, nested list positions correspond to keys
        isbn_key -- the key in keys that corresponds with ISBN (primary key)

        Returns:
        Items object
        """
        namespace = f"{type(self).__name__}.{self.__init__.__name__}"

        if len(keys) != len(value_list[0]):
            logging.error(f"{namespace}: Key count does not match value count.")
            raise IndexError

        self.isbn_key = isbn_key
        self.column_dict = dict(zip(keys, Items.ALPHA_LIST))

        self.items = []
        for row_num, entry in enumerate(value_list):
            self.items.append(Item(keys, entry, row_num, self.isbn_key))

    def get_items(self):
        return self.items

    def __iter__(self):
        return iter(self.items)

    def get_json_data_from_file(self, datafile):
        namespace = f"{type(self).__name__}.{self.get_json_data_from_file.__name__}"
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

    def load_scraped_data(self, datafile):
        data = self.get_json_data_from_file(datafile)
        self.set_scraped_data(data)

    def save_scraped_data(self, datafile):
        namespace = f"{type(self).__name__}.{self.save_scraped_data.__name__}"

        internal_data = self.get_scraped_data()
        external_data = self.get_json_data_from_file(datafile)
        external_data.update(internal_data)
        if external_data:
            logging.debug(f"{namespace}: attempting to open {datafile}")
            with open(datafile, "w+") as filepointer:
                logging.debug(f"{namespace}: dumping scraped data to {datafile}")
                json.dump(external_data, filepointer, indent=4)
            filepointer.close()

    def set_scraped_data(self, data):
        for isbn in data:
            item = self.find_item(isbn)
            if not item:
                continue
            item.data["DESCRIPTION"] = data[isbn]["DESCRIPTION"]
            item.image_urls = data[isbn]["image_urls"]

    def get_scraped_data(self):
        data = {}
        for item in self.items:
            if item.image_urls != []:
                data_elem = {}
                data_elem["isbn10"] = item.isbn10
                data_elem["image_urls"] = item.image_urls
                if "DESCRIPTION" in item.data:
                    data_elem["DESCRIPTION"] = item.data["DESCRIPTION"]
                data[item.isbn] = data_elem

        return data

    def find_item(self, isbn):
        for item in self.items:
            if item.isbn == isbn:
                return item
        return None

    def get_items_with_image_urls(self):
        # WARNING: this looks a scraped urls to determine if the item has images.
        #   Images may be retrieved from GCloud storage.  So, there may be cases
        #   where this method of searching leads to false positives/negatives.
        items_with_images = []
        for item in self.items:
            if item.image_urls != []:
                items_with_images.append(item)
        return items_with_images
