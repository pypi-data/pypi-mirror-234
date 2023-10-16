#!/usr/bin/env python3

import logging
import urllib.parse
import string
import io

import requests

import dojo


class Import_Scan(dojo.DAPI):
    _endpoint = string.Template("/api/v2/import-scan/${id}/")
    _post_endpoint = "/api/v2/import-scan/"
    _search_endpoint = "/api/v2/import-scan/"

    _no_get = True
    _no_search = True
    _default_action = "new"

    # Disable get, disable search, disable put?

    _model_validation = {
        "scan_date": {"type": str,
                      "required": False},
        "minimum_severity": {"type": str,
                             "required": False,
                             "enum": ("Info", "Low", "Medium", "High", "Critical")},
        "active": {"type": bool,
                   "required": True},
        "verified": {"type": bool,
                     "required": True},
        "scan_type": {"type": str,
                      "required": True},
        "endpoint_to_add": {"type": int,
                            "required": False},
        "product_type_name": {"type": "string",
                              "required": False},
        "product_name": {"type": str,
                         "required": False},
        "engagement_name": {"type": str,
                            "required": False},
        "engagement_end_date": {"type": str,
                                "required": False},
        "source_code_management_uri": {"type": str,
                                       "required": False},
        "engagement": {"type": (dojo.Engagement, int),
                       "required": False},
        "test_title": {"type": str,
                       "required": False},
        "auto_create_context": {"type": bool,
                                "required": False},
        "deduplication_on_engagement": {"type": bool,
                                        "required": False},
        "lead": {"type": int,
                 "required": False},
        "tags": {"type": list,
                 "required": False},
        "close_old_findings": {"type": bool,
                               "required": False},
        "close_old_findings_product_scope": {"type": bool,
                                             "required": False},
        "push_to_jira": {"type": bool,
                         "required": False},
        "environment": {"type": str,
                        "required": False},
        "version": {"type": str,
                    "required": False},
        "build_id": {"type": str,
                     "required": False},
        "branch_tag": {"type": str,
                       "required": False},
        "commit_hash": {"type": str,
                        "required": False},
        "api_scan_configuration": {"type": int,
                                   "required": False},
        "service": {"type": str,
                    "required": False},

        "group_by": {"type": str,
                     "required": False,
                     "enum": ("component_name", "component_name+component_version", "file_path", "finding_title")},
        "create_finding_groups_for_all_findings": {"type": bool,
                                                   "required": False}
    }

    _obj_iterate = ".ImportScan[]"

    _type = "finding"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = logging.getLogger("DAPI.Finding")

        # def add_note(self, note_text):


