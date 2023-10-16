"""A module for j_objects (JSON deserializable objects). This module is used to identify the object type.

Usage:
    json.load(file, object_hook=loadJObject)

Classes:
    j_object (j_object): A base class for all jObjects (JSON deserializable objects). This class is used to identify the
    object type.

Methods:
    load_j_object (function): Return a j_object from a dictionary. Use this method as the object_hook for json.load.
    list_all_j_objects (function): Return a dict of the names of all j_object objects and their classes.

Attributes:
    j_object_type (str): The name of the object type.

"""

import json


class j_object:
    """A base class for all j_objects (JSON deserializable objects). This class is used to identify the object type."""

    def __init__(self) -> None:
        """Initialize the object.

        Parameters:
            j_object_type (str): The name of the object type.
        """
        self.j_object_type = type(self).__name__


def load_j_object(d: dict) -> j_object:
    """Return a j_object from a dictionary. Use this method as the object_hook for json.load.

    Args:
        d (dict): The dictionary to load the j_object from.

    Returns:
        j_object: The j_object loaded from the dictionary.

    Usage:
        json.load(file, object_hook=load_j_object)
    """
    object_type = d.get("j_object_type")
    new_object = list_all_j_objects().get(object_type)
    new_object = new_object() if new_object is not None else None

    if new_object is None:
        return d

    for var in d:
        if var in vars(new_object):
            setattr(new_object, var, d[var])

    return new_object


def list_all_j_objects() -> dict:
    """Return a dict of the names of all j_object objects and their classes."""
    classes = {}

    for cls in j_object.__subclasses__():
        classes[cls.__name__] = cls
        for subclass in cls.__subclasses__():
            classes[subclass.__name__] = subclass

    return classes


class j_object_encoder(json.JSONEncoder):
    """JSON encoder for j_objects."""

    def default(self, o):
        """Return a dictionary of the j_object's variables that do not start with an underscore."""
        return {name: var for (name, var) in o.__dict__.items() if not str(name).startswith("_")}
