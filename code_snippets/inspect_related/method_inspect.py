# -*- coding: utf-8 -*-

import inspect


def extract_qualname(meth):
    """
    :param meth: a function, could be pure function, or bounded method
    :return: return the __qualname__ of meth
    """
    if inspect.ismethod(meth):
        meth = meth.__func__
    if inspect.isfunction(meth):
        return meth.__qualname__

    return ''
