# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This is a sample Hello World API implemented using Google Cloud Endpoints."""

import endpoints
import functools
import logging
import urlparse

from google.appengine.ext import ndb
from google.appengine.api import users

from endpoints_proto_datastore import ndb as endpoints_model

from protorpc import message_types
from protorpc import messages
from protorpc import remote

# print 'file', endpoints.__file__

class Greeting(endpoints_model.EndpointsModel):
    message = ndb.StringProperty()

    # Define IdSet() and id() to require a string id.
    def IdSet(self, value):
        if not isinstance(value, basestring):
            raise TypeError('ID must be a string.')
        self.UpdateFromKey(ndb.Key(type(self), value))

    @endpoints_model.EndpointsAliasProperty(setter=IdSet, required=True)
    def id(self):
      if self.key is not None:
        return self.key.string_id()


####################################################################
# TEMPORARY
class Result(messages.Message):
    message = messages.StringField(1)


STORED_GREETINGS = [
    Greeting(message='hello world!', id='banana'),
    Greeting(message='goodbye world!', id='orange'),
]
####################################################################


####################################################################
# The Greeting API
####################################################################

WEB_CLIENT_ID = '294885104230-a8i6fnv7pcgsg0chm0r8vtihcftkcurj.apps.googleusercontent.com'
PS_CLIENT_ID = '294885104230-ue8r3k8on02m0kjsu8vh5ulnke7imnrf.apps.googleusercontent.com'
ADMIN_USERS = ['soltesz@google.com', 'stephen.soltesz@gmail.com']

ALLOWED_CLIENT_IDS = [
    WEB_CLIENT_ID, PS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID]


def authorized(f):
    @functools.wraps(f)
    def admin_check(*args, **kwargs):
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.ForbiddenException('Users must be authenticated!')
        if user.email() not in ADMIN_USERS:
            raise endpoints.UnauthorizedException(
                '%s is not an admin user.' % user)
        return f(*args, **kwargs)
    return admin_check


@endpoints.api(name='greeting', version='v1',
               allowed_client_ids=ALLOWED_CLIENT_IDS)
class GreetingApi(remote.Service):

    @Greeting.query_method(query_fields=('limit', 'order', 'pageToken'),
                           path='greetings2')
    @authorized
    def list(self, query):
        logging.debug('query: %s', query)
        return query

    @Greeting.method(path='greetings2/{id}', http_method='GET')
    @authorized
    def get(self, greeting):
        if not greeting.from_datastore:
            raise endpoints.NotFoundException(
                    'Greeting not found: "%s"' % greeting.key.id())
        return greeting

    @Greeting.method(path='greetings2', http_method='POST')
    @authorized
    def create(self, greeting):
        greeting.put()
        return greeting

    @Greeting.method(
        response_fields=(), path='greetings2/{id}', http_method='POST')
    @authorized
    def delete(self, greeting):
        if not greeting.from_datastore:
            raise endpoints.NotFoundException(
                    'Greeting not found: "%s"' % greeting.key.id())
        greeting.key.delete()
        return greeting


    # TEMPORARY
    @endpoints.method(
        message_types.VoidMessage, Result, path='setup2', http_method='GET')
    @authorized
    def setup2(self, unused_request):
        for greeting in STORED_GREETINGS:
            greeting.put()
        return Result(message='okay')

    @endpoints.method(
        message_types.VoidMessage, Result,
        path='authcheck', http_method='GET')
    def authcheck(self, unused_request):
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.ForbiddenException(
                'Users must be authenticated!')
        msg = user.email()
        if users.is_current_user_admin():
            msg += ' is ADMIN'
        else:
            msg += ' is not admin'
        logging.info('authcheck: %s', msg)
        return Result(message=msg)



# The api server.
api = endpoints.api_server([GreetingApi])
