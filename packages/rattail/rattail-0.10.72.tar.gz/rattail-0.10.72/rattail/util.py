# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Utilities
"""

import collections
import importlib
import re
import shlex
import unicodedata
import datetime
import decimal
import subprocess
import logging
import warnings

from pkg_resources import iter_entry_points


log = logging.getLogger(__name__)

# generic singleton to indicate an arg which isn't set etc.
NOTSET = object()


class OrderedDict(collections.OrderedDict):
    def __init__(self, *args, **kwargs):
        warnings.warn("rattail.util.OrderedDict is deprecated; "
                      "please use collections.OrderedDict instead",
                      DeprecationWarning, stacklevel=2)
        super(OrderedDict, self).__init__(*args, **kwargs)


def capture_output(*args, **kwargs):
    """
    Runs ``command`` and returns any output it produces.
    """
    # We *need* to pipe ``stdout`` because that's how we capture the output of
    # the ``hg`` command.  However, we must pipe *all* handles in order to
    # prevent issues when running as a GUI but *from* the Windows console.  See
    # also: http://bugs.python.org/issue3905
    kwargs.update({
        'stdin': subprocess.PIPE,
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
    })
    output = subprocess.Popen(*args, **kwargs).communicate()[0]
    return output


def data_diffs(local_data, host_data, fields=None,
               fuzzy_fields=None, fuzz_factor=None):
    """
    Find all (relevant) fields which differ between the host and local data
    values for a given record.
    """
    if fields is None:
        fields = list(local_data)

    diffs = []
    fuzzy_time_cutoff = datetime.timedelta(seconds=fuzz_factor or 1)
    for field in fields:

        # maybe raise explicit error to indicate *which* dict is missing data
        # (otherwise the comparison below raises "ambiguous" error about it)
        if field not in local_data:
            raise KeyError("key '{}' is missing from local_data".format(field))
        if field not in host_data:
            raise KeyError("key '{}' is missing from host_data".format(field))

        local_value = local_data[field]
        host_value = host_data[field]

        if fuzzy_fields and field in fuzzy_fields:

            if local_value and not host_value:
                diffs.append(field)
                continue

            if host_value and not local_value:
                diffs.append(field)
                continue

            if isinstance(local_value, datetime.datetime):

                if (host_value > local_value
                    and host_value - local_value >= fuzzy_time_cutoff):
                    diffs.append(field)

                elif (local_value > host_value
                      and local_value - host_value >= fuzzy_time_cutoff):
                    diffs.append(field)

                continue

            elif isinstance(local_value, (int, float, decimal.Decimal)):

                if (host_value > local_value
                    and host_value - local_value >= fuzz_factor):
                    diffs.append(field)

                elif (local_value > host_value
                      and local_value - host_value >= fuzz_factor):
                    diffs.append(field)

                continue

        if local_value != host_value:
            diffs.append(field)

    return diffs


def get_class_hierarchy(klass, topfirst=True):
    """
    Returns a list of all classes in the inheritance chain for the
    given class.

    For instance::

       class A(object):
          pass

       class B(A):
          pass

       class C(B):
          pass

       get_class_hierarchy(C)
       # -> [A, B, C]

    Specify ``topfirst=False`` to get ``[C, B, A]`` instead.
    """
    hierarchy = []

    def traverse(cls):
        if cls is not object:
            hierarchy.append(cls)
            for parent in cls.__bases__:
                traverse(parent)

    traverse(klass)
    if topfirst:
        hierarchy.reverse()
    return hierarchy


def get_package_name(name):
    """
    Generic logic to derive a "package name" from the given name.

    E.g. if ``name`` is "Poser Plus" this will return "poser_plus"
    """
    # cf. https://stackoverflow.com/a/3194567
    name = unicodedata.normalize('NFD', name)
    name = name.encode('ascii', 'ignore').decode('ascii')
    words = re.split(r'[\- ]', name)
    return '_'.join([word.lower() for word in words])


def get_studly_prefix(name):
    """
    Generic logic to derive a "studly prefix" from the given name.

    E.g. if ``name`` is "Poser Plus" this will return "PoserPlus"
    """
    # cf. https://stackoverflow.com/a/3194567
    name = unicodedata.normalize('NFD', name)
    name = name.encode('ascii', 'ignore').decode('ascii')
    words = re.split(r'[\- ]', name)
    return ''.join([word.capitalize() for word in words])


def import_module_path(module_path):
    """
    Import an arbitrary Python module.

    .. warning::

       This function is deprecated; please use
       :func:`python:importlib.import_module()` instead.

    :param module_path: String referencing a module by its "dotted path".

    :returns: The referenced module.
    """
    warnings.warn("rattail.util.import_module_path() is deprecated; "
                  "please use importlib.import_module() instead",
                  DeprecationWarning, stacklevel=2)

    return importlib.import_module(module_path)


def import_reload(module):
    """
    Reload a module.

    .. warning::

       This function is deprecated; please use
       :func:`python:importlib.reload()` instead.

    :param module: An already-loaded module.

    :returns: The module.
    """
    warnings.warn("rattail.util.import_reload() is deprecated; "
                  "please use importlib.reload() instead",
                  DeprecationWarning, stacklevel=2)

    return importlib.reload(module)


def get_object_spec(obj):
    """
    Returns the "object spec" string for the given object.
    """
    # TODO: this only handles a class *instance* currently
    return '{}:{}'.format(obj.__module__, obj.__class__.__name__)


def load_object(specifier):
    """
    Load an arbitrary object from a module, according to a specifier.

    The specifier string should contain a dotted path to an importable module,
    followed by a colon (``':'``), followed by the name of the object to be
    loaded.  For example:

    .. code-block:: none

       rattail.files:overwriting_move

    You'll notice from this example that "object" in this context refers to any
    valid Python object, i.e. not necessarily a class instance.  The name may
    refer to a class, function, variable etc.  Once the module is imported, the
    ``getattr()`` function is used to obtain a reference to the named object;
    therefore anything supported by that method should work.

    :param specifier: Specifier string.

    :returns: The specified object.
    """
    if not specifier:
        raise ValueError("no object spec provided")
    module_path, name = specifier.split(':')
    module = importlib.import_module(module_path)
    return getattr(module, name)


def load_entry_points(group, ignore_errors=False):
    """
    Load a set of ``setuptools``-style entry points.

    This is a convenience wrapper around ``pkg_resources.iter_entry_points()``.

    :param group: The group of entry points to be loaded.

    :returns: A dictionary whose keys are the entry point names, and values are
       the loaded entry points.
    """
    entry_points = {}
    for entry_point in iter_entry_points(group):
        try:
            ep = entry_point.load()
        except:
            if not ignore_errors:
                raise
            log.warning("failed to load entry point: %s", entry_point,
                        exc_info=True)
        else:
            entry_points[entry_point.name] = ep
    return entry_points


def prettify(text):
    """
    Return a "prettified" version of text.
    """
    text = text.replace('_', ' ')
    text = text.replace('-', ' ')
    words = text.split()
    return ' '.join([x.capitalize() for x in words])


def pretty_boolean(value):
    """
    Returns ``'Yes'`` or ``'No'`` or empty string if value is ``None``
    """
    if value is None:
        return ""
    return "Yes" if value else "No"


def hours_as_decimal(hours, places=2):
    """
    Convert the given ``datetime.timedelta`` object into a Decimal whose
    value is in terms of hours.
    """
    if hours is None:
        return
    minutes = (hours.days * 1440) + (hours.seconds // 60)
    fmt = '{{:0.{}f}}'.format(places)
    return decimal.Decimal(fmt.format(minutes / 60.0))


def pretty_hours(hours=None, seconds=None):
    """ DEPRECATED """
    warnings.warn("pretty_hours() function is deprecated; please "
                  "use AppHandler.render_duration() insted",
                  DeprecationWarning, stacklevel=2)

    if hours is None and seconds is None:
        return ''
    if hours is None:
        hours = datetime.timedelta(seconds=seconds)

    # determine if hours value is positive or negative.  seems like some of the
    # math can be "off" if negative values are involved, in which case we'll
    # convert to positive for sake of math and then prefix result with a hyphen
    negative = False

    if isinstance(hours, decimal.Decimal):
        if hours < 0:
            negative = True
            hours = -hours
        hours = datetime.timedelta(seconds=int(hours * 3600))

    minutes = (hours.days * 1440) + (hours.seconds / 60)
    rendered = "{}:{:02d}".format(int(minutes // 60), int(minutes % 60))
    if negative:
        rendered = "-{}".format(rendered)
    return rendered


def pretty_quantity(value, empty_zero=False):
    """
    Return a "pretty" version of the given value, as string.  This is meant primarily
    for use with things like order quantities, so that e.g. 1.0000 => 1
    """
    if value is None:
        return ''
    if int(value) == value:
        value = int(value)
        if empty_zero and value == 0:
            return ''
        return str(value)
    return str(value).rstrip('0')


def progress_loop(func, items, factory, *args, **kwargs):
    """
    This will iterate over ``items`` and call ``func`` for each.  If a progress
    ``factory`` kwarg is provided, then a progress instance will be created and
    updated along the way.
    """
    message = kwargs.pop('message', None)
    count = kwargs.pop('count', None)
    allow_cancel = kwargs.pop('allow_cancel', False)
    if count is None:
        try:
            count = len(items)
        except TypeError:
            count = items.count()
    if not count:
        return True

    prog = None
    if factory:
        prog = factory(message, count)

    canceled = False
    for i, item in enumerate(items, 1):
        func(item, i, *args, **kwargs)
        if prog and not prog.update(i):
            canceled = True
            break
    if prog:
        prog.finish()
    if canceled and not allow_cancel:
        raise RuntimeError("Operation was canceled")
    return not canceled


def simple_error(error):
    """
    Return a "simple" string for the given error.  Result will look like::

       "ErrorClass: Description for the error"

    However the logic checks to ensure the error has a descriptive message
    first; if it doesn't the result will just be::

       "ErrorClass"
    """
    cls = str(type(error).__name__)
    msg = str(error)
    if msg:
        return "{}: {}".format(cls, msg)
    return cls


def shlex_join(split_command):
    """
    Wrapper which invokes ``shlex.join()`` if available; otherwise
    a workaround is implemented.

    cf. https://stackoverflow.com/a/50022816
    """
    # python 3.8+ has native shlex.join()
    if hasattr(shlex, 'join'):
        return shlex.join(split_command)

    # python 3.3+ has native shlex.quote()
    if hasattr(shlex, 'quote'):
        return ' '.join(shlex.quote(x) for x in split_command)

    # python 2 has neither...so the rest of this logic is copy/pasted
    # from later python
    # _find_unsafe = re.compile(r'[^\w@%+=:,./-]', re.ASCII).search
    _find_unsafe = re.compile(r'[^\w@%+=:,./-]').search

    def quote(s):
        """Return a shell-escaped version of the string *s*."""
        if not s:
            return "''"
        if _find_unsafe(s) is None:
            return s

        # use single quotes, and put single quotes into double quotes
        # the string $'b is then quoted as '$'"'"'b'
        return "'" + s.replace("'", "'\"'\"'") + "'"

    return ' '.join(quote(x) for x in split_command)
