# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,E0402


"methods"


import datetime
import os
import uuid


from .objects import items, keys


def edit(obj, setter, skip=False):
    for key, val in items(setter):
        if skip and val == "":
            continue
        try:
            obj[key] = int(val)
            continue
        except ValueError:
            pass
        try:
            obj[key] = float(val)
            continue
        except ValueError:
            pass
        if val in ["True", "true"]:
            obj[key] = True
        elif val in ["False", "false"]:
            obj[key] = False
        else:
            obj[key] = val


def fmt(obj, args=None, skip=None) -> str:
    if args is None:
        args = keys(obj)
    if skip is None:
        skip = []
    txt = ""
    for key in sorted(args):
        if key in skip:
            continue
        try:
            value = obj[key]
        except KeyError:
            continue
        if isinstance(value, str) and len(value.split()) >= 2:
            txt += f'{key}="{value}" '
        else:
            txt += f'{key}={value} '
    return txt.strip()


def fqn(obj) -> str:
    kin = str(type(obj)).split()[-1][1:-2]
    if kin == "type":
        kin = obj.__name__
    return kin


def ident(obj) -> str:
    return os.path.join(
                        fqn(obj),
                        str(uuid.uuid4().hex),
                        os.path.join(*str(datetime.datetime.now()).split())
                       )


def parse(obj, txt=None) -> None:
    args = []
    obj.args = obj.args or []
    obj.cmd = obj.cmd or ""
    obj.gets = obj.gets or {}
    obj.hasmods = obj.hasmod or False
    obj.mod = obj.mod or ""
    obj.opts = obj.opts or ""
    obj.result = obj.reult or []
    obj.sets = obj.sets or {}
    obj.otxt = txt or obj.txt or ""
    _nr = -1
    for spli in obj.otxt.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            if key == "mod":
                obj.hasmods = True
                if obj.mod:
                    obj.mod += f",{value}"
                else:
                    obj.mod = value
                continue
            obj.sets[key] = value
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            obj.gets[key] = value
            continue
        _nr += 1
        if _nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.txt = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.txt = obj.cmd + " " + obj.rest
    else:
        obj.txt = obj.cmd or ""


def search(obj, selector) -> bool:
    res = False
    for key, value in items(selector):
        if key not in obj:
            res = False
            break
        val = obj[key]
        if str(value) in str(val):
            res = True
            break
    return res
