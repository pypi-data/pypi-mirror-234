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
Application Configuration
"""

import importlib
import os
import re
import sys
import shlex
import datetime
import configparser
import warnings
import logging
import logging.config

import config as configuration

from rattail.util import load_entry_points, load_object
from rattail.exceptions import WindowsExtensionsNotInstalled, ConfigurationError
from rattail.files import temp_path
from rattail.logging import TimeConverter


log = logging.getLogger(__name__)


def parse_bool(value):
    """
    Derive a boolean from the given string value.
    """
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if str(value).lower() in ('true', 'yes', 'y', 'on', '1'):
        return True
    return False


def parse_list(value):
    """
    Parse a configuration value, splitting by whitespace and/or commas and
    taking quoting into account, etc., yielding a list of strings.
    """
    if value is None:
        return []
    parser = shlex.shlex(value)
    parser.whitespace += ','
    parser.whitespace_split = True
    values = list(parser)
    for i, value in enumerate(values):
        if value.startswith('"') and value.endswith('"'):
            values[i] = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            values[i] = value[1:-1]
    return values


class RattailConfigWrapper:
    """
    Simple wrapper around *either* the legacy :class:`RattailConfig`
    or the newer :class:`RattailConfiguration` object.

    .. note::

       This class will go away once migration to the newer
       ``RattailConfiguration`` is complete.
    """

    def __init__(self, *args, **kwargs):

        # first make legacy config
        self.__dict__['config'] = RattailConfig(*args, **kwargs)

        # but use new-style instead, if config says so
        if self.config.getbool('rattail.config', 'use_configuration', usedb=False):
            self.__dict__['config'] = RattailConfiguration(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.config, name)

    def __setattr__(self, name, value):
        setattr(self.config, name, value)

    def __repr__(self):
        legacy = not isinstance(self.config, RattailConfiguration)
        return f"RattailConfigWrapper(legacy={legacy})"


class RattailConfiguration:
    """
    Configuration for Rattail apps.

    .. warning::

       I'm documenting this as though it's complete, but as of writing
       this class is **not used** unless config says to, via:

       .. code-block:: ini

          [rattail.config]
          use_configuration = true

    A single instance of this class is created on app startup, by way
    of calling :func:`make_config()`.

    Even though this config object is "global" in nature, it must
    be passed around to all areas of the app; you cannot simply
    import it.  In other words::

       # this won't work!
       from rattail.config import global_config_object

    The global config object is mainly responsible for providing
    config values to the app, via :meth:`get()` and similar methods.

    The config object has more than one place to look when finding
    values.  This can vary somewhat but usually the priority for
    lookup is like:

    * settings table in the DB
    * one or more INI files
    * "defaults" provided by app logic

    .. attribute:: configuration

       Reference to the ``ConfigurationSet`` instance which houses the
       full set of config values which are kept in memory.  This does
       *not* contain settings from DB, but *does* contain
       :attr:`defaults` as well as values read from INI files.

    .. attribute:: defaults

       Reference to the ``Configuration`` instance containing config
       *default* values.  This is exposed in case it's useful, but in
       practice you should not update it directly; instead use
       :meth:`setdefault()`.

    .. attribute:: files_read

       List of all INI config files which were read on app startup.
       These are listed in the same order as they were read.  This
       sequence also reflects priority for value lookups, i.e. the
       first file with the value wins.

    .. attribute:: usedb

       Flag indicating whether values should ever be looked up from
       the settings table in DB.  Note that you can override this when
       calling :meth:`get()`.

    .. attribute:: preferdb

       Flag indicating whether DB settings should be preferred over
       the values from INI files or app defaults.  Note that you can
       override this when calling :meth:`get()`.

    .. attribute:: versioning_has_been_enabled

       Flag indicating whether SQLAlchemy-Continuum versioning has
       been enabled for the running app.  This gets set when
       :func:`~rattail.db.config.configure_versioning()` happens.
    """

    def __init__(
            self,
            files=[],
            usedb=None,
            preferdb=None,
    ):

        self.files_read = []
        configs = []

        # read all files requested
        for path in files:
            self._load_ini_configs(path, configs, require=True)

        # add 'defaults' config, for use w/ setdefault()
        self.defaults = configuration.Configuration({})
        configs.append(self.defaults)

        # master config set
        self.configuration = configuration.ConfigurationSet(*configs)

        # usedb flag
        self.usedb = usedb
        if self.usedb is None:
            self.usedb = self.get_bool('rattail.config.usedb',
                                       usedb=False, default=False)

        # preferdb flag
        self.preferdb = preferdb
        if self.usedb and self.preferdb is None:
            self.preferdb = self.get_bool('rattail.config.preferdb',
                                          usedb=False, default=False)

        # attempt to detect lack of sqlalchemy libraries etc.  this
        # allows us to avoid installing those on a machine which will
        # not need to access a database etc.
        if self.usedb:
            try:
                from rattail.db import Session
            except ImportError: # pragma: no cover
                log.warning("config created with `usedb = True`, but can't import "
                            "`rattail.db.Session`, so setting `usedb = False` instead",
                            exc_info=True)
                self.usedeb = False
                self.preferdb = False

        # this is always false, unless/until it becomes true
        self.versioning_has_been_enabled = False

    def _load_ini_configs(self, path, configs, require=True):
        path = os.path.abspath(path)

        # try to load config from the given path
        try:
            config = configuration.config_from_ini(path, read_from_file=True)
        except FileNotFoundError:
            if not require:
                log.warning("INI config file not found: %s", path)
                return
            raise

        # ok add that one to the mix
        configs.append(config)
        self.files_read.append(path)

        # need parent folder of that path, for %(here)s interpolation
        here = os.path.dirname(path)

        # bring in any "required" files
        requires = config.get('rattail.config.require')
        if requires:
            for path in parse_list(requires):
                path = path % {'here': here}
                self._load_ini_configs(path, configs, require=True)

        # bring in any "included" files
        includes = config.get('rattail.config.include')
        if includes:
            for path in parse_list(includes):
                path = path % {'here': here}
                self._load_ini_configs(path, configs, require=False)

    def get_app(self):
        """
        Returns the global :class:`~rattail.app.AppHandler` instance,
        creating it if necessary.
        """
        if not hasattr(self, 'app'):
            spec = self.get('rattail.app.handler', usedb=False,
                            default='rattail.app:AppHandler')
            factory = load_object(spec)
            self.app = factory(self)
        return self.app

    def setdefault(self, *args):
        """
        Establish a default config value.

        Positional arguments to this method may vary.  The *new*
        (optional) way is to pass just two args: ``key`` and
        ``value``.  But the traditional way was to pass *three* args:
        ``section``, ``option`` and ``value``.

        The main point of this is to provide a default value when none
        is actually configured, i.e. via INI file or DB settings.

        Note that if the app already has a default value for the given
        key, this method will *not* replace that value.  So the first
        call with given key will set default value, then subsequent
        calls for that key have no effect.

        :returns: The current config value, *outside of the DB*.  For
           various reasons this method may not be able to lookup
           settings from the DB, e.g. during app init.  So it can only
           determine the value per INI files + config defaults.
        """
        # figure out what sort of args were passed
        if len(args) == 2:
            key, value = args
        elif len(args) == 3:
            section, option, value = args
            key = f'{section}.{option}'
        else:
            raise ValueError("must pass either 2 args (key, value), "
                             "or 3 args (section, option, value)")

        # set default value, if not already set
        self.defaults.setdefault(key, value)

        # get current value, sans db
        return self.get(key, usedb=False)

    def get(self, *args, **kwargs):
        """
        Retrieve a value from config.

        Positional arguments to this method may vary.  The *new*
        (optional) way is to pass just one ``key`` arg.  But the
        traditional way was to pass *two* args, ``section`` and
        ``option``.

        Any keyword arguments passed, if applicable, will have
        identical meanings as for :meth:`RattailConfig.get()`.

        :returns: Value as string (always!).
        """
        # figure out what sort of args were passed
        if len(args) == 1:
            key = args[0]
        elif len(args) == 2:
            section, option = args
            key = f'{section}.{option}'
        else:
            raise ValueError("must pass either 1 arg (key), "
                             "or 2 args (section, option)")

        if kwargs.get('require') and 'default' in kwargs:
            raise ValueError("must not specify default value when require=True")

        # caller may specify (part of) error message, if applicable.
        # but we remove it from kwargs for sake of other calls below
        msg = kwargs.pop('msg', None)

        # should we use db?
        usedb = kwargs.get('usedb')
        usedb = usedb if usedb is not None else self.usedb

        # should we prefer db?
        preferdb = False
        if usedb:
            preferdb = kwargs.get('preferdb')
            if preferdb is None:
                preferdb = self.preferdb

        # read from db first if so requested
        if usedb and preferdb:
            value = self.get_from_db(key, session=kwargs.get('session'))
            if value is not None:
                return value

        # read from defaults + INI files
        value = self.configuration.get(key)
        if value is not None:
            # TODO: in most cases the distinction of "key"
            # vs. "section, option" is transparent, but in some cases
            # not so.  e.g. this came up when fetching the value for
            # key of 'tailbone.menus' which was now ambiguous..
            #
            # e.g. older code uses config like:
            #
            # [tailbone]
            # menus = poser.web.menus
            #
            # but newer code looks elsewhere:
            #
            # [tailbone.menus]
            # handler = poser.web.menus:PoserMenuHandler
            #
            # with the above, config.get('tailbone.menus') will never
            # return 'poser.web.menus' and instead will always return
            # a "sub" config object with 'handler' key!
            #
            # this also came up for datasync watcher/consumer config,
            # where some keys became ambiguous in similar way.
            #
            # so now any such keys which would be ambiguous, must
            # simply be abandoned by all app logic, and unambiguous
            # keys must be used instead.  this requires updating logic
            # as well as config files and/or DB settings, and with a
            # lengthy grace period with fallback to old setting name.
            # note however the fallback will *not* work with this new
            # RattailConfiguration class, only the older RattailConfig!
            if not isinstance(value, configuration.Configuration):
                return value

        # read from db last if so requested
        if usedb and not preferdb:
            value = self.get_from_db(key, session=kwargs.get('session'))
            if value is not None:
                return value

        # raise error if required value not found
        if kwargs.get('require'):
            msg = (f"{msg or 'missing or invalid config'}; "
                   f"please set config value for: {key}")
            raise ConfigurationError(msg)

        # give the default value if specified
        if 'default' in kwargs:
            return kwargs['default']

    def require(self, *args, **kwargs):
        """
        Retrieve a value from config, or raise error if no value can
        be found.  This is just a shortcut, so these work the same::

           config.get('foo', require=True)

           config.require('foo')
        """
        kwargs['require'] = True
        return self.get(*args, **kwargs)

    def get_from_db(self, key, session=None):
        """
        Retrieve a config value from database settings table.
        """
        app = self.get_app()
        with app.short_session(session=session) as s:
            return app.get_setting(s, key)

    def get_bool(self, *args, **kwargs):
        """
        Retrieve a boolean value from config.
        """
        value = self.get(*args, **kwargs)
        return self.parse_bool(value)

    getbool = get_bool

    def parse_bool(self, value):
        """
        Coerce the given value to a boolean.
        """
        return parse_bool(value)

    def get_int(self, *args, **kwargs):
        """
        Retrieve an integer value from config.
        """
        value = self.get(*args, **kwargs)
        if value is None:
            return None
        if value == '' and 'default' in kwargs:
            return kwargs['default']
        if isinstance(value, int):
            return value
        return int(value)

    getint = get_int

    def get_date(self, *args, **kwargs):
        """
        Retrieve a date value from config.
        """
        value = self.get(*args, **kwargs)
        app = self.get_app()
        return app.parse_date(value)

    getdate = get_date

    def get_list(self, *args, **kwargs):
        """
        Retrieve a list of string values from a single config value.
        """
        value = self.get(*args, **kwargs)
        if value is None:
            return None
        if isinstance(value, str):
            return self.parse_list(value)
        return value            # maybe a caller-provided default?

    getlist = get_list

    def parse_list(self, value):
        """
        Coerce the given value to a list.
        """
        return parse_list(value)

    def make_list_string(self, values):
        """
        Coerce the given list of values to a string, for config
        storage.  If this string is later parsed via
        :meth:`parse_list()` then it should return the same list of
        values.
        """
        final = []
        for value in values:
            if ' ' in value:
                quote = '"' if "'" in value else "'"
                value = f"{quote}{value}{quote}"
            final.append(value)
        return ', '.join(final)

    def get_dict(self, prefix):
        """
        Retrieve a particular group of values, as a dictionary.

        Please note, this will only return values from INI files +
        defaults.  It will *not* return values from DB settings.

        The ``prefix`` is analogous to the ``section`` arg used in
        :meth:`RattailConfig.get_dict()`.  However in this case it is
        not *necessarily* a traditional "section" name from INI file.
        Rather, it refers to "any" logical group under which other
        config values may be found.
        """
        try:
            values = self.configuration[prefix]
        except KeyError:
            return {}

        return values.as_dict()

    def configure_logging(self):
        """
        This first checks current config to determine whether or not we're
        supposed to be configuring logging at all.  If not, nothing more is
        done.

        If we are to configure logging, then this will save the current config
        parser defaults to a temporary file, and use this file to configure
        Python's standard logging module.
        """
        if not self.get_bool('rattail.config.configure_logging', usedb=False):
            return

        # coerce all logged timestamps to the local timezone, if possible
        timezone = self.get('rattail', 'timezone.default', usedb=False)
        if timezone:
            logging.Formatter.converter = TimeConverter(self)

        # write current values to file suitable for logging auto-config
        path = self._write_logging_config_file()
        try:
            logging.config.fileConfig(path, disable_existing_loggers=False)
        except configparser.NoSectionError as error:
            log.warning("tried to configure logging, but got NoSectionError: %s",
                        error)
        else:
            log.debug("configured logging")
        finally:
            os.remove(path)

        # if we could not coerce timestamps, log a warning about that
        if not timezone:
            log.warning("timezone is not set, so logging timestamps may "
                        "appear \"off\" - to fix, set a config value for "
                        "[rattail] timezone.default")

    def _write_logging_config_file(self):

        # load all current values into configparser
        parser = configparser.RawConfigParser()
        for section, values in self.configuration.items():
            parser.add_section(section)
            for option, value in values.items():
                parser.set(section, option, value)

        # write INI file and return path
        path = temp_path(suffix='.conf')
        with open(path, 'wt') as f:
            parser.write(f)
        return path

    ##################################################
    # TODO: remove these?
    ##################################################

    def node_type(self, default=None):
        """
        Returns the "type" of current node.  What this means will
        generally depend on the app logic.
        """
        try:
            return self.require('rattail.node_type', usedb=False)
        except ConfigurationError:
            if default:
                return default
            raise

    def production(self):
        """
        Returns boolean indicating whether the app is running in
        production mode
        """
        return self.get_bool('rattail.production', default=False)

    def appdir(self, require=True, **kwargs):
        """
        Returns path to the 'app' dir, if known.
        """
        kwargs['require'] = require
        kwargs.setdefault('usedb', False)
        return self.get('rattail.appdir', **kwargs)

    def datadir(self, require=True):
        """
        Returns path to the 'data' dir, if known.
        """
        return self.get('rattail.datadir', require=require)

    def workdir(self, require=True):
        """
        Returns path to the 'work' dir, if known.
        """
        return self.get('rattail.workdir', require=require)

    def get_model(self):
        """
        Returns a reference to configured 'model' module; defaults to
        :mod:`rattail.db.model`.
        """
        spec = self.get('rattail.model', usedb=False,
                        default='rattail.db.model')
        return importlib.import_module(spec)

    def get_enum(self, **kwargs):
        """
        Returns a reference to configured "enum" module; defaults to
        :mod:`rattail.enum`.
        """
        kwargs.setdefault('usedb', False)
        spec = self.get('rattail', 'enum', default='rattail.enum', **kwargs)
        return importlib.import_module(spec)

    def get_trainwreck_model(self):
        """
        Returns a reference to the configured data 'model' module for
        Trainwreck.  Note that there is *not* a default value for
        this; it must be configured.
        """
        spec = self.require('rattail.trainwreck.model', usedb=False)
        return importlib.import_module(spec)

    def versioning_enabled(self):
        """
        Returns boolean indicating whether data versioning is enabled.
        """
        return self.get_bool('rattail.db.versioning.enabled', usedb=False,
                             default=False)

    def product_key(self, **kwargs):
        """
        Deprecated; instead please see
        :meth:`rattail.app.AppHandler.get_product_key_field()`.
        """
        warnings.warn("config.product_key() is deprecated; please "
                      "use app.get_product_key_field() instead",
                      DeprecationWarning, stacklevel=2)
        return self.get_app().get_product_key_field()

    def product_key_title(self, key=None):
        """
        Deprecated; instead please see
        :meth:`rattail.app.AppHandler.get_product_key_label()`.
        """
        warnings.warn("config.product_key_title() is deprecated; please "
                      "use app.get_product_key_label() instead",
                      DeprecationWarning, stacklevel=2)
        return self.get_app().get_product_key_label(field=key)

    def app_package(self, default=None):
        """
        Returns the name of Python package for the top-level app.
        """
        kwargs = {}
        if default:
            kwargs['default'] = default
        else:
            kwargs['require'] = True
        return self.get('rattail.app_package', **kwargs)

    def app_title(self, **kwargs):
        """ DEPRECATED """
        # TODO: should put a deprecation warning here, but it could
        # make things noisy for a while and i'm not ready for that
        app = self.get_app()
        return app.get_title(**kwargs)

    def node_title(self, **kwargs):
        """ DEPRECATED """
        # TODO: should put a deprecation warning here, but it could
        # make things noisy for a while and i'm not ready for that
        app = self.get_app()
        return app.get_node_title(**kwargs)

    def running_from_source(self):
        """
        Returns boolean indicating whether the app is running from
        source, as opposed to official release.
        """
        return self.get_bool('rattail.running_from_source', default=False)

    def demo(self):
        """
        Returns boolean indicating whether the app is running in demo mode
        """
        return self.get_bool('rattail.demo', default=False)

    def appdir(self, require=True, **kwargs):
        """
        Returns path to the 'app' dir, if known.
        """
        if require:
            path = os.path.join(sys.prefix, 'app')
            kwargs.setdefault('default', path)
        kwargs.setdefault('usedb', False)
        return self.get('rattail.appdir', **kwargs)

    def datadir(self, require=True):
        """
        Returns path to the 'data' dir, if known.
        """
        return self.get('rattail.datadir', require=require)

    def workdir(self, require=True):
        """
        Returns path to the 'work' dir, if known.
        """
        return self.get('rattail.workdir', require=require)

    def batch_filedir(self, key=None):
        """
        Returns path to root folder where batches (optionally of type 'key')
        are stored.
        """
        path = os.path.abspath(self.require('rattail.batch.files'))
        if key:
            return os.path.join(path, key)
        return path

    def batch_filepath(self, key, uuid, filename=None, makedirs=False):
        """
        Returns absolute path to a batch's data folder, with optional
        filename appended.  If ``makedirs`` is set, the batch data
        folder will be created if it does not already exist.
        """
        rootdir = self.batch_filedir(key)
        filedir = os.path.join(rootdir, uuid[:2], uuid[2:])
        if makedirs and not os.path.exists(filedir):
            os.makedirs(filedir)
        if filename:
            return os.path.join(filedir, filename)
        return filedir

    def export_filedir(self, key=None):
        """
        Returns path to root folder where exports (optionally of type 'key')
        are stored.
        """
        path = self.get('rattail.export.files')
        if not path:
            path = os.path.join(self.appdir(), 'data', 'exports')
        path = os.path.abspath(path)
        if key:
            return os.path.join(path, key)
        return path

    def export_filepath(self, key, uuid, filename=None, makedirs=False):
        """
        Returns absolute path to export data file, generated from the given args.
        """
        rootdir = self.export_filedir(key)
        filedir = os.path.join(rootdir, uuid[:2], uuid[2:])
        if makedirs and not os.path.exists(filedir):
            os.makedirs(filedir)
        if filename:
            return os.path.join(filedir, filename)
        return filedir

    def upgrade_filedir(self):
        """
        Returns path to root folder where upgrade files are stored.
        """
        path = os.path.abspath(self.require('rattail.upgrades.files'))
        return path

    def upgrade_filepath(self, uuid, filename=None, makedirs=False):
        """
        Returns absolute path to upgrade data file, generated from the given args.
        """
        rootdir = self.upgrade_filedir()
        filedir = os.path.join(rootdir, uuid[:2], uuid[2:])
        if makedirs and not os.path.exists(filedir):
            os.makedirs(filedir)
        if filename:
            return os.path.join(filedir, filename)
        return filedir

    def upgrade_command(self, default='/bin/sleep 30'):
        """
        Returns command to be used when performing upgrades.
        """
        # TODO: what were those reasons then..?
        # NOTE: we don't allow command to be specified in DB, for
        # security reasons..
        return self.get_list('rattail.upgrades.command', usedb=False,
                             default=default)

    def base_url(self):
        """
        Returns the configured "base" (root) URL for the web app.
        """
        # first try "generic" config option
        url = self.get('rattail.base_url')

        # or use tailbone as fallback, since it's most likely
        if url is None:
            url = self.get('tailbone.url')

        if url is not None:
            return url.rstrip('/')

    def datasync_url(self, **kwargs):
        """
        Returns configured URL for managing datasync daemon.
        """
        return self.get('rattail.datasync.url', **kwargs)

    def single_store(self):
        """
        Returns boolean indicating whether the system is configured to behave
        as if it belongs to a single Store.
        """
        return self.get_bool('rattail.single_store', default=False)

    def get_store(self, session):
        """
        Returns a :class:`rattail.db.model.Store` instance corresponding to app
        config, or ``None``.
        """
        store = self.get('rattail.store')
        if store:
            app = self.get_app()
            org_handler = app.get_org_handler()
            return org_handler.get_store(session, store)

    # TODO: use this or lose it etc.
    def beaker_invalidate_setting(self, name):
        # if not self.beaker_caching:
        #     return

        # # tell beaker to remove the cached value for this setting
        # self.beaker_config_cache.remove_value(key=name)

        pass


class RattailConfig(object):
    """
    .. note::

       This class has served us well over the years, but will soon be
       replaced with :class:`RattailConfiguration`.  See docs for that
       new class if you wish to enable it in your app.

    Rattail config object; this represents the sum total of configuration
    available to the running app.  The actual config available falls roughly
    into two categories: the "defaults" and the "db" (more on these below).
    The general idea here is that one might wish to provide some default
    settings within some config file(s) and/or the command line itself, but
    then allow all settings found in the database to override those defaults.
    However, all variations on this theme are supported, e.g. "use db settings
    but prefer those from file", "never use db settings", and so on.

    As for the "defaults" aspect of the config, this is read only once upon
    application startup.  It almost certainly involves one (or more) config
    file(s), but in addition to that, the application itself is free to embed
    default settings within the config object.  When this occurs, there will be
    no distinction made between settings which came from a file versus those
    which were established as defaults by the application logic.

    As for the "db" aspect of the config, of course this ultimately hinges upon
    the config defaults.  If a default Rattail database connection is defined,
    then the ``Setting`` table within that database may also be consulted for
    config values.  When this is done, the ``Setting.name`` is determined by
    concatenating the ``section`` and ``option`` arguments from the
    :meth:`get()` call, with a period (``'.'``) in between.
    """

    def __init__(self, files=[], usedb=None, preferdb=None):
        self.files_requested = []
        self.files_read = []
        self.parser = configparser.ConfigParser()
        for path in files:
            self.read_file(path)
        self.usedb = usedb
        if self.usedb is None:
            self.usedb = self.getbool('rattail.config', 'usedb', usedb=False, default=False)
        self.preferdb = preferdb
        if self.usedb and self.preferdb is None:
            self.preferdb = self.getbool('rattail.config', 'preferdb', usedb=False, default=False)

        # Attempt to detect lack of SQLAlchemy libraries etc.  This allows us
        # to avoid installing those on a machine which will not need to access
        # a database etc.
        if self.usedb:
            try:
                from rattail.db import Session
            except ImportError: # pragma: no cover
                log.warning("config created with `usedb = True`, but can't import "
                            "`rattail.db.Session`, so setting `usedb = False` instead",
                            exc_info=True)
                self.usedeb = False
                self.preferdb = False

        # this is always false, unless/until it becomes true
        self.versioning_has_been_enabled = False

        # should we use beaker caching?
        self.beaker_caching = self.getbool('rattail.config', 'beaker_cache.enabled',
                                           usedb=False, default=False)
        if self.beaker_caching:
            from beaker.cache import CacheManager
            from beaker.util import parse_cache_config_options

            # default cache settings
            namespace = None
            options = {
                'cache.type': 'file',
                'cache.data_dir': os.path.join(self.appdir(), 'cache',
                                               'config', 'data'),
                'cache.lock_dir': os.path.join(self.appdir(), 'cache',
                                               'config', 'lock'),
            }

            # but let config override and supplement
            if self.parser.has_section('rattail.config'):
                for option in self.parser.options('rattail.config'):
                    if option == 'beaker_cache.namespace':
                        namespace = self.parser.get('rattail.config', option)
                        continue
                    prefix = 'beaker_cache.'
                    if option.startswith(prefix):
                        key = 'cache.{}'.format(option[len(prefix):])
                        options[key] = self.parser.get('rattail.config', option)

            # and with those options, make a cache manager
            self.beaker_cache_manager = CacheManager(
                **parse_cache_config_options(options))

            # use app-specific namespace in case multiple apps use the
            # same (e.g. memcached) backend.  note that we're making a
            # "best faith" effort here; using the name of the python
            # environment root dir.
            if not namespace:
                appdir = self.appdir()
                rootdir = os.path.dirname(appdir)
                envname = os.path.basename(rootdir)
                namespace = 'rattail.config:{}'.format(envname)

            # and finally, make our cache
            self.beaker_config_cache = self.beaker_cache_manager.get_cache(
                namespace)

    def read_file(self, path, recurse=True, require=False):
        """
        Read in config from the given file.

        By default this will "crawl" the file and recursively read in
        any other config files which this one "includes" (or
        "requires").

        :param path: Path to the config file to read.

        :param recurse: Whether the file should be recursively
           "crawled" as described above.

        :param require: If true, and the given file path is not
           readable, will raise an error.
        """
        path = os.path.abspath(path)
        if path in self.files_requested:
            log.debug("ignoring config file which was already requested: {0}".format(path))
            return

        log.debug("will attempt to read config from file: {0}".format(path))
        self.files_requested.append(path)

        parser = configparser.ConfigParser(dict(
            here=os.path.dirname(path),
        ))
        if not parser.read(path):
            log.debug("ConfigParser.read() failed")
            if require:
                raise RuntimeError("Cannot read from config file path: {}".format(path))
            return

        # If recursing, walk the complete config file inheritance chain.
        if recurse:
            if parser.has_section('rattail.config'):

                # first bring in any "required" files
                if parser.has_option('rattail.config', 'require'):
                    includes = self.parse_list(
                        parser.get('rattail.config', 'require'))
                    for included in includes:
                        self.read_file(included, recurse=True, require=True)

                # next try to bring in any "included" files
                if parser.has_option('rattail.config', 'include'):
                    includes = self.parse_list(
                        parser.get('rattail.config', 'include'))
                    for included in includes:
                        self.read_file(included, recurse=True)

        # Okay, now we can finally read this file into our main parser.
        self.parser.read(path)
        self.files_read.append(path)
        log.info("config was read from file: {0}".format(path))

    def configure_logging(self):
        """
        This first checks current config to determine whether or not we're
        supposed to be configuring logging at all.  If not, nothing more is
        done.

        If we are to configure logging, then this will save the current config
        parser defaults to a temporary file, and use this file to configure
        Python's standard logging module.
        """
        if not self.getbool('rattail.config', 'configure_logging', usedb=False, default=False):
            return

        # Coerce all logged timestamps to the local timezone, if possible.
        timezone = self.get('rattail', 'timezone.default', usedb=False)
        if timezone:
            logging.Formatter.converter = TimeConverter(self)

        # Flush all current config to a single file, for input to fileConfig().
        path = temp_path(suffix='.conf')
        with open(path, 'wt') as f:
            self.parser.write(f)

        try:
            logging.config.fileConfig(path, disable_existing_loggers=False)
        except configparser.NoSectionError as error:
            log.warning("tried to configure logging, but got NoSectionError: {0}".format(error))
        else:
            log.debug("configured logging")
        finally:
            os.remove(path)

        # if we could not coerce timestamps, log a warning about that
        if not timezone:
            log.warning("timezone is not set, so logging timestamps may "
                        "appear \"off\" - to fix, set a config value for "
                        "[rattail] timezone.default")

    def setdefault(self, section, option, value):
        """
        Establishes a new default for the given setting, if none exists yet.
        The effective default value is returned in all cases.
        """
        exists = True
        if not self.parser.has_section(section):
            self.parser.add_section(section)
            exists = False
        elif not self.parser.has_option(section, option):
            exists = False
        if not exists:
            self.parser.set(section, option, value)
        return self.parser.get(section, option)

    def set(self, section, option, value):
        """
        Set a value within the config's parser data set, i.e. the "defaults".
        This should probably be used sparingly, though one expected use is
        within tests (for convenience).
        """
        if not self.parser.has_section(section):
            self.parser.add_section(section)
        self.parser.set(section, option, value)

    def get(self, section, option, usedb=None, preferdb=None, session=None, default=None):
        """
        Retrieve a value from config.
        """
        usedb = usedb if usedb is not None else self.usedb
        if usedb:
            preferdb = preferdb if preferdb is not None else getattr(self, 'preferdb', False)
        else:
            preferdb = False
        
        if usedb and preferdb:
            value = self._getdb(section, option, session=session)
            if value is not None:
                return value

        if self.parser.has_option(section, option):
            return self.parser.get(section, option)

        if usedb and not preferdb:
            value = self._getdb(section, option, session=session)
            if value is not None:
                return value

        return default

    def _getdb(self, section, option, session=None):
        """
        Retrieve a config value from database settings table.
        """
        app = self.get_app()
        name = '{}.{}'.format(section, option)

        if self.beaker_caching:
            return self._getdb_beaker(section, option)

        close = False
        if not session:
            # nb. avoid continuum user lookup
            session = app.make_session(continuum_user=None)
            close = True

        value = app.get_setting(session, name)

        if close:
            session.close()

        return value

    def _getdb_beaker(self, section, option):
        """
        Retrieve a config value from database settings table.
        """
        app = self.get_app()
        name = '{}.{}'.format(section, option)

        def get_value():
            # nb. avoid continuum user lookup
            session = app.make_session(continuum_user=None)
            value = app.get_setting(session, name)
            session.close()
            log.debug("had to (re-)fetch setting '%s' from db: %s", name, value)
            return value

        return self.beaker_config_cache.get(key=name, createfunc=get_value)

    def beaker_invalidate_setting(self, name):
        if not self.beaker_caching:
            return

        # tell beaker to remove the cached value for this setting
        self.beaker_config_cache.remove_value(key=name)

    def setdb(self, section, option, value, session=None):
        """
        Set a config value in the database settings table.  Note that the
        ``value`` arg should be a Unicode object.
        """
        app = self.get_app()

        close = False
        if not session:
            # nb. avoid continuum user lookup
            session = app.make_session(continuum_user=None)
            close = True

        name = '{}.{}'.format(section, option)
        app.save_setting(session, name, value)

        if close:
            session.commit()
            session.close()

    def getbool(self, *args, **kwargs):
        """
        Retrieve a boolean value from config.
        """
        value = self.get(*args, **kwargs)
        return parse_bool(value)

    def getint(self, *args, **kwargs):
        """
        Retrieve an integer value from config.
        """
        value = self.get(*args, **kwargs)
        if value is None:
            return None
        if value == '' and 'default' in kwargs:
            return kwargs['default']
        if isinstance(value, int):
            return value
        return int(value)

    def getdate(self, *args, **kwargs):
        """
        Retrieve a date value from config.
        """
        value = self.get(*args, **kwargs)
        app = self.get_app()
        return app.parse_date(value)

    def getlist(self, *args, **kwargs):
        """
        Retrieve a list of string values from a single config option.
        """
        value = self.get(*args, **kwargs)
        if value is None:
            return None
        if isinstance(value, str):
            return self.parse_list(value)
        return value            # maybe a caller-provided default?

    def parse_bool(self, value):
        return parse_bool(value)

    def parse_list(self, value):
        return parse_list(value)

    def make_list_string(self, values):
        """
        Coerce the given list of values to a string, for config
        storage.  If this string is later parsed via
        :meth:`parse_list()` then it should return the same list of
        values.
        """
        final = []
        for value in values:
            if ' ' in value:
                quote = '"' if "'" in value else "'"
                value = f"{quote}{value}{quote}"
            final.append(value)
        return ', '.join(final)

    def get_dict(self, section):
        """
        Convenience method which returns a dictionary of options contained
        within the given section.  Note that this method only supports the
        "default" config settings, i.e. those within the underlying parser.
        """
        settings = {}
        if self.parser.has_section(section):
            for option in self.parser.options(section):
                settings[option] = self.parser.get(section, option)
        return settings

    def require(self, section, option, **kwargs):
        """
        Fetch a value from current config, and raise an error if no value can
        be found.
        """
        if 'default' in kwargs:
            warnings.warn("You have provided a default value to the `RattailConfig.require()` "
                          "method.  This is allowed but also somewhat pointless, since `get()` "
                          "would suffice if a default is known.", UserWarning)

        msg = kwargs.pop('msg', None)
        value = self.get(section, option, **kwargs)
        if value is not None:
            return value

        if msg is None:
            msg = "Missing or invalid config"
        msg = "{0}; please set '{1}' in the [{2}] section of your config file".format(
            msg, option, section)
        raise ConfigurationError(msg)

    ##############################
    # convenience methods
    ##############################

    def get_app(self):
        """
        Returns the global Rattail ``AppHandler`` instance, creating it first
        if necessary.
        """
        if not hasattr(self, 'app'):
            spec = self.get('rattail', 'app.handler', usedb=False,
                            default='rattail.app:AppHandler')
            factory = load_object(spec)
            self.app = factory(self)
        return self.app

    def app_package(self, default=None):
        """
        Returns the name of Python package for the top-level app.
        """
        if not default:
            return self.require('rattail', 'app_package')
        return self.get('rattail', 'app_package', default=default)

    def app_title(self, **kwargs):
        """ DEPRECATED """
        # TODO: should put a deprecation warning here, but it could
        # make things noisy for a while and i'm not ready for that
        app = self.get_app()
        return app.get_title(**kwargs)

    def node_title(self, **kwargs):
        """ DEPRECATED """
        # TODO: should put a deprecation warning here, but it could
        # make things noisy for a while and i'm not ready for that
        app = self.get_app()
        return app.get_node_title(**kwargs)

    def node_type(self, default=None):
        """
        Returns the "type" of current node.  What this means will generally
        depend on the app logic.
        """
        try:
            return self.require('rattail', 'node_type', usedb=False)
        except ConfigurationError:
            if default:
                return default
            raise

    def production(self):
        """
        Returns boolean indicating whether the app is running in production mode
        """
        return self.getbool('rattail', 'production', default=False)

    def running_from_source(self):
        """
        Returns boolean indicating whether the app is running from
        source, as opposed to official release.
        """
        return self.getbool('rattail', 'running_from_source', default=False)

    def demo(self):
        """
        Returns boolean indicating whether the app is running in demo mode
        """
        return self.getbool('rattail', 'demo', default=False)

    def versioning_enabled(self):
        """
        Returns boolean indicating whether data versioning is enabled.
        """
        return self.getbool('rattail.db', 'versioning.enabled', usedb=False,
                            default=False)

    def appdir(self, require=True, **kwargs):
        """
        Returns path to the 'app' dir, if known.
        """
        if require:
            path = os.path.join(sys.prefix, 'app')
            kwargs.setdefault('default', path)
        kwargs.setdefault('usedb', False)
        return self.get('rattail', 'appdir', **kwargs)

    def datadir(self, require=True):
        """
        Returns path to the 'data' dir, if known.
        """
        get = self.require if require else self.get
        return get('rattail', 'datadir')

    def workdir(self, require=True):
        """
        Returns path to the 'work' dir, if known.
        """
        get = self.require if require else self.get
        return get('rattail', 'workdir')

    def batch_filedir(self, key=None):
        """
        Returns path to root folder where batches (optionally of type 'key')
        are stored.
        """
        path = os.path.abspath(self.require('rattail', 'batch.files'))
        if key:
            return os.path.join(path, key)
        return path

    def batch_filepath(self, key, uuid, filename=None, makedirs=False):
        """
        Returns absolute path to a batch's data folder, with optional filename
        appended.  If ``makedirs`` is set, the batch data folder will be
        created if it does not already exist.
        """
        rootdir = self.batch_filedir(key)
        filedir = os.path.join(rootdir, uuid[:2], uuid[2:])
        if makedirs and not os.path.exists(filedir):
            os.makedirs(filedir)
        if filename:
            return os.path.join(filedir, filename)
        return filedir

    def export_filedir(self, key=None):
        """
        Returns path to root folder where exports (optionally of type 'key')
        are stored.
        """
        path = self.get('rattail', 'export.files')
        if not path:
            path = os.path.join(self.appdir(), 'data', 'exports')
        path = os.path.abspath(path)
        if key:
            return os.path.join(path, key)
        return path

    def export_filepath(self, key, uuid, filename=None, makedirs=False):
        """
        Returns absolute path to export data file, generated from the given args.
        """
        rootdir = self.export_filedir(key)
        filedir = os.path.join(rootdir, uuid[:2], uuid[2:])
        if makedirs and not os.path.exists(filedir):
            os.makedirs(filedir)
        if filename:
            return os.path.join(filedir, filename)
        return filedir

    def upgrade_filedir(self):
        """
        Returns path to root folder where upgrade files are stored.
        """
        path = os.path.abspath(self.require('rattail.upgrades', 'files'))
        return path

    def upgrade_filepath(self, uuid, filename=None, makedirs=False):
        """
        Returns absolute path to upgrade data file, generated from the given args.
        """
        rootdir = self.upgrade_filedir()
        filedir = os.path.join(rootdir, uuid[:2], uuid[2:])
        if makedirs and not os.path.exists(filedir):
            os.makedirs(filedir)
        if filename:
            return os.path.join(filedir, filename)
        return filedir

    def upgrade_command(self, default='/bin/sleep 30'):
        """
        Returns command to be used when performing upgrades.
        """
        # NOTE: we don't allow command to be specified in DB, for security reasons..
        return self.getlist('rattail.upgrades', 'command', default=default, usedb=False)

    def base_url(self):
        """
        Returns the configured "base" (root) URL for the web app.
        """
        # first try "generic" config option
        url = self.get('rattail', 'base_url')

        # or use tailbone as fallback, since it's most likely
        if url is None:
            url = self.get('tailbone', 'url')

        if url is not None:
            return url.rstrip('/')

    def datasync_url(self, **kwargs):
        """
        Returns configured URL for managing datasync daemon.
        """
        return self.get('rattail.datasync', 'url', **kwargs)

    def get_enum(self, **kwargs):
        """
        Returns a reference to configured 'enum' module; defaults to
        :mod:`rattail.enum`.
        """
        kwargs.setdefault('usedb', False)
        spec = self.get('rattail', 'enum', default='rattail.enum', **kwargs)
        return importlib.import_module(spec)

    def get_model(self):
        """
        Returns a reference to configured 'model' module; defaults to
        :mod:`rattail.db.model`.
        """
        spec = self.get('rattail', 'model', default='rattail.db.model', usedb=False)
        return importlib.import_module(spec)

    def get_trainwreck_model(self):
        """
        Returns a reference to the configured data 'model' module for
        Trainwreck.  Note that there is *not* a default value for this; it must
        be configured.
        """
        spec = self.require('rattail.trainwreck', 'model', usedb=False)
        return importlib.import_module(spec)

    def product_key(self, **kwargs):
        """
        Deprecated; instead please see
        :meth:`rattail.app.AppHandler.get_product_key_field()`.
        """
        warnings.warn("config.product_key() is deprecated; please "
                      "use app.get_product_key_field() instead",
                      DeprecationWarning, stacklevel=2)
        return self.get_app().get_product_key_field()

    def product_key_title(self, key=None):
        """
        Deprecated; instead please see
        :meth:`rattail.app.AppHandler.get_product_key_label()`.
        """
        warnings.warn("config.product_key_title() is deprecated; please "
                      "use app.get_product_key_label() instead",
                      DeprecationWarning, stacklevel=2)
        return self.get_app().get_product_key_label(field=key)

    def single_store(self):
        """
        Returns boolean indicating whether the system is configured to behave
        as if it belongs to a single Store.
        """
        return self.getbool('rattail', 'single_store', default=False)

    def get_store(self, session):
        """
        Returns a :class:`rattail.db.model.Store` instance corresponding to app
        config, or ``None``.
        """
        store = self.get('rattail', 'store')
        if store:
            app = self.get_app()
            org_handler = app.get_org_handler()
            return org_handler.get_store(session, store)


    ##############################
    # deprecated methods
    ##############################

    def options(self, section):
        warnings.warn("RattailConfig.option() is deprecated, please find "
                      "another way to accomplish what you're after.",
                      DeprecationWarning, stacklevel=2)
        return self.parser.options(section)

    def has_option(self, section, option):
        warnings.warn("RattailConfig.has_option() is deprecated, please find "
                      "another way to accomplish what you're after.",
                      DeprecationWarning, stacklevel=2)
        return self.parser.has_option(section, option)


class ConfigExtension(object):
    """
    Base class for all config extensions.
    """
    key = None

    def __repr__(self):
        return "ConfigExtension(key={0})".format(repr(self.key))

    def configure(self, config):
        """
        All subclasses should override this method, to extend the config object
        in any way necessary etc.
        """


def make_config(
        files=None,
        plus_files=None,
        usedb=None,
        preferdb=None,
        env=None,
        winsvc=None,
        extend=True,
        versioning=None):
    """
    Returns a new config object, initialized with the given parameters and
    further modified by all registered config extensions.

    :param files: Config path(s) to be loaded.  If not specified, then some
       "default" behavior will be attempted.  This will check for env var
       ``RATTAIL_CONFIG_FILES`` or fallback to system default paths.  Or
       you can override all that by specifying some path(s) here.

    :param plus_files: Additional config path(s) to be loaded.  You
       may specify a "config tweak" file here, and leave ``files``
       empty, to get "normal plus tweak" behavior.

    :param versioning: Controls whether or not the versioning system is
       configured with the new config object.  If ``True``, versioning will be
       configured.  If ``False`` then it will not be configured.  If ``None``
       (the default) then versioning will be configured only if the config
       object itself says that it should be.
    """
    if env is None:
        env = os.environ
    if files is None:
        files = env.get('RATTAIL_CONFIG_FILES')
        if files is not None:
            files = files.split(os.pathsep)
        else:
            # try to guess a default config path
            # TODO: for now, prefer app/quiet.conf if present, but
            # probably we should look for adhoc.conf instead, since
            # the point of this magic is to make running ad-hoc
            # commands easier..
            quiet = os.path.join(sys.prefix, 'app', 'quiet.conf')
            if os.path.exists(quiet):
                # this config is definitely app-specific
                files = [quiet]
            else:
                # generic fallback, probably not very useful
                files = default_system_paths() + default_user_paths()
    elif isinstance(files, str):
        files = [files]

    if plus_files:
        if isinstance(plus_files, str):
            plus_files = [plus_files]
        files += plus_files

    # If making config for a Windows service, we must read the default config
    # file(s) first, and check it to see if there is an alternate config file
    # which should be considered the "root" file.  Normally we specify the root
    # config file(s) via command line etc., but there is no practical way to
    # pass parameters to a Windows service.  This way we can effectively do
    # just that, via config.
    if winsvc is not None:
        parser = configparser.SafeConfigParser()
        parser.read(files)
        if parser.has_section('rattail.config'):
            key = 'winsvc.{0}'.format(winsvc)
            if parser.has_option('rattail.config', key):
                files = parse_list(parser.get('rattail.config', key))

    # Initial config object will have values read from the given file paths,
    # and kwargs, but no other app defaults etc. will have been applied yet.
    config = RattailConfigWrapper(files, usedb=usedb, preferdb=preferdb)
    config.configure_logging()
    log.debug("using config object of type: %s",
              config.config.__class__.__name__)
    log.debug("config files were: %s", config.files_read)

    # turn on display of rattail deprecation warnings by default
    # TODO: this should be configurable, and possibly live elsewhere?
    warnings.filterwarnings('default', category=DeprecationWarning,
                            module=r'^rattail')
    warnings.filterwarnings('default', category=DeprecationWarning,
                            module=r'^tailbone')

    if config.getbool('rattail', 'suppress_psycopg2_wheel_warning', usedb=False):
        # TODO: revisit this, does it require action from us?
        # suppress this warning about psycopg2 wheel; not sure what it means yet
        # exactly but it's causing frequent noise for us...
        warnings.filterwarnings(
            'ignore',
            r'^The psycopg2 wheel package will be renamed from release 2\.8; in order to keep '
            r'installing from binary please use "pip install psycopg2-binary" instead\. For details '
            r'see: <http://initd.org/psycopg/docs/install.html#binary-install-from-pypi>\.',
            UserWarning,
            r'^psycopg2$',
        )

    # Apply extra config for all available extensions.
    if extend:
        extensions = load_entry_points('rattail.config.extensions')
        for extension in extensions.values():
            log.debug("applying '{0}' config extension".format(extension.key))
            extension().configure(config)

    # maybe configure versioning
    if versioning is None:
        versioning = config.versioning_enabled()
    if versioning:
        from rattail.db.config import configure_versioning
        configure_versioning(config)

    # maybe set "future" behavior for SQLAlchemy
    if config.getbool('rattail.db', 'sqlalchemy_future_mode', usedb=False):
        from rattail.db import Session
        if Session:
            Session.configure(future=True)

    return config


def default_system_paths():
    """
    Returns a list of default system-level config file paths, according to the
    current platform.
    """
    if sys.platform == 'win32':

        # Use the Windows Extensions libraries to fetch official defaults.
        try:
            from win32com.shell import shell, shellcon
        except ImportError:
            # raise WindowsExtensionsNotInstalled
            return []
        else:
            return [
                os.path.join(shell.SHGetSpecialFolderPath(
                    0, shellcon.CSIDL_COMMON_APPDATA), 'rattail.conf'),
                os.path.join(shell.SHGetSpecialFolderPath(
                    0, shellcon.CSIDL_COMMON_APPDATA), 'rattail', 'rattail.conf'),
            ]

    return [
        '/etc/rattail.conf',
        '/etc/rattail/rattail.conf',
        '/usr/local/etc/rattail.conf',
        '/usr/local/etc/rattail/rattail.conf',
    ]


def default_user_paths():
    """
    Returns a list of default user-level config file paths, according to the
    current platform.
    """
    if sys.platform == 'win32':

        # Use the Windows Extensions libraries to fetch official defaults.
        try:
            from win32com.shell import shell, shellcon
        except ImportError:
            # raise WindowsExtensionsNotInstalled
            return []
        else:
            return [
                os.path.join(shell.SHGetSpecialFolderPath(
                    0, shellcon.CSIDL_APPDATA), 'rattail.conf'),
                os.path.join(shell.SHGetSpecialFolderPath(
                    0, shellcon.CSIDL_APPDATA), 'rattail', 'rattail.conf'),
            ]

    return [
        os.path.expanduser('~/.rattail.conf'),
        os.path.expanduser('~/.rattail/rattail.conf'),
    ]


def get_user_dir(create=False):
    """
    Returns a path to the "preferred" user-level folder, in which additional
    config files (etc.) may be placed as needed.  This essentially returns a
    platform-specific variation of ``~/.rattail/``.

    If ``create`` is ``True``, then the folder will be created if it does not
    already exist.
    """
    if sys.platform == 'win32':

        # Use the Windows Extensions libraries to fetch official defaults.
        try:
            from win32com.shell import shell, shellcon
        except ImportError:
            raise WindowsExtensionsNotInstalled
        else:
            path = os.path.join(shell.SHGetSpecialFolderPath(
                0, shellcon.CSIDL_APPDATA), 'rattail')

    else:
        path = os.path.expanduser('~/.rattail')

    if create and not os.path.exists(path):
        os.mkdir(path)
    return path


def get_user_file(filename, createdir=False):
    """
    Returns a full path to a user-level config file location.  This is obtained
    by first calling :func:`get_user_dir()` and then joining the result with
    ``filename``.

    The ``createdir`` argument will be passed to :func:`get_user_dir()` as its
    ``create`` arg, and may be used to ensure the user-level folder exists.
    """
    return os.path.join(get_user_dir(create=createdir), filename)


class ConfigProfile(object):
    """
    Generic class to represent a config "profile", as used by the filemon and
    datasync daemons, etc.

    .. todo::

       This clearly needs more documentation.

    .. attribute:: config

       Reference to the primary Rattail config object for the running app.

    .. attribute:: key

       String identifier unique to this profile, within the broader
       config section.
    """

    def __init__(self, config, key, **kwargs):
        self.config = config
        self.app = self.config.get_app()
        self.model = self.config.get_model()
        self.enum = self.config.get_enum()
        self.key = key
        self.prefix = kwargs.pop('prefix', key)
        self.load()

    def load(self):
        """
        Read all relevant settings etc. from the config object,
        setting attributes on this profile instance as needed.
        """

    def load_defaults(self):
        """
        Read all "default" (common) settings from config, for the
        current profile.
        """
        self.workdir = self._config_string('workdir')
        self.stop_on_error = self._config_boolean('stop_on_error', False)

    def load_actions(self):
        """
        Read the "actions" from config, for the current profile, and
        assign the result to ``self.actions``.
        """
        self.actions = []
        for action in self._config_list('actions'):
            self.actions.append(self._config_action(action))

    @property
    def section(self):
        """
        Each subclass of ``ConfigProfile`` must define this.
        """
        raise NotImplementedError

    def _config_string(self, option, **kwargs):
        return self.config.get(self.section,
                               '{}.{}'.format(self.prefix, option),
                               **kwargs)

    def _config_boolean(self, option, default=None):
        return self.config.getbool(self.section,
                                   '{}.{}'.format(self.prefix, option),
                                   default=default)

    def _config_int(self, option, minimum=1, default=None):
        """
        Retrieve the *integer* value for the given option.
        """
        option = '{}.{}'.format(self.prefix, option)

        # try to read value from config
        value = self.config.getint(self.section, option)
        if value is not None:

            # found a value; validate it
            if value < minimum:
                log.warning("config value %s is too small; falling back to minimum "
                            "of %s for option: %s", value, minimum, option)
                value = minimum

        # or, use default value, if valid
        elif default is not None and default >= minimum:
            value = default

        # or, just use minimum value
        else:
            value = minimum

        return value

    def _config_list(self, option, default=None, **kwargs):
        value = self._config_string(option, **kwargs)
        if value:
            return self.config.parse_list(value)

        if isinstance(default, list):
            return default

        return []

    def _config_action(self, name):
        """
        Retrieve an "action" value from config, for the current
        profile.  This returns a :class:`ConfigProfileAction`
        instance.
        """
        from rattail.monitoring import CommandAction

        function = self._config_string('action.{}.func'.format(name))
        class_ = self._config_string('action.{}.class'.format(name))
        cmd = self._config_string('action.{}.cmd'.format(name))

        specs = [1 if spec else 0 for spec in (function, class_, cmd)]
        if sum(specs) != 1:
            raise ConfigurationError(
                "Monitor profile '{}' (action '{}') must have exactly one of: "
                "function, class, command".format(self.prefix, name))

        action = ConfigProfileAction()
        action.config = self.config

        if function:
            action.spec = function
            action.action = load_object(action.spec)
        elif class_:
            action.spec = class_
            action.action = load_object(action.spec)(self.config)
        elif cmd:
            action.spec = cmd
            action.action = CommandAction(self.config, cmd)

        action.args = self._config_list('action.{}.args'.format(name))

        action.kwargs = {}
        pattern = re.compile(r'^{}\.action\.{}\.kwarg\.(?P<keyword>\w+)$'.format(self.prefix, name), re.IGNORECASE)
        settings = self.config.get_dict(self.section)
        for key in settings:
            match = pattern.match(key)
            if match:
                action.kwargs[match.group('keyword')] = settings[key]

        action.retry_attempts = self._config_int('action.{}.retry_attempts'.format(name), minimum=1)
        action.retry_delay = self._config_int('action.{}.retry_delay'.format(name), minimum=0)
        return action


class ConfigProfileAction(object):
    """
    Simple class to hold configuration for a particular "action"
    defined within a monitor :class:`ConfigProfile`.  Each instance
    has the following attributes:

    .. attribute:: spec

       The original "spec" string used to obtain the action callable.

    .. attribute:: action

       A reference to the action callable.

    .. attribute:: args

       A sequence of positional arguments to be passed to the callable
       (in addition to the file path) when invoking the action.

    .. attribute:: kwargs

       A dictionary of keyword arguments to be passed to the callable
       (in addition to the positional arguments) when invoking the
       action.

    .. attribute:: retry_attempts

       Number of attempts to make when invoking the action.  Defaults
       to ``1``, meaning the first attempt will be made but no retries
       will happen.

    .. attribute:: retry_delay

       Number of seconds to pause between retry attempts, if
       :attr:`retry_attempts` is greater than one.  Defaults to ``0``.
    """
    spec = None
    action = None
    args = []
    kwargs = {}
    retry_attempts = 1
    retry_delay = 0


class FreeTDSLoggingFilter(logging.Filter):
    """
    Custom logging filter, to suppress certain "write to server failed"
    messages relating to FreeTDS database connections.  They seem harmless and
    just cause unwanted error emails.
    """

    def __init__(self, *args, **kwargs):
        logging.Filter.__init__(self, *args, **kwargs)
        self.pattern = re.compile(r'(?:Read from|Write to) the server failed')

    def filter(self, record):
        if (record.name == 'sqlalchemy.pool.QueuePool'
            and record.funcName == '_finalize_fairy'
            and record.levelno == logging.ERROR
            and record.msg == "Exception during reset or similar"
            and record.exc_info
            and self.pattern.search(str(record.exc_info[1]))):

            # Log this as a warning instead of error, to cut down on our noise.
            record.levelno = logging.WARNING
            record.levelname = 'WARNING'

        return True
