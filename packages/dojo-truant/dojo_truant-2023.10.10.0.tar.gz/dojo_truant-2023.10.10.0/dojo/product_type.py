#!/usr/bin/env python3

import logging
import urllib.parse
import string

import requests

import dojo


class Product_Type(dojo.DAPI):
    _endpoint = string.Template("/api/v2/product_types/${id}/")
    _post_endpoint = "/api/v2/product_types/"
    _search_endpoint = "/api/v2/product_types/"

    _model_validation = {"name": {"type": str},
                          "description": {"type": str},
                          "critical_product": {"type": bool},
                          "key_product": {"type": bool}
                          }

    _obj_iterate = ".results[]"

    _type = "product_type"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = logging.getLogger("DAPI.Product_Type")
