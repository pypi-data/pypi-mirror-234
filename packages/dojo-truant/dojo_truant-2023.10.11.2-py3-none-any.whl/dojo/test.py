#!/usr/bin/env python3

import logging
import urllib.parse
import string

import requests

import dojo

class Test(dojo.DAPI):
    _endpoint = string.Template("/api/v2/tests/${id}/")
    _post_endpoint = "/api/v2/tests/"
    _search_endpoint = "/api/v2/tests/"

    _model_validation = {
        "engagement": {"type": (int, dojo.Engagement),
                       "required": True},
        "tags": {"type": list,
                 "required": False},
        "notes": {"type": list,
                  "required": False},
        "scan_type": {"type": str,
                      "required": False},
        "title": {"type": str,
                  "required": False},
        "description": {"type": str,
                        "required": False},
        "target_start": {"type": str,
                         "required": True,
                         "regex": "\d{4}-\d{2}-\d{2}"},
        "target_end": {"type": str,
                       "required": True,
                       "regex": "\d{4}-\d{2}-\d{2}"},
        "percent_complete": {"type": int,
                             "required": False},
        "version": {"type": str,
                    "required": False},
        "build_id": {"type": str,
                     "required": False},
        "commit_hash": {"type": str,
                        "required": False},
        "branch_tag": {"type": str,
                       "required": False},
        "lead": {"type": int,
                 "required": False},
        "test_type": {"type": (int, dojo.Test_Type),
                      "required": False},
        "environment": {"type": (int, dojo.Development_Environment),
                        "required": False},
        "api_scan_configuration": {"type": int,
                                   "required": False}
    }

    _obj_iterate = ".results[]"

    _type = "test"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = logging.getLogger("DAPI.Test")
