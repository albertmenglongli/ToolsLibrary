# -*- coding: utf-8 -*-

import inspect


def is_attribute(klass, attr, value=None):
    """Test if a value of a class is attribute. (Not a @property style
    attribute)
    :param klass: the class
    :param attr: attribute name
    :param value: attribute value
    """
    if value is None:
        value = getattr(klass, attr)
    assert getattr(klass, attr) == value

    if not inspect.isroutine(value):
        if not isinstance(value, property):
            return True
    return False


def is_property_method(klass, attr, value=None):
    """Test if a value of a class is @property style attribute.
    :param klass: the class
    :param attr: attribute name
    :param value: attribute value
    """
    if value is None:
        value = getattr(klass, attr)
    assert getattr(klass, attr) == value

    if not inspect.isroutine(value):
        if isinstance(value, property):
            return True
    return False


def is_regular_method(klass, attr, value=None):
    """Test if a value of a class is regular method.
    example::
        class MyClass(object):
            def to_dict(self):
                ...
    :param klass: the class
    :param attr: attribute name
    :param value: attribute value
    """
    if value is None:
        value = getattr(klass, attr)
    assert getattr(klass, attr) == value

    if inspect.isroutine(value):
        if not is_static_method(klass, attr, value) and not is_class_method(klass, attr, value):
            return True

    return False


def is_static_method(klass, attr, value=None):
    """Test if a value of a class is static method.
    example::
        class MyClass(object):
            @staticmethod
            def method():
                ...
    :param klass: the class
    :param attr: attribute name
    :param value: attribute value
    """
    if value is None:
        value = getattr(klass, attr)
    assert getattr(klass, attr) == value

    for cls in inspect.getmro(klass):
        if inspect.isroutine(value):
            if attr in cls.__dict__:
                binded_value = cls.__dict__[attr]
                if isinstance(binded_value, staticmethod):
                    return True
    return False


def is_class_method(klass, attr, value=None):
    """Test if a value of a class is class method.
    example::
        class MyClass(object):
            @classmethod
            def method(cls):
                ...
    :param klass: the class
    :param attr: attribute name
    :param value: attribute value
    """
    if value is None:
        value = getattr(klass, attr)
    assert getattr(klass, attr) == value

    for cls in inspect.getmro(klass):
        if inspect.isroutine(value):
            if attr in cls.__dict__:
                binded_value = cls.__dict__[attr]
                if isinstance(binded_value, classmethod):
                    return True
    return False
