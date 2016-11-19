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

class GreetingEP(endpoints_model.EndpointsModel):
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


class GreetingCollectionEP(endpoints_model.EndpointsModel):
    items = ndb.StructuredProperty(GreetingEP, repeated=True)



####################################################################
# TEMPORARY
class Result(messages.Message):
    message = messages.StringField(1)


class Greeting(messages.Message):
    """Greeting that stores a message."""
    message = messages.StringField(1)
    id = messages.StringField(2)


class GreetingCollection(messages.Message):
    """Collection of Greetings."""
    items = messages.MessageField(Greeting, 1, repeated=True)


STORED_GREETINGS = GreetingCollection(items=[
    Greeting(message='hello world!', id='banana'),
    Greeting(message='goodbye world!', id='orange'),
])
####################################################################


####################################################################
# The Greeting API
####################################################################

WEB_CLIENT_ID = '294885104230-a8i6fnv7pcgsg0chm0r8vtihcftkcurj.apps.googleusercontent.com'
ADMIN_USERS = ['soltesz@google.com', 'stephen.soltesz@gmail.com']

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
               allowed_client_ids=[
                   WEB_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID])
class GreetingApi(remote.Service):

    @GreetingEP.query_method(query_fields=('limit', 'order', 'pageToken'),
                             path='greetings2')
    @authorized
    def list(self, query):
        logging.debug('query: %s', query)
        return query

    @GreetingEP.method(
        path='greetings2/{id}', http_method='GET')
    @authorized
    def get(self, greeting):
        if not greeting.from_datastore:
            raise endpoints.NotFoundException(
                    'Greeting not found: "%s"' % greeting.key.id())
        return greeting

    @GreetingEP.method(path='greetings2', http_method='POST')
    @authorized
    def create(self, greeting):
        greeting.put()
        return greeting

    @GreetingEP.method(
        response_fields=(),
        path='greetings2/{id}', http_method='POST')
    @authorized
    def delete(self, greeting):
        greeting.key.delete()
        return greeting


    # TEMPORARY
    @endpoints.method(
        message_types.VoidMessage, Result,
        path='setup2', http_method='GET')
    @authorized
    def setup2(self, unused_request):
        for greeting in STORED_GREETINGS.items:
            g = GreetingEP(message=greeting.message)
            g.key = ndb.Key(GreetingEP, greeting.id)
            g.put()
        return Result(message='okay')

    @endpoints.method(
        message_types.VoidMessage, Result,
        path='authcheck', http_method='GET')
    def authcheck(self, unused_request):
        # print dir(self)
        # print unused_request
        user = endpoints.get_current_user()
        # request_path = urlparse.urlsplit(self.request.url).path
        # if request_path.startswith('/_ah/api/'):
        #     logging.info('path: %s', request_path)

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


    # [START multiply]
    # This ResourceContainer is similar to the one used for get_greeting, but
    # this one also contains a request body in the form of a Greeting message.
#    MULTIPLY_RESOURCE = endpoints.ResourceContainer(
#        Greeting,
#        times=messages.IntegerField(2, variant=messages.Variant.INT32,
#                                    required=True))
#
#    @endpoints.method(
#        # This method accepts a request body containing a Greeting message
#        # and a URL parameter specifying how many times to multiply the
#        # message.
#        MULTIPLY_RESOURCE,
#        # This method returns a Greeting message.
#        Greeting,
#        path='greetings/multiply/{times}',
#        http_method='POST',
#        name='greetings.multiply')
#    def multiply_greeting(self, request):
#        return Greeting(message=request.message * request.times)
#    # [END multiply]


# [START auth_config]
WEB_CLIENT_ID = '294885104230-a8i6fnv7pcgsg0chm0r8vtihcftkcurj.apps.googleusercontent.com'
# WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID
ALLOWED_CLIENT_IDS = [
    WEB_CLIENT_ID, ANDROID_CLIENT_ID, IOS_CLIENT_ID,
    endpoints.API_EXPLORER_CLIENT_ID]
# [END auth_config]


# [START authed_greeting_api]
#@endpoints.api(
#    name='authed_greeting',
#    version='v1',
#    # Only allowed configured Client IDs to access this API.
#    allowed_client_ids=ALLOWED_CLIENT_IDS,
#    # Only allow auth tokens with the given audience to access this API.
#    audiences=[ANDROID_AUDIENCE],
#    # Require auth tokens to have the following scopes to access this API.
#    scopes=[endpoints.EMAIL_SCOPE])
#class AuthedGreetingApi(remote.Service):
#
#    @endpoints.method(
#        message_types.VoidMessage,
#        Greeting,
#        path='greet',
#        http_method='POST',
#        name='greet')
#    def greet(self, request):
#        user = endpoints.get_current_user()
#        user_name = user.email() if user else 'Anonymous'
#        return Greeting(message='Hello, {}'.format(user_name))
## [END authed_greeting_api]


# [START api_server]
# api = endpoints.api_server([GreetingApi, AuthedGreetingApi])
api = endpoints.api_server([GreetingApi])
# [END api_server]
