#!/usr/bin/env python3

import logging
import urllib.parse
import string

import requests

import dojo

class Test_Type(dojo.DAPI):
    _endpoint = string.Template("/api/v2/test_types/${id}/")
    _post_endpoint = "/api/v2/test_types/"
    _search_endpoint = "/api/v2/test_types/"

    _model_validation = {
        "tags": {"type": list,
                 "required": False},
        "name": {"type": str,
                  "required": True},
        "static_tool": {"type": bool,
                      "required": False},
        "dynamic_tool": {"type": bool,
                        "required": False},
        "active": {"type": bool,
                         "required": False},
    }

    _obj_iterate = ".results[]"

    _type = "test_type"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = logging.getLogger("DAPI.Test")
