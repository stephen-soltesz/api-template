#!/usr/bin/python


import logging
import sys

from apiclient import discovery
import httplib2
import oauth2client
from oauth2client import tools

import hosts_go as hosts
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
    print client.api.Setup(hosts.HostsSetupRequest())

    # Create.
    print client.api.Create(hosts.Host(id='64.123.0.22'))

    # List all.
    resp = client.api.List(hosts.HostsListRequest())
    for i, host in enumerate(resp.items):
        print 'list', i, host

    # Delete the new one.
    print client.api.Delete(hosts.Host(id='64.123.0.22'))

    # List them all again.
    resp = client.api.List(hosts.HostsListRequest())
    for i, host in enumerate(resp.items):
        print 'list', i, host


if __name__ == '__main__':
    main(sys.argv)
