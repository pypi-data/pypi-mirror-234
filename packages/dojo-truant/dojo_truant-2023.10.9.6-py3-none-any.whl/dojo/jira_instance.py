#!/usr/bin/env python3

import logging
import urllib.parse
import string

import requests

import dojo


class Jira_Instance(dojo.DAPI):
    _endpoint = string.Template("/api/v2/jira_instances/${id}/")
    _post_endpoint = "/api/v2/jira_instances/"
    _search_endpoint = "/api/v2/jira_instances/"

    _model_validation = {"configuration_name": {"type": str,
                                                "required": True},
                         "url": {"type": str},
                         "username": {"type": str,
                                      "requried": True},
                         "password": {"type": str,
                                      "required": True},
                         "default_issue_type": {"type": str,
                                                "required": False},
                         "issue_tempalte_dir": {"type": str,
                                                "required": False},
                         "epic_name_id": {"type": int,
                                          "required": True},
                         "open_status_key": {"type": int,
                                             "required": True},
                         "close_status_key": {"type": int,
                                              "required": True},
                         "info_mapping_severity": {"type": str,
                                                   "required": True},
                         "low_mapping_severity": {"type": str,
                                                  "required": True},
                         "medium_mapping_severity": {"type": str,
                                                     "required": True},
                         "high_mapping_severity": {"type": str,
                                                   "required": True},
                         "critical_mapping_severity": {"type": str,
                                                       "required": True},
                         "finding_text": {"type": str,
                                          "required": False},
                         "accepted_mapping_resolution": {"type": str,
                                                         "required": False},
                         "false_positive_mapping_resolution": {"type": str,
                                                               "required": False},
                         "global_jira_sla_notification": {"type": bool,
                                                               "required": False},
                         "finding_jira_sync": {"type": bool,
                                               "required": False}

                         }

    _obj_iterate = ".results[]"

    _type = "jira_instance"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = logging.getLogger("DAPI.Jira_Instance")
