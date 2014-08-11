from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings

from whats_fresh_api.models import *
from django.contrib.gis.db import models

import os
import time
import sys
import datetime
import json


class ProductViewTestCase(TestCase):

    fixtures = ['whats_fresh_api/tests/testdata/test_fixtures.json']

    def setup(self):
        self.expected_json = {
            "error": {
                "error_status": false,
                "error_name": null,
                "error_text": null,
                "error_level": null
            },
            "1": {
                "model": "whats_fresh_api.Product",
                "pk": "2",
                    "fields": {
                    "name": "Starfish Voyager",
                    "variety": "Tuna",
                    "alt_name": "The Stargazer",
                    "description": "This is one sweet fish!",
                    "origin": "The Delta Quadrant",
                    "season": "Season 1",
                    "available": true,
                    "market_price": "$33.31",
                    "link": "http://www.amazon.com/Star-Trek-Voyager-Complete-Seventh/dp/B00062IDCO/",
                    "image_id": 1,
                    "story_id": 1,
                    "created": "2014-08-08 23:27:05.568395+00:00",
                    "modified": "2014-08-08 23:27:05.568395+00:00"
                }
            },
            "2": {
                "model": "whats_fresh_api.Product",
                "pk": "1",
                "fields": {
                    "name": "Ezri Dax",
                    "variety": "Freshwater Eel",
                    "alt_name": "Jadzia",
                    "description": "That's not actually an eel, it's a symbiote.",
                    "origin": "Trill",
                    "season": "Season 7",
                    "available": true,
                    "market_price": "$32.64 per season",
                    "link": "http://www.amazon.com/Star-Trek-Deep-Space-Nine/dp/B00008KA57/",
                    "image_id": 1,
                    "story_id": 2,
                    "created": "2014-08-08 23:27:05.568395+00:00",
                    "modified": "2014-08-08 23:27:05.568395+00:00"
                }
            }
        }

    def test_url_endpoint(self):
        url = reverse('products-list')
        self.assertEqual(url, '/products')

    def test_json_equals(self):
        c = Client()
        response = c.get(reverse('products-list')).content
        parsed_answer = json.loads(response)
        expected_answer = json.loads(self.expected_json)
        self.assertTrue(parsed_answer == expected_answer)
