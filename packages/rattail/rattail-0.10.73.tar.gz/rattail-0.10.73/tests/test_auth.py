# -*- coding: utf-8; -*-

from __future__ import unicode_literals, absolute_import

from unittest import TestCase

import sqlalchemy as sa

from rattail import auth as mod
from rattail.config import make_config
from rattail.db import Session
from rattail.db.auth import (set_user_password, administrator_role, 
                             guest_role, authenticated_role)


class TestAuthHandler(TestCase):

    def setUp(self):
        self.config = self.make_config()
        self.handler = self.make_handler()

    def make_config(self):
        return make_config([], extend=False)

    def make_handler(self):
        return mod.AuthHandler(self.config)

    def test_authenticate_user(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)

        # should fail if there are no users!
        result = self.handler.authenticate_user(session, 'myuser', 'mypass')
        self.assertIsNone(result)

        # okay now add a user and make sure it does work
        myuser = model.User(username='myuser')
        set_user_password(myuser, 'mypass')
        session.add(myuser)
        result = self.handler.authenticate_user(session, 'myuser', 'mypass')
        self.assertIsInstance(result, model.User)
        self.assertEqual(result.username, 'myuser')

    def test_generate_preferred_username(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)

        # default is just hard-coded
        result = self.handler.generate_preferred_username(session)
        self.assertEqual(result, 'newuser')

        # but if we specify a person then will return 'first.last'
        person = model.Person(first_name='Fred', last_name='Flintstone')
        result = self.handler.generate_preferred_username(session, person=person)
        self.assertEqual(result, 'fred.flintstone')

    def test_generate_unique_username(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)

        # default is just hard-coded
        result = self.handler.generate_unique_username(session)
        self.assertEqual(result, 'newuser')

        # unless we make a user with that name, then it must use a counter
        user = model.User(username='newuser')
        session.add(user)
        result = self.handler.generate_unique_username(session)
        self.assertEqual(result, 'newuser01')

        # if we specify a person then will return 'first.last'
        person = model.Person(first_name='Fred', last_name='Flintstone')
        result = self.handler.generate_unique_username(session, person=person)
        self.assertEqual(result, 'fred.flintstone')

        # unless username is taken, in which case it must use a counter
        user = model.User(username='fred.flintstone')
        session.add(user)
        person = model.Person(first_name='Fred', last_name='Flintstone')
        result = self.handler.generate_unique_username(session, person=person)
        self.assertEqual(result, 'fred.flintstone01')

    def test_make_user(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)

        # making a user with no info at all, gets hard-coded username
        user = self.handler.make_user()
        self.assertIsInstance(user, model.User)
        self.assertEqual(user.username, 'newuser')

        # or we can specify the username directly
        user = self.handler.make_user(username='foobar')
        self.assertIsInstance(user, model.User)
        self.assertEqual(user.username, 'foobar')

        # if we specify a person then username will be like 'first.last'
        person = model.Person(first_name='Fred', last_name='Flintstone')
        user = self.handler.make_user(session, person=person)
        self.assertEqual(user.username, 'fred.flintstone')

    def test_delete_user(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)
        
        # make a user, then delete - it should work
        user = model.User(username='foobar')
        session.add(user)
        session.commit()
        self.assertIn(user, session)
        self.handler.delete_user(user)
        session.commit()
        self.assertNotIn(user, session)

    def test_has_permission(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)

        # anonymous does not have any permission by default
        result = self.handler.has_permission(session, None, 'common.feedback')
        self.assertFalse(result)

        # make a role and user, but each should still not have permission
        role = model.Role(name='foobar')
        user = model.User(username='whatever')
        user.roles.append(role)
        session.add(user)
        result = self.handler.has_permission(session, role, 'common.feedback')
        self.assertFalse(result)
        result = self.handler.has_permission(session, user, 'common.feedback')
        self.assertFalse(result)
        
        # grant permission, then check again
        role.permissions.append('common.feedback')
        result = self.handler.has_permission(session, role, 'common.feedback')
        self.assertTrue(result)
        result = self.handler.has_permission(session, user, 'common.feedback')
        self.assertTrue(result)

    def test_get_permissions(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)

        # admin does not have any permissions by default
        admin = administrator_role(session)
        result = self.handler.get_permissions(session, admin)
        self.assertEqual(result, set())

        # we can grant perm to guest, and then all can inherit
        guest = guest_role(session)
        guest.permissions.append('common.feedback')
        result = self.handler.get_permissions(session, None)
        self.assertEqual(result, set(['common.feedback']))

        # make a user, make sure it gets same perms
        user = model.User(username='betty')
        session.add(user)
        result = self.handler.get_permissions(session, user)
        self.assertEqual(result, set(['common.feedback']))

        # but it has no perms if we exclude guest when checking
        result = self.handler.get_permissions(session, user, include_guest=False)
        self.assertEqual(result, set())

        # grant perms to authenticated, make sure that works
        authd = authenticated_role(session)
        authd.permissions.append('common.consume_batch_id')
        result = self.handler.get_permissions(session, user, include_guest=False)
        self.assertEqual(result, set(['common.consume_batch_id']))

        # and user still does not have perms if we exclude authenticated
        result = self.handler.get_permissions(session, user, include_guest=False,
                                              include_authenticated=False)
        self.assertEqual(result, set())

        # finally add user to new role, make sure all works
        role = model.Role(name='Site Admin')
        user.roles.append(role)
        role.permissions.append('common.change_app_theme')
        result = self.handler.get_permissions(session, user)
        self.assertEqual(result, set(['common.change_app_theme',
                                      'common.consume_batch_id', 
                                      'common.feedback']))

        # now let's set a node type and corresponding roles, grant some 
        # selective perms, then make sure all comes back okay
        self.config.setdefault('rattail', 'node_type', 'type1')
        type1_users = model.Role(name='Node Type 1 Users', node_type='type1')
        type2_users = model.Role(name='Node Type 2 Users', node_type='type2')
        user.roles.extend([type1_users, type2_users])
        type1_users.permissions.append('products.list')
        type2_users.permissions.append('customers.list')

        # our node is configured as type 1, so even though user belongs to
        # type2 role it should not inherit that permission on *this* node
        result = self.handler.get_permissions(session, user)
        self.assertEqual(result, set(['common.change_app_theme', 
                                      'common.consume_batch_id',
                                      'common.feedback',
                                      'products.list']))

    def test_grant_permission(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)
        
        # make a role, grant a perm, confirm
        role = model.Role(name='FooBar')
        self.assertEqual(role.permissions, [])
        self.handler.grant_permission(role, 'perm01')
        self.assertEqual(role.permissions, ['perm01'])

        # make sure it doesn't double-add
        self.handler.grant_permission(role, 'perm01')
        self.assertEqual(role.permissions, ['perm01'])

    def test_revoke_permission(self):
        engine = sa.create_engine('sqlite://')
        model = self.config.get_model()
        model.Base.metadata.create_all(bind=engine)
        session = Session(bind=engine)
        
        # make a role, grant perms, then revoke one and check
        role = model.Role(name='FooBar')
        role.permissions.extend(['perm01', 'perm02'])
        self.handler.revoke_permission(role, 'perm01')
        self.assertEqual(role.permissions, ['perm02'])
        
        # make sure it doesn't try to somehow double-revoke
        self.handler.revoke_permission(role, 'perm01')
        self.assertEqual(role.permissions, ['perm02'])
