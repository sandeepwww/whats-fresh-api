from django.test import TestCase
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

from whats_fresh_api.models import *
from django.contrib.gis.db import models

import os
import time
import sys
import datetime


class ImageTestCase(TestCase):
    def setUp(self):
        self.expected_fields = {
            'image': models.ImageField,
            'caption': models.TextField,
            'created': models.DateTimeField,
            'modified': models.DateTimeField,
            u'id': models.AutoField
        }

    def test_fields_exist(self):
        model = models.get_model('whats_fresh_api', 'Image')
        for field, field_type in self.expected_fields.items():
            self.assertEqual(
                field_type, type(model._meta.get_field_by_name(field)[0]))

    def test_no_additional_fields(self):
        fields = Image._meta.get_all_field_names()
        self.assertTrue(sorted(fields) == sorted(self.expected_fields.keys()))

    def test_created_modified_fields(self):
        self.assertTrue(Image._meta.get_field('modified').auto_now)
        self.assertTrue(Image._meta.get_field('created').auto_now_add)