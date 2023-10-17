#!/usr/bin/env python3

import logging
import urllib.parse
import string

import requests

import dojo


class Risk_Acceptance(dojo.DAPI):
    _endpoint = string.Template("/api/v2/risk_acceptance/${id}/")
    _post_endpoint = "/api/v2/risk_acceptance/"
    _search_endpoint = "/api/v2/risk_acceptance/"

    _model_validation = {
        "name": {"type": str,
                "required": True},
        "recommendation": {"type": str,
                        "required": False},
        "decision": {"type": str,
                    "required": False},
        "path": {"type": str,
                "required": False},
        "recommendation_details": {"type": str,
                                "required": False},
        "decision_details": {"type": str,
                            "required": False},
        "accepted_by": {"type": str,
                        "required": False},
        "expiration_date": {"type": str,
                            "required": True,
                            "regex": "\d{4}-\d{2}-\d{2}"},
        "expiration_date_warned": {"type": str,
                                "required": False,
                                "regex": "\d{4}-\d{2}-\d{2}"},
        "expiration_date_handled": {"type": str,
                                "required": False,
                                "regex": "\d{4}-\d{2}-\d{2}"},
        "reactivate_expired": {"type": bool,
                            "required": False},
        "restart_sla_expired": {"type": bool,
                                "required": False},
        "created": {"type": str,
                    "required": False,
                    "regex": "\d{4}-\d{2}-\d{2}"},
        "updated": {"type": str,
                    "required": False,
                    "regex": "\d{4}-\d{2}-\d{2}"},
        "owner": {"type": int,
                "required": False},
        "accepted_findings": {"type": list,
                            "required": False},
        "notes":{"type": list,
                 "required": False}
    }

    _obj_iterate = ".results[]"

    _type = "risk_acceptance"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = logging.getLogger("DAPI.RiskAcceptance")
