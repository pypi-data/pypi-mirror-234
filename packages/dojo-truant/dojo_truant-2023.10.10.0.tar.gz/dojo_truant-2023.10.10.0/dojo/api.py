#!/usr/bin/env python3

import logging
import urllib.parse
import json
import difflib


import json_fix
import requests
import pyjq


class DAPI:
    _allowed_methods = ["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"]
    _endpoint = None
    _post_endpoint = None
    _type = "Unknown"
    _model_validation = {}
    _obj_iterate = None
    _comp_ignore_keys = ["updated", "created", "prefetch", "target_start", "limit", "offset"]

    _id_column = "id"
    _default_action = None
    _no_get = False
    _no_search = False
    _no_new = False

    def __init__(self, **kwargs):

        self.logger = logging.getLogger("DAPI")
        self.endpoint = kwargs.get("endpoint", self._endpoint)
        self.post_endpoint = kwargs.get("post_endpoint", self._post_endpoint)
        self.host = kwargs.get("host", None)
        self.type = kwargs.get("type", self._type)

        self.allowed_methods = kwargs.get("allowed_methods", self._allowed_methods)

        self.logger.debug(kwargs)

        self.kwargs = kwargs

        if kwargs.get("token", None) is None:
            if kwargs.get("username", None) is None or kwargs.get("password", None) is None:
                raise ValueError("I need a token or a username/password combination to work")
            else:
                self.token = self.get_token(username=kwargs.get("username", None),
                                            password=kwargs.get("password", None)
                                            )

                self.logger.debug("token: {}".format(self.token))

        else:
            self.token = kwargs["token"]

        self.data = kwargs.get("data", None)
        self.id = kwargs.get("id", None)
        self.multidata = None

        self.action = kwargs.get("action", self._default_action)

        if self.action == "get":

            self.get_obj()
        elif self.action == "new":

            self.new_obj()

        elif self.action == "search":

            self.search_for_obj()

    def chain_repr(self):

        return self.id

    def see_if_changes(self, wanted_state, include_gone=False, include_new=False):

        """
        See if there's any changes between the current objec and the wanted state.
        :return:
        """

        comp_ignore_keys = self.kwargs.get("comp_ignore_keys", self._comp_ignore_keys)

        current_data = self.data

        changes = list()

        new_keys = [k for k in wanted_state.keys() if k not in current_data.keys() and k not in comp_ignore_keys]
        gone_keys = [k for k in current_data.keys() if k not in wanted_state.keys() and k not in comp_ignore_keys]
        gone_keys_data = {k: current_data[k] for k in gone_keys}
        match_keys = [k for k in current_data.keys() if k in wanted_state.keys() and k not in comp_ignore_keys]

        self.logger.debug("New Keys: {}".format(new_keys))
        self.logger.debug("Gone Keys: {}".format(gone_keys))
        self.logger.debug("Match Keys: {}".format(match_keys))

        for nk in new_keys:
            if include_new is True:
                changes.append((nk, "Key exists on config but no server."))

        for gk in gone_keys:
            if include_gone is True:
                changes.append((gk, "Key exists on server but not config."))

        for mk in match_keys:

            current_mk_json = json.dumps(current_data[mk], default=str, indent=2, sort_keys=True)
            wanted_mk_json = json.dumps(wanted_state[mk], default=str, indent=2, sort_keys=True)

            if current_mk_json == wanted_mk_json:
                self.logger.debug("MK {} Checks out as good.".format(mk))
            else:
                self.logger.info("Trigger Patch, MK {} Mismatch".format(mk))

                the_diff = difflib.unified_diff(current_mk_json.splitlines(keepends=True),
                                                wanted_mk_json.splitlines(keepends=True),
                                                fromfile="current_state.json",
                                                tofile="wanted_state.json")

                diff_string = "".join(the_diff)

                self.logger.debug("The {} Diff:\n{}".format(mk, diff_string))

                changes.append((mk, diff_string))

        return changes

    def update_obj(self, update_dict):

        changes = self.see_if_changes(update_dict)

        if len(changes) == 0:
            self.logger.warning("Ignoring Update all Items are the Same")
        else:
            self.logger.info("Updating {} attributes for this object".format(len(changes)))
            update_obj = dict()
            for k, reason in changes:
                update_obj[k] = update_dict[k]

            self.logger.info("Update Object {}".format(json.dumps(update_obj)))

            data = self.api_call(endpoint=self.endpoint.safe_substitute(id=self.id),
                                 method="PATCH",
                                 json=update_obj)

            self.logger.debug("New Data : {}".format(data))


    def get_obj(self):

        '''
        Get's the Object
        :return: data
        '''

        if self.kwargs.get("no_get", self._no_get) is True:
            obj_data = None

        else:
            obj_data = self.api_call(endpoint=self.endpoint.safe_substitute(id=self.id),
                                     method="GET")

            self.logger.debug(obj_data)

        self.data = obj_data

    def new_obj(self):

        '''

        :return: id, data
        '''

        id = None
        data = None


        if self.kwargs.get("no_new", self._no_new) is True:
            id = None
            data = None
        else:
            post_kwargs = {}

            if self.validate_obj(enforce_all=True) is True:
                self.logger.debug(self.data)
                if self.kwargs.get("files", None) is None:
                    post_kwargs["json"] = self.data
                else:
                    post_kwargs["data"] = self.data
                    post_kwargs["ctype_json"] = False
                    post_kwargs["accept_json"] = False
                    post_kwargs["files"] = self.kwargs["files"]

                data = self.api_call(endpoint=self.post_endpoint,
                                     method="POST", **post_kwargs)

                if data is not None:
                    id = data[self.kwargs.get("id_column", self._id_column)]
            else:
                self.logger.error("Validation of New Object Failed")


        self.id = id
        self.data = data

    def search_for_obj(self):

        '''

        :return: id, data
        '''

        id = None
        data = None

        if self.kwargs.get("no_search", self._no_search) is True:
            id = None
            data = None
        else:

            if self.validate_obj() is True:
                search_obj_data = self.api_call(endpoint=self.post_endpoint,
                                                method="GET",
                                                params=self.data)

                #self.logger.debug(search_obj_data)

                if search_obj_data["count"] > 0:
                    if self.kwargs.get("multi", False) is True:
                        self.logger.debug("Storing Search Obj Data as Requested")
                        self.multidata = search_obj_data

                    # I've found an object
                    data = pyjq.first(self.kwargs.get("obj_iterate", self._obj_iterate),
                                      search_obj_data)
                    id = data[self.kwargs.get("id_column", self._id_column)]

                else:
                    self.logger.warning("Unable to find object with given terms.")

            else:
                self.logger.error("Unable to process search terms")

        self.id = id
        self.data = data


    def validate_obj(self, enforce_all=False):

        create_validation = self.kwargs.get("model_validation", self._model_validation)

        comp_ignore_keys = self.kwargs.get("comp_ignore_keys", self._comp_ignore_keys)

        valid = True

        for k, v in self.data.items():
            if k not in create_validation.keys() and k not in comp_ignore_keys:
                self.logger.warning("Item {} not in validation definition for {}".format(k, self.type))
                valid = False
                break
            else:
                if k in comp_ignore_keys:
                    pass
                elif "type" in create_validation[k].keys():
                    try:
                        if isinstance(v, create_validation[k]["type"]) is False:
                            self.logger.warning("Factor {} is of an incorrect type {}.".format(k, type(v)))
                            valid = False
                            break
                        else:
                            pass
                    except TypeError as te:
                        self.logger.error("Type Test for {} on {} is incorrectly specified.".format(k, self.type))
                        raise te
                # Other future validation rules

        if enforce_all is True:
            extra_keys = [k for k in self.data.keys() if k not in create_validation.keys()]
            missing_keys = [k for k in create_validation.keys() if
                            k not in self.data.keys() and create_validation[k].get("required", True) is True]

            if len(extra_keys) > 0:
                self.logger.warning("Extra Keys in Model : {}".format(extra_keys))
                valid = False

            if len(missing_keys) > 0:
                self.logger.warning("Missing Keys in Model : {}".format(missing_keys))
                valid = False
        else:
            pass

        return valid

    def __str__(self):

        """
        :return:
        """

        strv = "{} with id {}".format(self.type,
                                      self.id)

        return strv

    def __repr__(self):

        repv = "{}(id={})".format(self.__class__.__name__,
                                  self.id)

        return repv

    def __json__(self):
        '''

        :return:
        '''

        return self.id

    def get_token(self, username="admin", password="admin"):

        '''
        Use  to get a token /api/v2/api-token-auth/
        '''

        token_data = self.api_call(endpoint="api/v2/api-token-auth/",
                                   method="POST",
                                   token=False,
                                   json={"username": username,
                                         "password": password})

        return token_data["token"]

    def api_call(self,
                 endpoint=None,
                 method="GET",
                 token=True,
                 return_json=True,
                 **kwargs):

        '''
        :param endpoint: Which Endpoint to Hit, uses self.endpoint if not set
        :param method: What type of method to use, "GET"
        :param token: Use the token when making a request
        :param return_json: Default true, return json
        :param kwargs: Alternative kwargs
        :return:
        '''

        response = None

        if endpoint is None:
            endpoint = self.endpoint

        if method not in self.allowed_methods:
            raise ValueError("Unable to make method call of {}".format(method))

        this_call_url = urllib.parse.urljoin(self.host, endpoint)

        request_kwargs = dict()

        if token is True:
            request_kwargs["headers"] = {"Authorization": "Token {}".format(self.token),
                                         **request_kwargs.get("headers", {})}

        if kwargs.get("accept_json", True) is True:
            request_kwargs["headers"] = {"accept": "application/json",
                                         **request_kwargs.get("headers", {})}

        if kwargs.get("ctype_json", True) is True:
            request_kwargs["headers"] = {"Content-Type": "application/json",
                                         **request_kwargs.get("headers", {})}
        elif kwargs.get("ctype_form", False) is True:
            request_kwargs["headers"] = {"Content-Type": "multipart/form-data",
                                         **request_kwargs.get("headers", {})}



        for x in ["params", "data", "json", "headers", "cookies", "files", "timeout"]:
            if x in kwargs.keys():
                if x not in ["headers", "params"]:
                    # Not a dictionary type
                    request_kwargs[x] = kwargs[x]
                else:
                    # Is a dictionary type
                    request_kwargs[x] = {**kwargs[x], **request_kwargs.get(x, {})}

        try:
            self.logger.debug("Request kwargs: {}".format(request_kwargs))
            this_request = requests.request(method, this_call_url, **request_kwargs)
        except Exception as request_error:
            self.logger.error("Requests Error: {}".format(request_error))
        else:
            if this_request.ok is False:
                self.logger.error("Response Error Code: {}".format(this_request.status_code))
                self.logger.info("Error Response: \n{}".format(this_request.text))
            else:
                if return_json is True:
                    response = this_request.json()
                else:
                    response = this_request.text

            self.logger.debug(this_request.headers)
            self.logger.info(this_request.status_code)
            #self.logger.debug(this_request.text)

        return response
