#!/usr/bin/env python3

import logging
import pyjq


class api_multi:

    '''
    Hit an endpoint for a given type and give me a container with all of the objects in that list

    Useful for "give me all the controls".
    '''

    def __init__(self, type=None, **kwargs):

        self.logger = logging.getLogger("multi_api")
        self.type = type

        if self.type is None:
            raise ValueError("I need a type object to multify upon.")

        self.kwargs = kwargs

        self.base_search_obj = self.type(**self.kwargs,
                                         action="search",
                                         multi=True)

        self.data = self.base_search_obj.multidata
