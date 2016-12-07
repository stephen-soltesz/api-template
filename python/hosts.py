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
"""This is a sample Hosts API implemented using Google Cloud Endpoints."""


import datetime
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


class Host(endpoints_model.EndpointsModel):
    """A Host Entity represents a machine record."""
    # Reset default from messages.StringField so clients see a date-time format.
    # created = endpoints_model.EndpointsDateTimeProperty() # ndb.DateTimeProperty()
    created = ndb.DateTimeProperty()

    # Should help convert DateTimeProperty to a correct date-time format, however,
    # there appears to be some bug that still prevents this:
    # https://github.com/GoogleCloudPlatform/endpoints-proto-datastore/issues/83
    # _custom_property_to_proto = {
    #     # fails.
    #     endpoints_model.EndpointsDateTimeProperty: message_types.DateTimeField
    #     # fails.
    #     ndb.DateTimeProperty: message_types.DateTimeField
    #     # works, but is the wrong type of course for a datetime object.
    #     ndb.DateTimeProperty: messages.BytesField
    # }

    # Define IdSet() and id() to require a string id.
    def IdSet(self, value):
        if not isinstance(value, basestring):
            raise TypeError('ID must be a string.')
        self.UpdateFromKey(ndb.Key(type(self), value))

    @endpoints_model.EndpointsAliasProperty(setter=IdSet, required=True)
    def id(self):
      if self.key is not None:
        return self.key.string_id()

    @property
    def ip_address(self):
        return self.id


####################################################################
# TEMPORARY
STORED_HOSTS = [
    Host(id='192.168.1.1'),
    Host(id='127.0.0.1'),
    Host(id='10.3.4.22'),
]
####################################################################


####################################################################
# The Hosts API
####################################################################

PS_CLIENT_ID = '294885104230-ue8r3k8on02m0kjsu8vh5ulnke7imnrf.apps.googleusercontent.com'
ADMIN_USERS = ['soltesz@google.com', 'stephen.soltesz@gmail.com']

ALLOWED_CLIENT_IDS = [PS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID]


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


@endpoints.api(name='hosts', version='v1',
               allowed_client_ids=ALLOWED_CLIENT_IDS,
               auth_level=endpoints.AUTH_LEVEL.REQUIRED,
               description='Hosts API (Python)')
class HostsApi(remote.Service):

    # TODO: enable standard query_fields=('limit', 'order', 'pageToken').
    @Host.query_method(path='hosts', query_fields=())
    @authorized
    def list(self, query):
        logging.debug('query: %s', query)
        return query

    @Host.method(path='hosts/{id}', http_method='GET')
    @authorized
    def get(self, host):
        if not host.from_datastore:
            raise endpoints.NotFoundException(
                    'Host not found: "%s"' % host.key.id())
        return host

    @Host.method(path='hosts')
    @authorized
    def create(self, host):
        host.created = datetime.datetime.now()
        host.put()
        return host

    @Host.method(path='hosts/{id}')
    @authorized
    def delete(self, host):
        if not host.from_datastore:
            raise endpoints.NotFoundException(
                    'Host not found: "%s"' % host.key.id())
        host.key.delete()
        return host

    # TEMPORARY
    @Host.method(
        request_message=message_types.VoidMessage, path='setup',
        http_method='GET')
    @authorized
    def setup(self, unused_request):
        for host in STORED_HOSTS:
            host.created = datetime.datetime.now()
            host.put()
        return host


# API server.
api = endpoints.api_server([HostsApi])
