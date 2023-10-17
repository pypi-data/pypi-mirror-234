import logging

import isbnlib


class Item:
    def __init__(self, keys, values, row_num, isbn_key):
        keys = [x.strip().upper() for x in keys]
        self.data = dict(zip(keys, values))
        self.data_row_num = row_num
        self.isbn_key = isbn_key
        self.isbn = str(self.data[isbn_key])
        self.isbn10 = isbnlib.to_isbn10(self.isbn)
        self.image_urls = []
        if "DESCRIPTION" not in self.data:
            self.data["DESCRIPTION"] = ""
        self._sort_data()

    def _sort_data(self):
        namespace = f"{type(self).__name__}.{self._sort_data.__name__}"

        def sort_order(e):
            defined_order = [
                "TITLE",
                "SUBTITLE",
                "AUTHOR",
                "PUBLISHER",
                "PUB DATE",
                "PUBLISHERDATE",
                "FORMAT",
            ]
            if e in defined_order:
                return defined_order.index(e)
            return 99

        sorted_keys = list(self.data.keys())
        # sort by defined order
        sorted_keys.sort(key=sort_order)
        # move ISBN and DESCRIPTION to end of list
        sorted_keys.sort(key=self.isbn_key.__eq__)
        sorted_keys.sort(key="DESCRIPTION".__eq__)
        logging.debug(f"{namespace}: Sorted keys: {sorted_keys}")

        sorted_data = {key: self.data[key] for key in sorted_keys}
        self.data = sorted_data
