#!/usr/bin/env python3

import logging
import urllib.parse
import string

import requests

import dojo


class Stub_Finding(dojo.DAPI):
    _endpoint = string.Template("/api/v2/stub_findings/${id}/")
    _post_endpoint = "/api/v2/stub_findings/"
    _search_endpoint = "/api/v2/stub_findings/"

    _model_validation = {
        "test": {"type": (int, dojo.Test),
                 "required": True},
        "title": {"type": str,
                  "required": True},
        "date": {"type": str,
                 "required": False,
                 "regex": "\d{4}-\d{2}-\d{2}"},
        "severity": {"type": str,
                     "required": False,
                     "enum": ("Critical", "High", "Medium", "Low", "Informtional")},
        "description": {"type": str,
                        "required": False}
    }

    _obj_iterate = ".results[]"

    _type = "stub_finding"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = logging.getLogger("DAPI.Stub_Finding")
