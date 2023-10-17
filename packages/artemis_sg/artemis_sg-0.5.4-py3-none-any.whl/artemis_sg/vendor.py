import logging
import sys

from artemis_sg.config import CFG


class Vendor:
    def __init__(self, code):
        self.vendor_code = code
        self.vendor_name = ""
        self.isbn_key = ""

    def _filter_database_data(self, all_data):
        namespace = f"{type(self).__name__}.{self._filter_database_data.__name__}"
        try:
            return next(
                (item for item in all_data if item["code"] == self.vendor_code), None
            )
        except KeyError:
            logging.error(f"{namespace}: Vendor code not found in database")
            sys.exit(1)

    def set_vendor_data(self):
        """Create Vendor object class"""
        namespace = f"{type(self).__name__}.{self.set_vendor_data.__name__}"

        all_data = CFG["asg"]["vendors"]
        vendor_data = self._filter_database_data(all_data)
        logging.debug(f"{namespace}: Vendor data is: '{vendor_data}'")
        self.vendor_name = vendor_data["name"]
        self.isbn_key = vendor_data["isbn_key"].upper()
