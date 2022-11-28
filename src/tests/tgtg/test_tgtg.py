import unittest
from os import environ
from tgtg import TgtgClient
from .constants import GLOBAL_PROPERTIES, ITEM_PROPERTIES, PRICE_PROPERTIES


class TGTGAPITest(unittest.TestCase):
    def test_get_items(self):
        username = environ.get("TGTG_USERNAME", None)
        timeout = environ.get("TGTG_TIMEOUT", 60)
        access_token = environ.get("TGTG_ACCESS_TOKEN", None)
        refresh_token = environ.get("TGTG_REFRESH_TOKEN", None)
        user_id = environ.get("TGTG_USER_ID", None)

        client = TgtgClient(
            email=username,
            timeout=timeout,
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user_id,
        )

        # Tests
        items = client.get_items(favorites_only=True)
        assert len(items) > 0
        item = items[0]
        item_id = item["item"]["item_id"]
        for prop in GLOBAL_PROPERTIES:
            assert prop in item
        for prop in ITEM_PROPERTIES:
            assert prop in item["item"]
        for prop in PRICE_PROPERTIES:
            assert prop in item["item"]["price_including_taxes"]

        client.set_favorite(item_id, False)
        client.set_favorite(item_id, True)

        item = client.get_item(item_id)

        assert item["item"]["item_id"] == item_id
