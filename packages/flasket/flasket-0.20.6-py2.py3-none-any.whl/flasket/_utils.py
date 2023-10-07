import typing as t
from copy import deepcopy

from boltons.iterutils import remap


def strip_none(_p: str, k: str, v: t.Any) -> bool:
    return k is not None and v is not None


def _deepmerge(src: t.Dict[str, t.Any], dst: t.Dict[str, t.Any], path: t.List[str] = None) -> t.Dict[str, t.Any]:
    """
    Take every key, value from src and merge it recursively into dst.
    Adapted from https://stackoverflow.com/questions/7204805

    Parameters
    ----------
    dst: dict
        Destination dictionary

    src: dict
        Source dictionary

    path:
        Used internally

    Returns
    -------
    dict:
        Merged dictionary
    """
    if path is None:
        path = []

    for key in src:
        if key not in dst:
            dst[key] = src[key]
        elif isinstance(dst[key], dict) and isinstance(src[key], dict):
            _deepmerge(src[key], dst[key], path + [str(key)])
        elif dst[key] == src[key]:
            pass  # same leaf value
        else:
            dst[key] = src[key]
    return dst


def deepmerge(dst: t.Dict[str, t.Any], src: t.Dict[str, t.Any]) -> t.Dict[str, t.Any]:
    """
    Take every key, value from src and merge it recursivly into dst.
    None values are stripped from src before merging.

    Adapted from https://stackoverflow.com/questions/7204805

    Parameters
    ----------
    dst: dict
        destination dictionary

    src: dict
        source dictionary

    Returns
    -------
    dict:
        merged dictionary
    """
    # pylint: disable=unnecessary-lambda-assignment
    src = remap(src, visit=strip_none)

    return _deepmerge(src, deepcopy(dst))
