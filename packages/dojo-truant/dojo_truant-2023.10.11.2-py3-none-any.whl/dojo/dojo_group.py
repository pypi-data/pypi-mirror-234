#!/usr/bin/env python3

import logging
import urllib.parse
import string

import requests

import dojo


class Dojo_Group(dojo.DAPI):
    _endpoint = string.Template("/api/v2/dojo_groups/${id}/")
    _post_endpoint = "/api/v2/dojo_groups/"
    _search_endpoint = "/api/v2/dojo_groups/"

    _model_validation = {"configuration_permissions": {"type": list,
                                                       "required": False},
                         "name": {"type": str},
                         "description": {"type": str,
                                         "requried": False},
                         "social_provider": {"type": str,
                                             "required": False}
                         }

    _obj_iterate = ".results[]"

    _type = "dojo_group"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = logging.getLogger("DAPI.Dojo_Group")
