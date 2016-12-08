#!/usr/bin/python


import logging
import sys

from apiclient import discovery
import httplib2
import oauth2client
from oauth2client import tools

# Generated from the hosts API discovery document, installed via apitools.
from apitools.clients import hosts
import local_oauth


logging.basicConfig(level=logging.DEBUG)


def main(argv):
    parser = local_oauth.GetOAuth2OptionsParser()
    options = parser.parse_args(argv[1:])

    credentials, http = local_oauth.GetCredentials(options)

    # Setup service client with new credentials.
    # The discovery URL is baked into the generated HostsV1 class.
    client = hosts.HostsV1(credentials=credentials)

    # Setup datastore with sample data.
    print 'Setup\n', client.api.Setup(hosts.HostsSetupRequest())

    # Create.
    print 'Create\n', client.api.Create(hosts.Host(id='64.123.0.22'))

    # List all.
    print 'List\n'
    resp = client.api.List(hosts.HostsListRequest())
    for i, host in enumerate(resp.items):
        print '\tList', i, host

    # Delete the new one.
    print 'Delete\n', client.api.Delete(hosts.Host(id='64.123.0.22'))

    # List them all again.
    print 'List\n'
    resp = client.api.List(hosts.HostsListRequest())
    for i, host in enumerate(resp.items):
        print '\tList', i, host


if __name__ == '__main__':
    main(sys.argv)
