from typing import Tuple

from tecton.framework import base_tecton_object


def short_tecton_objects_repr(tecton_objects: Tuple[base_tecton_object.BaseTectonObject]) -> str:
    """Returns a shortened printable representation for a tuple of Tecton objects. Used for printing summaries."""
    short_strings = tuple(short_tecton_object_repr(obj) for obj in tecton_objects)
    return repr(short_strings)


def short_tecton_object_repr(tecton_object: base_tecton_object.BaseTectonObject) -> str:
    """Returns a shortened printable representation for a Tecton object. Used for printing summaries."""
    return f"{type(tecton_object).__name__}('{tecton_object.info.name}')"
