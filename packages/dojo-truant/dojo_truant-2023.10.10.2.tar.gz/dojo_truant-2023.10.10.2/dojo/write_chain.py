#!/usr/bin/env python3

import logging
import json_fix
import json
import string

import dojo



def expand_data(data, template):

    """

    :param data:
    :return:
    """

    logger = logging.getLogger("expand_data")

    expanded_data = None
    expanded_template = dict()

    for tk, tv in template.items():
        if isinstance(tk, str) and tk.startswith("N"):
            expanded_template[tk] = tv.chain_repr()
        elif isinstance(tk, int):
            expanded_template["I{}".format(tk)] = tv.chain_repr()
        else:
            pass
            #  Something else is happening here

    if isinstance(data, dict):
        expanded_data = dict()
        for k, v in data.items():
            if isinstance(v, (list, tuple)):
                expanded_data[k] = [expand_data(vi, template) for vi in v]
            else:
                expanded_data[k] = expand_data(v, template)

    elif isinstance(data, string.Template):

        expanded_data = data.safe_substitute(**expanded_template)

        try:
            expanded_data = int(expanded_data)
        except ValueError as noint:
            logger.debug("Template'd Item Not an Integer")

        logger.info("Expanding {} to {}".format(data, expanded_data))
        logger.info("From Template: {}".format(expanded_template))
    else:
        expanded_data = data

    return expanded_data

def write_chain(chain=[], **kwargs):
    '''
    Write this chain of objects
    :param chain:
    :return:
    '''

    logger = logging.getLogger("dojo.write_chain")

    host = kwargs.get("host", None)
    token = kwargs.get("token", None)
    username = kwargs.get("username", None)
    password = kwargs.get("password", None)

    if host is None:
        logger.error("Write chain needs a defectDojo host specified in Host to work")
        raise ValueError("No Host")
    if token is None and (username is None or password is None):
        logger.error("Application needs either a username/password combination or an api token specified")
        raise ValueError("No Authentication")

    all_args = {"host": host,
                "token": token,
                "username": username,
                "password": password}

    template_obj = None
    if chain is not None:
        template_obj = {}
        for x in range(0, len(chain)):

            logger.debug("Processing : {}".format(chain[x]))
            # Search for Chain Item
            tdata = expand_data(chain[x]["data"], template_obj)
            sdata = expand_data(chain[x]["search_data"], template_obj)

            logger.info("TData: {}".format(tdata))

            dojo_obj = chain[x]["type"](
                action="search",
                data=sdata,
                **all_args)

            if dojo_obj.id is None:
                # None found create new Object
                dojo_obj.data = tdata
                dojo_obj.new_obj()
            else:
                # One Found Update Existing Object
                logger.info("update obj: {}".format(json.dumps(tdata)))
                dojo_obj.update_obj(tdata)

            for func, arguments in chain[x].get("extra_func", dict()).items():
                try:
                    getattr(dojo_obj, func)(*arguments.get("args", list()),
                                            **arguments.get("kwargs", dict())
                                            )
                except Exception as extra_arg_fail:
                    logger.warning("Unable to Run extra Arg : {} against {} ignoring".format(func, dojo_obj))
                else:
                    logger.debug("Ran Extra Arg : {} against {}".format(func, dojo_obj))


            template_obj[x] = dojo_obj
            if chain[x].get("named", None) is not None:
                template_obj["N{}".format(chain[x]["named"])] = dojo_obj
    else:
        logger.warning("No Chain of Items Given")

    return template_obj
