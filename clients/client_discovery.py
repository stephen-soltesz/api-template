#!/usr/bin/python


import argparse
import logging
import pprint
import os
import sys

from apiclient import discovery
import httplib2
import oauth2client
from oauth2client import tools

import local_oauth


def main(argv):
    parser = local_oauth.GetOAuth2OptionsParser()

    parser.add_argument(
        '--hostname', default='dash-test-1.appspot.com',
        help='The AppEngine app FQDN. This should provide the base of the API.')
    parser.add_argument(
        '--api', default='hosts', help='The API name.')
    parser.add_argument(
        '--version', default='v1', help='The API version.')
    parser.add_argument(
        '--insecure', dest='secure', default=True, action="store_false",
        help='Whether to disable HTTPS.')

    options = parser.parse_args(argv[1:])

    credentials, http = local_oauth.GetCredentials(options)

    discovery_url = local_oauth.GetDiscoveryURL(
        options.hostname, options.api, options.version, options.secure)
    logging.info(discovery_url)

    # Build a service object for interacting with the API.
    service = discovery.build(
        options.api, options.version, discoveryServiceUrl=discovery_url,
        http=http, cache_discovery=False)
    # credentials=credentials

    # Setup datastore with sample data.
    response = service.setup().execute()
    pprint.pprint(response)

    # Create.
    response = service.create(body={'id': '64.123.0.65'}).execute()
    pprint.pprint(response)

    # List all.
    response = service.list().execute()
    pprint.pprint(response)

    # Delete the new one.
    response = service.delete(body={}, id='64.123.0.65').execute()
    pprint.pprint(response)

    # List them all again.
    response = service.list().execute()
    pprint.pprint(response)


if __name__ == '__main__':
    main(sys.argv)
