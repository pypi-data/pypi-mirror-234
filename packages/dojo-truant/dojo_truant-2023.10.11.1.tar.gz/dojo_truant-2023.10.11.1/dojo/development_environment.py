#!/usr/bin/env python3

import logging
import urllib.parse
import string

import requests
import pyjq

import dojo

class Development_Environment(dojo.DAPI):
    _endpoint = string.Template("/api/v2/development_enviornments/${id}/")
    _post_endpoint = "/api/v2/development_environments/"
    _search_endpoint = "/api/v2/development_environments/"

    _model_validation = {
        "name": {"type": str,
                  "required": True},
    }

    _obj_iterate = ".results[]"

    _type = "development_environment"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.logger = logging.getLogger("DAPI.Test")


    def search_for_obj(self):

        '''
        Override the default search_for_obj endpoint /development_environment doesn't allow filtering by name in the api
        TODO:: Report this as a bug

        :return: id, data
        '''

        id = None
        data = None

        if self.validate_obj() is True:
            search_obj_data = self.api_call(endpoint=self.post_endpoint,
                                            method="GET",
                                            params=self.data)

            self.logger.debug(search_obj_data)

            if search_obj_data["count"] > 0:
                # I've found an object
                for x in pyjq.all(self.kwargs.get("obj_iterate", self._obj_iterate), search_obj_data):
                    if x["name"] == search_obj_data.get("name", None):
                        data = x
                        id = data[self.kwargs.get("id_column", self._id_column)]
                        break
            else:
                self.logger.warning("Unable to find object with given terms.")

        else:
            self.logger.error("Unable to process search terms")

        self.id = id
        self.data = data