# ruff: noqa: S101
from artemis_sg import item


class TestItem:
    def test_create_item(self):
        """
        GIVEN Item class
        WHEN Item instance is created
        THEN the instance is of type item.Item
        AND has a data attribute with the given values
        AND has a data_row_num attribute
        AND has an isbn attribute
        AND has an isbn10 attribute
        """
        isbn13 = "9780802157003"
        isbn10 = "0802157009"
        expected_data = {
            "ISBN": isbn13,
            "PRICE": "$42",
            "DESCRIPTION": "cool description",
        }
        row_number = 0
        isbn_key = "ISBN"
        product = item.Item(
            list(expected_data.keys()),
            list(expected_data.values()),
            row_number,
            isbn_key,
        )

        assert isinstance(product, item.Item)
        assert product.data == expected_data
        assert product.data_row_num == row_number
        assert product.isbn == isbn13
        assert product.isbn10 == isbn10
        assert product.image_urls == []
