"""
The State Library: SaltStack state documentor module.
"""
import logging
import os
import re

import salt.fileclient
import salt.utils.state

__virtualname__ = "tsl"

"""
_infotype_ contains the possible doc values, with a boolean 'required' flag
"""
_infotype_ = {
    "Author": True,
    "Description": True,
    "Syntax": True,
    "Pillars": False,
    "Grains": False,
}

__func_alias__ = {"list_": "list"}

log = logging.getLogger(__name__)


def __virtual__():
    return __virtualname__


def hello():
    """
    Check that the TSL is working.

    CLI Example:

    .. code-block:: bash

    salt '*' tsl.hello
    """
    return "Hi"


def _filedoc(filename, state, saltenv=None):
    """
    Parse the document section of a state file.
    """

    if __salt__["file.file_exists"](filename):
        content = __salt__["file.read"](filename)
        docs_section = re.findall("#START-DOC(.*?)#END-DOC", content, re.S)
        if docs_section:
            docs = docs_section[0].splitlines()
            tsl, exists, error = {}, [], []
            tsl["State_name"] = state
            tsl["File_name"] = filename
            # Pillars
            plist = pillars(state, saltenv=saltenv)
            if len(plist) > 0:
                tsl["Pillars"] = plist
            # Grains
            glist = grains(state, saltenv=saltenv)
            if len(glist) > 0:
                tsl["Grains"] = glist
            # Includes
            ilist = includes(state, saltenv=saltenv)
            if len(ilist) > 0:
                tsl["Includes"] = ilist
            # Processing DOC string
            for line in docs:
                docval = re.match(r"#\s*([0-9a-zA-Z_]+):\s*(.*)", line)
                if docval:
                    name = docval.expand(r"\1")
                    value = docval.expand(r"\2")
                    # Check if this info is known to us
                    if name in _infotype_:
                        # Check duplicate info
                        if name in exists:
                            error.append(
                                "Duplicated info: " + name + docval.expand(r" (\2)"),
                            )
                            continue
                        if name == "Pillars":
                            plist = sorted(list({v.strip() for v in value.split(",")}))
                            if name in tsl:
                                tsl[name] = sorted(list(set(tsl[name] + plist)))
                            else:
                                tsl[name] = plist
                        elif name == "Grains":
                            glist = sorted(list({v.strip() for v in value.split(",")}))
                            if name in tsl:
                                tsl[name] = sorted(list(set(tsl[name] + glist)))
                            else:
                                tsl[name] = glist
                        else:
                            tsl[name] = value
                        exists.append(name)
                    else:
                        error.append(docval.expand(r"Unknown info: \1 "))
            # Look for missing info
            for typ, req in _infotype_.items():
                if req and typ not in exists:
                    error += ("Missing info: " + typ,)
            retval = {}
            retval["Doc Info"] = os.linesep.join(
                [
                    f"{k}: {v}"
                    if not isinstance(v, list)
                    else os.linesep.join(["%s:" % k] + ["\t%s" % v_ for v_ in v])
                    for k, v in tsl.items()
                ]
            )
            if error:
                retval["Errors"] = error
            return retval
        else:
            return {"Error": "Missing DOC section"}
    else:
        return {"Error": "Missing .sls file"}


def _path(state, saltenv=None):
    """
    Return the cached .sls file path of the state.
    """
    saltenv = saltenv or __opts__.get("saltenv") or "base"
    opts = salt.utils.state.get_sls_opts(__opts__, saltenv=saltenv)

    with salt.fileclient.get_file_client(opts) as client:
        info = client.get_state(state, saltenv)
    # st_ = salt.state.HighState(opts)
    # info = st_.client.get_state(state, saltenv)

    if "dest" in info:
        path = info["dest"]
        return path
    else:
        return False


def doc(state, saltenv=None):
    """
    Show the document section of a state.

    CLI Example:

    .. code-block:: bash

    salt '*' tsl.doc state
    """
    path = _path(state, saltenv=saltenv)
    if path:
        return _filedoc(path, state, saltenv=saltenv)
    else:
        return "State does not exist on this minion."


def list_(saltenv=None):
    """
    Show the document section state files recursively for a minion.

    saltenv
        Salt fileserver environment

    CLI Example:

    .. code-block:: bash

    salt 'minion' tsl.list
    salt 'minion' tsl.list saltenv=dev
    """

    saltenv = saltenv or __opts__.get("saltenv")
    opts = salt.utils.state.get_sls_opts(__opts__, saltenv=saltenv)
    st_ = salt.state.HighState(opts)
    states = st_.compile_state_usage()

    tsl = {"Unused states": {}, "Used in Highstate": {}}
    for env, data in states.items():
        used = data["used"]
        unused = data["unused"]
        try:
            used.remove("top")
        except ValueError:
            pass
        try:
            unused.remove("top")
        except ValueError:
            pass
        if unused:
            tsl["Unused states"][env] = unused
        if used:
            tsl["Used in Highstate"][env] = used

    return tsl


def list_simple(saltenv=None):
    """
    Show used and unused state files for a minion.

    saltenv
        Salt fileserver environment

    CLI Example:

    .. code-block:: bash

    salt 'minion' tsl.list
    salt 'minion' tsl.list saltenv=dev
    """

    saltenv = saltenv or __opts__.get("saltenv")
    opts = salt.utils.state.get_sls_opts(__opts__, saltenv=saltenv)
    st_ = salt.state.HighState(opts)
    states = st_.compile_state_usage()

    tsl = {}
    for env, data in states.items():
        stl = data["used"] + data["unused"]
        try:
            stl.remove("top")
        except ValueError:
            pass
        tsl[env] = stl

    return tsl


def list_full(saltenv=None):
    """
    Show the document section of states for a minion.

    saltenv
        Salt fileserver environment

    CLI Example:

    .. code-block:: bash

    salt 'minion' tsl.list_full
    salt 'minion' tsl.list_full saltenv=dev
    """

    saltenv = saltenv or __opts__.get("saltenv")
    opts = salt.utils.state.get_sls_opts(__opts__, saltenv=saltenv)
    st_ = salt.state.HighState(opts)
    states = st_.compile_state_usage()

    tsl = {"Doc section": {}, "Unused states": {}, "Used in Highstate": {}}
    for env, data in states.items():
        for state in data["used"]:
            if state == "top":
                continue
            path = _path(state, saltenv=env)
            if env not in tsl["Doc section"]:
                tsl["Doc section"][env] = {}
            if env not in tsl["Used in Highstate"]:
                tsl["Used in Highstate"][env] = {}
            tsl["Doc section"][env][state] = _filedoc(path, state, saltenv=env)
            tsl["Used in Highstate"][env][state] = {"name": state, "path": path}

        for state in data["unused"]:
            if state == "top":
                continue
            path = _path(state, saltenv=env)
            if env not in tsl["Unused states"]:
                tsl["Unused states"][env] = {}
            tsl["Unused states"][env][state] = {"name": state, "path": path}

    return tsl


def search(term, saltenv=None):
    """
    Search for term in the document section of states for a minion.

    term
        Search term

    CLI Example:

    .. code-block:: bash

    salt 'minion' tsl.search term
    salt 'minion' tsl.search term saltenv=dev
    """

    # Get the states of minion
    saltenv = saltenv or __opts__.get("saltenv")
    opts = salt.utils.state.get_sls_opts(__opts__, saltenv=saltenv)
    st_ = salt.state.HighState(opts)
    states = st_.compile_state_usage()

    # return ','.join(states)
    tsl = {}
    # Lookup all statefiles
    for env, data in states.items():
        for state in list(set(data["used"] + data["unused"])):
            if state == "top":
                continue
            if state.find(term) != -1:
                if env not in tsl:
                    tsl[env] = {}
                tsl[env][state] = ["Module: " + state]
            path = _path(state, saltenv=env)
            # Parse the states' doc section and search for term
            doc_ = _filedoc(path, state, saltenv=env)
            for section in doc_:
                if "Doc Info" in section:
                    for info in doc_["Doc Info"]:
                        if info.find(term) != -1:
                            if env not in tsl:
                                tsl[env] = {}
                            if state not in tsl[env]:
                                tsl[env][state] = []
                            tsl[env][state].append(info)

    return tsl


def pillars(state, saltenv=None):
    """
    List of used pillars in a state for a minion.

    state
        State name

    saltenv
        Salt fileserver environment from which to retrieve the file

    CLI Example:

    .. code-block:: bash

    salt 'minion' tsl.pillars state
    salt 'minion' tsl.pillars state saltenv=dev
    """
    saltenv = saltenv or "base"
    filename = _path(state, saltenv=saltenv)
    if filename:
        content = __salt__["file.read"](filename)
        finds = re.finditer(
            r"(pillar\[['\"]|salt\[['\"]pillar\.get['\"]\]\(['\"])(?P<pi>.+?)(['\"]\]|['\"]\))",
            content,
        )
        plist = sorted(list({f.group("pi") for f in finds}))
        return plist
    else:
        return "State does not exist on this minion."


def grains(state, saltenv=None):
    """
    List of used grains in a state for a minion.

    state
        State name

    saltenv
        Salt fileserver environment from which to retrieve the file

    CLI Example:

    .. code-block:: bash

    salt 'minion' tsl.grains state
    salt 'minion' tsl.grains state saltenv=dev
    """

    saltenv = saltenv or "base"
    filename = _path(state, saltenv=saltenv)
    if filename:
        content = __salt__["file.read"](filename)
        finds = re.finditer(
            r"(grains\[['\"]|salt\[['\"]grains\.get['\"]\]\(['\"])(?P<gr>.+?)(['\"]\]|['\"]\))",
            content,
        )
        glist = sorted(list({f.group("gr") for f in finds}))
        return glist
    else:
        return "State does not exist on this minion."


def includes(state, saltenv=None):
    """
    List of included state files for a minion.

    state
        State name

    saltenv
        Salt fileserver environment from which to retrieve the file

    CLI Example:

    .. code-block:: bash

    salt 'minion' tsl.includes state
    salt 'minion' tsl.includes state saltenv=dev
    """

    saltenv = saltenv or "base"
    filename = _path(state, saltenv=saltenv)
    if filename:
        content = __salt__["file.read"](filename)
        lines = content.splitlines()
        ilist = []
        included = False
        # Processing file string
        for line in lines:
            # Process file after include found
            if included:
                expr = re.match(r"^\s*-(.*)", line)
                if expr:
                    state = expr.expand(r"\1").strip()
                    ilist.append(state)
                else:
                    # End of includes
                    break
            else:
                # Process file to find include
                expr = re.match("include:", line)
                if expr:
                    included = True

        # Make list unique
        ilist = list(set(ilist))
        return ilist
    else:
        return "State does not exist on this minion."
