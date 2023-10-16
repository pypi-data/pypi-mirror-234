# -*- coding: utf-8 -*-
from alibabacloud_tea_openapi import models as open_api_models


class BaseClient:
    def __init__(self, region_id, access_key_id, access_key_secret):
        self.region_id = region_id
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.config = open_api_models.Config(access_key_id=access_key_id, access_key_secret=access_key_secret)


