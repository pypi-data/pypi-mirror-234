#!/usr/bin/env python3

import logging
import urllib.parse
import string

import requests

import dojo


class Jira_Product_Configuration(dojo.DAPI):
    _endpoint = string.Template("/api/v2/jira_product_configurations/${id}/")
    _post_endpoint = "/api/v2/jira_product_configurations/"
    _search_endpoint = "/api/v2/jira_product_configurations/"

    _model_validation = {"project_key": {"type": str,
                                         "required": True},
                         "issue_template_dir": {"type": str,
                                                "required": False},
                         "component": {"type": str,
                                      "requried": False},
                         "custom_fields": {"type": dict,
                                           "required": False},
                         "jira_labels": {"type": str,
                                         "required": False},
                         "add_vulnerability_id_to_jira_label": {"type": bool,
                                                                "required": False},
                         "push_all_issues": {"type": bool,
                                             "required": False},
                         "enable_engagement_epic_mapping": {"type": bool,
                                                            "required": False},
                         "push_notes": {"type": bool,
                                        "required": False},
                         "product_jira_sla_notifications": {"type": bool,
                                                            "required": False},
                         "risk_acceptance_expiration_notification": {"type": bool,
                                                                     "required": False},
                         "jira_instance": {"type": int,
                                           "required": True},
                         "product": {"type": int,
                                     "required": False},
                         "engagement": {"type": int,
                                        "required": False}
                         }

    _obj_iterate = ".results[]"

    _type = "jira_product_configuration"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = logging.getLogger("DAPI.Jira_Product_Configuration")
