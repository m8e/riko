# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab
"""
    pipe2py.modules.pipestrconcat
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    http://pipes.yahoo.com/pipes/docs?doc=string#StringBuilder
"""

# aka stringbuilder

from pipe2py.lib import utils
from pipe2py.lib.dotdict import DotDict


def _gen_string(parts, item, context=None, **kwargs):
    for part in parts:
        try:
            yield utils.get_value(DotDict(part), item, **kwargs)
        except AttributeError:
            # ignore if the item is referenced but doesn't have our source
            # field
            # todo: issue a warning if debugging?
            continue
        except TypeError:
            if context and context.verbose:
                print "pipe_strconcat: TypeError"


def pipe_strconcat(context=None, _INPUT=None, conf=None, **kwargs):
    """A string module that builds a string. Loopable.

    Parameters
    ----------
    context : pipe2py.Context object
    _INPUT : pipeforever pipe or an iterable of items
    conf : {
        'part': [
            {'value': '<img src="'}, {'subkey': 'img.src'}, {'value': '">'}
        ]
    }

    Yields
    ------
    _OUTPUT : joined strings
    """
    conf = DotDict(conf)
    parts = utils.listize(conf['part'])

    for item in _INPUT:
        yield ''.join(_gen_string(parts, DotDict(item), context, **kwargs))
