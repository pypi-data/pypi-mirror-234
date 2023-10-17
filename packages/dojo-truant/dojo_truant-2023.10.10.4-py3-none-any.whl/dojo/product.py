#!/usr/bin/env python3

import logging
import urllib.parse
import string

import requests

import dojo


class Product(dojo.DAPI):
    _endpoint = string.Template("/api/v2/products/${id}/")
    _post_endpoint = "/api/v2/products/"
    _search_endpoint = "/api/v2/products/"

    _model_validation = {"tags": {"type": list,
                                  "required": False},
                         "name": {"type": str},
                         "description": {"type": str},
                         "prod_numeric_grade": {"type": int,
                                                "required": False},
                         "business_criticality": {"type": str,
                                                  "required": False,
                                                  "enum": ("none", "very low", "low", "medium", "high", "very high")},
                         "platform": {"type": str,
                                      "required": False,
                                      "enum": ("web", "mobile", "iot", "desktop", "web service")},
                         "lifecycle": {"type": str,
                                       "required": False,
                                       "enum": ("retirement", "production", "construction")},
                         "origin": {"type": str,
                                    "required": False,
                                    "enum": ("outsourced", "open source", "internal", "contractor", "purchased", "third party library")},
                         "user_records": {"type": int,
                                          "required": False},
                         "revenue": {"type": str,
                                     "required": False},
                         "external_audience": {"type": bool,
                                               "required": False},
                         "internet_accessible": {"type": bool,
                                                 "required": False},
                         "enable_simple_risk_acceptance": {"type": bool,
                                                           "required": False},
                         "enable_full_risk_acceptance": {"type": bool,
                                                         "required": False},
                         "product_manager": {"type": int,
                                             "required": False},
                         "technical_contact": {"type": int,
                                               "required": False},
                         "team_manager": {"type": int,
                                          "required": False},
                         "prod_type": {"type": (int, dojo.Product_Type)},
                         "sla_configuration": {"type": int,
                                               "required": False},
                         "regulations": {"type": list,
                                         "required": False}
                         }

    _obj_iterate = ".results[]"

    _type = "product"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = logging.getLogger("DAPI.Product")
