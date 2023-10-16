#!/usr/bin/env python3

import logging
import urllib.parse
import string

import requests

import dojo


class Engagement(dojo.DAPI):
    _endpoint = string.Template("/api/v2/engagements/${id}/")
    _post_endpoint = "/api/v2/engagements/"
    _search_endpoint = "/api/v2/engagements/"

    _model_validation = {
        "tags": {"type": list,
                                  "required": False},
        "name": {"type": str,
                 "required": False},
        "description": {"type": str,
                        "required": False},
        "version": {"type": str,
                    "required": False},
        "first_contacted": {"type": str,
                            "required": False,
                            "regex": "\d{4}-\d{2}-\d{2}"},

        "target_start": {"type": str,
                            "required": True,
                            "regex": "\d{4}-\d{2}-\d{2}"},
        "target_end": {"type": str,
                            "required": True,
                            "regex": "\d{4}-\d{2}-\d{2}"},
        "reason": {"type": str,
                   "required": False},
        "tracker": {"type": str,
                    "required": False},
        "test_strategy": {"type": str,
                          "required": False},
        "threat_model": {"type": bool,
                         "required": False},
        "api_test": {"type": bool,
                     "required": False},
        "pen_test": {"type": bool,
                     "required": False},
        "check_list": {"type": bool,
                       "required": False},
        "status": {"type": str,
                   "required": False,
                   "enum": ("Not Started", "Blocked", "Cancelled", "Completed", "In Progress", "On Hold", "Waiting for Resource")},
        "engagement_type": {"type": str,
                            "required": False,
                            "enum": ("Interactive", "CI/CD")},
        "build_id": {"type": str,
                     "required": False},
        "commit_hash": {"type": str,
                        "required": False},
        "branch_tag": {"type": str,
                       "required": False},
        "source_code_management_uri": {"type": str,
                                       "required": False},
        "deduplication_on_engagement": {"type": bool,
                                        "required": False},
        "lead": {"type": int,
                 "required": False},
        "requester": {"type": int,
                      "required": False},
        "preset": {"type": int,
                   "required": False},
        "report_type": {"type": int,
                        "required": False},
        "product": {"type": (int, dojo.Product),
                    "required": True},
        "build_server": {"type": int,
                         "required": False},
        "source_code_management_server": {"type": int,
                                          "required": False},
        "orchestration_engine": {"type": int,
                                 "required": False}
    }

    _obj_iterate = ".results[]"

    _type = "engagement"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = logging.getLogger("DAPI.Engagement")
