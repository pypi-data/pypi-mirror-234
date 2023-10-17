# -*- coding: utf-8; -*-

import os
import datetime
import decimal
from mock import patch
from unittest import TestCase

import sqlalchemy as sa
from sqlalchemy import orm

from rattail import app as mod
from rattail.config import make_config
from rattail.exceptions import ConfigurationError
from rattail.core import Object
from rattail.db import Session
from rattail.autocomplete import Autocompleter
from rattail.batch import BatchHandler
from rattail.bouncer import BounceHandler
from rattail.importing import ImportHandler
from rattail.importing.rattail import FromRattailToRattailImport
from rattail.gpc import GPC


class TestAppHandler(TestCase):

    def setUp(self):
        self.config = self.make_config()
        self.handler = self.make_handler()

    def make_config(self):
        return make_config([], extend=False)

    def make_handler(self):
        return mod.AppHandler(self.config)

    def test_get_title(self):

        # default for unconfigured title
        self.assertEqual(self.handler.get_title(), "Rattail")

        # unless default is provided
        self.assertEqual(self.handler.get_title(default="Foo"), "Foo")

        # or title can be configured
        self.config.setdefault('rattail', 'app_title', 'Bar')
        self.assertEqual(self.handler.get_title(), "Bar")
        self.assertEqual(self.handler.get_title(default="Foo"), "Bar")

    def test_get_timezone(self):

        # unconfigured zone causes error
        self.assertRaises(ConfigurationError, self.handler.get_timezone)

        # or one can be configured
        self.config.setdefault('rattail', 'timezone.default', 'America/Chicago')
        self.assertEqual(str(self.handler.get_timezone()), 'America/Chicago')

        # also can configure alternate zones
        self.assertRaises(ConfigurationError, self.handler.get_timezone, key='other')
        self.config.setdefault('rattail', 'timezone.other', 'America/New_York')
        self.assertEqual(str(self.handler.get_timezone(key='other')), 'America/New_York')

    def test_localtime(self):

        # must define timezone first
        self.config.setdefault('rattail', 'timezone.default', 'America/Chicago')

        # just confirm the method works on a basic level; the
        # underlying function is tested elsewhere
        now = self.handler.localtime()
        self.assertIsNotNone(now)

    def test_make_utc(self):

        # just confirm the method works on a basic level; the
        # underlying function is tested elsewhere
        now = self.handler.make_utc()
        self.assertIsNotNone(now)

    def test_load_object(self):

        # just confirm the method works on a basic level; the
        # underlying function is tested elsewhere
        cls = self.handler.load_object('rattail.core:Object')
        self.assertIs(cls, Object)

    def test_get_active_stores(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)

        # no stores by default
        stores = self.handler.get_active_stores(session)
        self.assertEqual(len(stores), 0)

        # add a basic store
        store001 = model.Store(id='001')
        session.add(store001)
        session.flush()
        session.refresh(store001)
        self.assertIsNone(store001.archived)

        # that one store should be returned
        stores = self.handler.get_active_stores(session)
        self.assertEqual(len(stores), 1)
        self.assertIs(stores[0], store001)

        # archive first store; add another
        store001.archived = True
        store002 = model.Store(id='002')
        session.add(store002)
        session.flush()
        
        # now only store 002 should be returned
        stores = self.handler.get_active_stores(session)
        self.assertEqual(len(stores), 1)
        self.assertIs(stores[0], store002)

        session.rollback()
        session.close()

    def test_get_autocompleter(self):

        # built-in autocompleter should be got okay
        from rattail.autocomplete.products import ProductAutocompleter
        autocompleter = self.handler.get_autocompleter('products')
        self.assertIsInstance(autocompleter, ProductAutocompleter)

        # now let's invent one, but first make sure it is not yet valid
        self.assertRaises(ValueError, self.handler.get_autocompleter, 'foobars')

        # okay now configure it and then it should be got okay
        self.config.setdefault('rattail', 'autocomplete.foobars',
                               'tests.test_app:FooBarAutocompleter')
        autocompleter = self.handler.get_autocompleter('foobars')
        self.assertIsInstance(autocompleter, FooBarAutocompleter)

    def test_get_auth_handler(self):
        
        # first call gets the default handler
        auth01 = self.handler.get_auth_handler()
        self.assertIsNotNone(auth01)

        # second call gets the same handler instance
        auth02 = self.handler.get_auth_handler()
        self.assertIs(auth02, auth01)

    def test_get_batch_handler(self):

        # unknown batch type raises error by default
        self.assertRaises(ValueError, self.handler.get_batch_handler, 'foobar')

        # or returns None if error is suppressed
        bhandler = self.handler.get_batch_handler('foobar', error=False)
        self.assertIsNone(bhandler)

        # but we can provide our own spec
        bhandler = self.handler.get_batch_handler(
            'foobar', default='tests.test_app:FooBarBatchHandler')
        self.assertIsInstance(bhandler, FooBarBatchHandler)

        # we also can configure our handler
        self.config.setdefault('rattail.batch', 'foobar.handler',
                               'tests.test_app:FooBarBatchHandler')
        bhandler = self.handler.get_batch_handler('foobar')
        self.assertIsInstance(bhandler, FooBarBatchHandler)

        # for some reason (?) the "importer" batch handler is special
        # and can be returned with no config
        from rattail.batch.importer import ImporterBatchHandler
        bhandler = self.handler.get_batch_handler('importer')
        self.assertIsInstance(bhandler, ImporterBatchHandler)

    def test_get_board_handler(self):

        # first call gets the default handler
        board01 = self.handler.get_board_handler()
        self.assertIsNotNone(board01)

        # second call gets the same handler instance
        board02 = self.handler.get_board_handler()
        self.assertIs(board02, board01)

    def test_get_bounce_handler(self):

        # unknown type raises error by default
        self.assertRaises(ValueError, self.handler.get_bounce_handler, 'foobar')

        # but we can configure our own too
        self.config.setdefault('rattail.bouncer', 'foobar.handler',
                               'tests.test_app:FooBarBounceHandler')
        bhandler = self.handler.get_bounce_handler('foobar')
        self.assertIsInstance(bhandler, FooBarBounceHandler)

        # default handler is special and works out of the box
        bhandler = self.handler.get_bounce_handler('default')
        self.assertIsInstance(bhandler, BounceHandler)

    def test_get_clientele_handler(self):

        # first call gets the default handler
        client01 = self.handler.get_clientele_handler()
        self.assertIsNotNone(client01)

        # second call gets the same handler instance
        client02 = self.handler.get_clientele_handler()
        self.assertIs(client02, client01)

    def test_get_custorder_handler(self):

        # first call gets the default handler
        custorder01 = self.handler.get_custorder_handler()
        self.assertIsNotNone(custorder01)

        # second call gets the same handler instance
        custorder02 = self.handler.get_custorder_handler()
        self.assertIs(custorder02, custorder01)

    def test_get_employment_handler(self):

        # first call gets the default handler
        employ01 = self.handler.get_employment_handler()
        self.assertIsNotNone(employ01)

        # second call gets the same handler instance
        employ02 = self.handler.get_employment_handler()
        self.assertIs(employ02, employ01)

    def test_get_feature_handler(self):

        # first call gets the default handler
        feature01 = self.handler.get_feature_handler()
        self.assertIsNotNone(feature01)

        # second call gets the same handler instance
        feature02 = self.handler.get_feature_handler()
        self.assertIs(feature02, feature01)

    def test_get_email_handler(self):

        # first call gets the default handler
        email01 = self.handler.get_email_handler()
        self.assertIsNotNone(email01)

        # second call gets the same handler instance
        email02 = self.handler.get_email_handler()
        self.assertIs(email02, email01)

    def test_get_all_import_handlers(self):

        # several default handlers exist, but not our custom handler
        Handlers = self.handler.get_all_import_handlers()
        self.assertTrue(Handlers)
        self.assertNotIn(FromFooToBar, Handlers)

        # and by default there are no errors to be raised
        Handlers = self.handler.get_all_import_handlers(ignore_errors=False)
        self.assertTrue(Handlers)

        # and just to make sure sorting "works" (no error)
        Handlers = self.handler.get_all_import_handlers(sort=True)
        self.assertTrue(Handlers)

        # finally let's configure a custom handler, and be sure it
        # comes back in the result.  note that we must "override" a
        # default importer here, cannot register a new type without
        # creating an entry point
        self.config.setdefault('rattail.importing',
                               'to_rattail.from_rattail.import.handler',
                               'tests.test_app:FromFooToBar')
        Handlers = self.handler.get_all_import_handlers()
        self.assertTrue(Handlers)
        self.assertIn(FromFooToBar, Handlers)

    def test_get_designated_import_handlers(self):

        # several default handlers exist, but not our custom handler
        handlers = self.handler.get_designated_import_handlers()
        self.assertTrue(handlers)
        self.assertFalse(any([isinstance(h, FromFooToBar)
                              for h in handlers]))
        self.assertTrue(any([isinstance(h, FromRattailToRattailImport)
                             for h in handlers]))

        # we can override a default with custom handler
        self.config.setdefault('rattail.importing',
                               'to_rattail.from_rattail.import.handler',
                               'tests.test_app:FromFooToBar')
        handlers = self.handler.get_designated_import_handlers()
        self.assertTrue(any([isinstance(h, FromFooToBar)
                             for h in handlers]))
        self.assertFalse(any([isinstance(h, FromRattailToRattailImport)
                              for h in handlers]))

        # but then original default is included with alternates
        handlers = self.handler.get_designated_import_handlers(with_alternates=True)
        matches = [h for h in handlers
                   if isinstance(h, FromFooToBar)]
        self.assertEqual(len(matches), 1)
        handler = matches[0]
        self.assertEqual(len(handler.alternate_handlers), 1)
        alternate = handler.alternate_handlers[0]
        self.assertIs(alternate, FromRattailToRattailImport)

    def test_get_import_handler(self):

        # make sure a basic fetch works
        handler = self.handler.get_import_handler('to_rattail.from_rattail.import')
        self.assertIsInstance(handler, FromRattailToRattailImport)

        # and make sure custom override works
        self.config.setdefault('rattail.importing',
                               'to_rattail.from_rattail.import.handler',
                               'tests.test_app:FromFooToBar')
        handler = self.handler.get_import_handler('to_rattail.from_rattail.import')

        # unknown importer cannot be found
        handler = self.handler.get_import_handler('this_should_not_work')
        self.assertIsNone(handler)

        # and if we require it, error will raise
        self.assertRaises(ValueError, self.handler.get_import_handler,
                          'this_should_not_work', require=True)

    def test_get_designated_import_handler_spec(self):
        
        # fetch of unknown key returns none
        spec = self.handler.get_designated_import_handler_spec('test01')
        self.assertIsNone(spec)

        # unless we require it, in which case, error
        self.assertRaises(ValueError, self.handler.get_designated_import_handler_spec,
                          'test01', require=True)

        # we configure one for whatever key we like
        self.config.setdefault('rattail.importing',
                               'test02.handler',
                               'tests.test_app:FromFooToBar')
        spec = self.handler.get_designated_import_handler_spec('test02')
        self.assertEqual(spec, 'tests.test_app:FromFooToBar')

        # we can also define a "default" designated handler
        self.config.setdefault('rattail.importing',
                               'test03.default_handler',
                               'tests.test_app:FromFooToBar')
        spec = self.handler.get_designated_import_handler_spec('test03')
        self.assertEqual(spec, 'tests.test_app:FromFooToBar')

        # we can also designate handler w/ legacy config
        # TODO: this should be removed at some point, surely?
        self.config.setdefault('rattail.importing',
                               'test04.legacy_handler_setting',
                               'rattail.importing, test04.custom_handler')
        self.config.setdefault('rattail.importing',
                               'test04.custom_handler',
                               'tests.test_app:FromFooToBar')
        spec = self.handler.get_designated_import_handler_spec('test04')
        self.assertEqual(spec, 'tests.test_app:FromFooToBar')

    def test_get_label_handler(self):

        # first call gets the default handler
        labels01 = self.handler.get_label_handler()
        self.assertIsNotNone(labels01)

        # second call gets the same handler instance
        labels02 = self.handler.get_label_handler()
        self.assertIs(labels01, labels01)

    def test_get_membership_handler(self):

        # first call gets the default handler
        membership01 = self.handler.get_membership_handler()
        self.assertIsNotNone(membership01)

        # second call gets the same handler instance
        membership02 = self.handler.get_membership_handler()
        self.assertIs(membership02, membership01)

    def test_get_people_handler(self):

        # first call gets the default handler
        people01 = self.handler.get_people_handler()
        self.assertIsNotNone(people01)

        # second call gets the same handler instance
        people02 = self.handler.get_people_handler()
        self.assertIs(people02, people01)

    def test_get_products_handler(self):

        # first call gets the default handler
        products01 = self.handler.get_products_handler()
        self.assertIsNotNone(products01)

        # second call gets the same handler instance
        products02 = self.handler.get_products_handler()
        self.assertIs(products02, products01)

    def test_get_report_handler(self):

        # first call gets the default handler
        report01 = self.handler.get_report_handler()
        self.assertIsNotNone(report01)

        # second call gets the same handler instance
        report02 = self.handler.get_report_handler()
        self.assertIs(report02, report01)

    def test_get_problem_report_handler(self):

        # first call gets the default handler
        problems01 = self.handler.get_problem_report_handler()
        self.assertIsNotNone(problems01)

        # second call gets the same handler instance
        problems02 = self.handler.get_problem_report_handler()
        self.assertIs(problems02, problems01)

    def test_get_trainwreck_handler(self):

        # first call gets the default handler
        trainwreck01 = self.handler.get_trainwreck_handler()
        self.assertIsNotNone(trainwreck01)

        # second call gets the same handler instance
        trainwreck02 = self.handler.get_trainwreck_handler()
        self.assertIs(trainwreck02, trainwreck01)

    def test_get_vendor_handler(self):

        # first call gets the default handler
        vendor01 = self.handler.get_vendor_handler()
        self.assertIsNotNone(vendor01)

        # second call gets the same handler instance
        vendor02 = self.handler.get_vendor_handler()
        self.assertIs(vendor02, vendor01)

    def test_progress_loop(self):
        from rattail.progress import ProgressBase

        class NullProgress(ProgressBase):
            pass

        result = []

        def inspect(obj, i):
            result.append(obj)

        # this is just a basic test to get coverage..
        self.handler.progress_loop(inspect, range(5), NullProgress)
        self.assertEqual(result, list(range(5)))

    def test_make_object(self):

        # basic test
        obj = self.handler.make_object()
        self.assertIsNotNone(obj)

        # make sure attr is set
        obj = self.handler.make_object(answer=42)
        self.assertEqual(obj.answer, 42)

    def test_make_uuid(self):
        uuid = self.handler.make_uuid()
        self.assertIsInstance(uuid, str)
        self.assertEqual(len(uuid), 32)

    def test_get_session(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)

        # giving an unrelated object raises error
        person = Object()
        self.assertRaises(orm.exc.UnmappedInstanceError,
                          self.handler.get_session, person)

        # a related object still may not be in a session
        person = model.Person()
        result = self.handler.get_session(person)
        self.assertIsNone(result)

        # okay then let's add to session, then should work
        session.add(person)
        result = self.handler.get_session(person)
        self.assertIs(result, session)

        session.rollback()
        session.close()

    def test_make_session(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        
        # default behavior should "work" albeit with no engine bound,
        # and no continuum user set
        session = self.handler.make_session()
        self.assertIsNotNone(session)
        self.assertIsNone(session.bind)
        self.assertIsNone(session.continuum_user)

        # okay then let's create one with engine bound, and add a user
        session = self.handler.make_session(bind=engine)
        user = model.User(username='ferdinand')
        session.add(user)
        session.commit()

        # now we can make a session with that user bound
        session = self.handler.make_session(bind=engine, user='ferdinand')
        self.assertEqual(session.continuum_user.username, 'ferdinand')

        # okay add another user, configure it as default, then confirm
        user = model.User(username='beaufort')        
        session.add(user)
        session.commit()
        self.config.setdefault('rattail', 'runas.default', 'beaufort')
        session = self.handler.make_session(bind=engine)
        self.assertEqual(session.continuum_user.username, 'beaufort')

    def test_cache_model(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)

        store001 = model.Store(id='001')
        session.add(store001)
        store002 = model.Store(id='002')
        session.add(store002)
        session.commit()

        # just do a basic cache to prove the concept
        stores = self.handler.cache_model(session, model.Store, key='id')
        self.assertEqual(len(stores), 2)
        self.assertIn('001', stores)
        self.assertIn('002', stores)
        self.assertIs(stores['001'], store001)
        self.assertIs(stores['002'], store002)

    def test_make_temp_dir(self):

        # things work with no args
        path = self.handler.make_temp_dir()
        self.assertTrue(os.path.exists(path))
        os.rmdir(path)

        # we can specify an alternate parent dir (in this case also temp)
        parent = self.handler.make_temp_dir()
        child = self.handler.make_temp_dir(dir=parent)
        self.assertTrue(os.path.exists(child))
        self.assertEqual(os.path.dirname(child), parent)
        os.rmdir(child)
        os.rmdir(parent)

        # also can configure the workdir, to be used as (indirect) parent
        workdir = self.handler.make_temp_dir()
        self.config.setdefault('rattail', 'workdir', workdir)
        child = self.handler.make_temp_dir()
        parent = os.path.dirname(child)
        self.assertEqual(os.path.dirname(parent), workdir)
        os.rmdir(child)
        os.rmdir(parent)
        os.rmdir(workdir)

    def test_make_temp_file(self):

        # things work with no args
        path = self.handler.make_temp_file()
        self.assertTrue(os.path.exists(path))
        os.remove(path)

        # we can specify an alternate parent dir (in this case also temp)
        parent = self.handler.make_temp_dir()
        path = self.handler.make_temp_file(dir=parent)
        self.assertTrue(os.path.exists(path))
        self.assertEqual(os.path.dirname(path), parent)
        os.remove(path)
        os.rmdir(parent)

        # also can configure the workdir, to be used as (indirect) parent
        workdir = self.handler.make_temp_dir()
        self.config.setdefault('rattail', 'workdir', workdir)
        path = self.handler.make_temp_file()
        self.assertTrue(os.path.exists(path))
        parent = os.path.dirname(path)
        self.assertEqual(os.path.dirname(parent), workdir)
        os.remove(path)
        os.rmdir(parent)
        os.rmdir(workdir)

    def normalize_phone_number(self):

        # pre-normalized value is unchanged
        number = '8885551234'
        result = self.handler.normalize_phone_number(number)
        self.assertEqual(result, number)

        # now a basic real-world example
        number = '(888) 555-1234'
        result = self.handler.normalize_phone_number(number)
        self.assertEqual(result, '8885551234')

        # and another for good measure
        number = '888.555.1234'
        result = self.handler.normalize_phone_number(number)
        self.assertEqual(result, '8885551234')

    def test_phone_number_is_invalid(self):
        
        # basic real-world example
        self.assertIsNone(self.handler.phone_number_is_invalid(
            '(888) 555-1234'))

        # and another for good measure
        self.assertIsNone(self.handler.phone_number_is_invalid(
            '888.555.1234'))

        # 10 digits are required, so 9 or 11 digits should fail
        self.assertEqual(self.handler.phone_number_is_invalid('123456789'),
                         "Phone number must have 10 digits")
        self.assertEqual(self.handler.phone_number_is_invalid('12345678901'),
                         "Phone number must have 10 digits")

    def test_format_phone_number(self):
        
        # basic real-world example
        result = self.handler.format_phone_number('8885551234')
        self.assertEqual(result, '(888) 555-1234')

        # garbage in garbage out
        result = self.handler.format_phone_number('garbage')
        self.assertEqual(result, 'garbage')

    def test_make_gpc(self):

        # basic real-world example
        result = self.handler.make_gpc('074305001321')
        self.assertIsInstance(result, GPC)
        self.assertEqual(str(result), '00074305001321')

        # and let it calculate check digit
        result = self.handler.make_gpc('7430500132', calc_check_digit='upc')
        self.assertIsInstance(result, GPC)
        self.assertEqual(str(result), '00074305001321')

    def test_render_gpc(self):

        # basic real-world example
        gpc = GPC('00074305001321')
        result = self.handler.render_gpc(gpc)
        self.assertEqual(result, '0007430500132-1')

    def test_render_currency(self):
        
        # basic decimal example
        value = decimal.Decimal('42.00')
        self.assertEqual(self.handler.render_currency(value), '$42.00')

        # basic float example
        value = 42.00
        self.assertEqual(self.handler.render_currency(value), '$42.00')

        # decimal places will be rounded
        value = decimal.Decimal('42.12345')
        self.assertEqual(self.handler.render_currency(value), '$42.12')

        # but we can declare the scale
        value = decimal.Decimal('42.12345')
        self.assertEqual(self.handler.render_currency(value, scale=4), '$42.1234')

        # negative numbers get parens
        value = decimal.Decimal('-42.42')
        self.assertEqual(self.handler.render_currency(value), '($42.42)')

    def test_render_quantity(self):

        # integer decimals become integers
        value = decimal.Decimal('1.000')
        self.assertEqual(self.handler.render_quantity(value), '1')

        # but decimal places are preserved
        value = decimal.Decimal('1.234')
        self.assertEqual(self.handler.render_quantity(value), '1.234')

    def test_render_cases_units(self):
        
        # basic examples, note the singular noun
        self.assertEqual(self.handler.render_cases_units(1, None), '1 case')
        self.assertEqual(self.handler.render_cases_units(None, 1), '1 unit')

        # mix it up a bit
        self.assertEqual(self.handler.render_cases_units(3, 2), '3 cases + 2 units')

        # also note that zero is not hidden
        self.assertEqual(self.handler.render_cases_units(3, 0), '3 cases + 0 units')

    def test_render_date(self):

        # basic example
        date = datetime.date(2021, 12, 31)
        self.assertEqual(self.handler.render_date(date), '2021-12-31')

    def test_render_datetime(self):

        # basic example
        dt = datetime.datetime(2021, 12, 31, 8, 30)
        self.assertEqual(self.handler.render_datetime(dt), '2021-12-31 08:30:00 AM')

    @patch('rattail.app.send_email')
    def test_send_email(self, send_email):
        
        # just make sure underlying function is invoked..
        self.handler.send_email('test')
        send_email.assert_called()


class FooBarAutocompleter(Autocompleter):
    autocompleter_key = 'foobars'


class FooBarBatchHandler(BatchHandler):
    pass


class FooBarBounceHandler(BounceHandler):
    pass


class FromFooToBar(ImportHandler):
    host_key = 'rattail'
    local_key = 'rattail'
