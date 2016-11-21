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


logging.basicConfig(level=logging.DEBUG)

SCOPE = 'https://www.googleapis.com/auth/userinfo.email'
USER_AGENT = 'sample-cmdline-tool/1.0'
OAUTH_DISPLAY_NAME = 'Sample API Commandline Tool'
CLIENT_ID = '294885104230-a8i6fnv7pcgsg0chm0r8vtihcftkcurj.apps.googleusercontent.com'
CLIENT_SECRET = 'pK_9Txg8jRP9ll_ttYxwxlzk'
CLIENT_ID = '294885104230-ue8r3k8on02m0kjsu8vh5ulnke7imnrf.apps.googleusercontent.com'
CLIENT_SECRET = 'g1bLl_oz-2bGqI12Blvr3tLU'

CREDENTIALS_FILE = os.path.join(os.environ['HOME'], '.api_credentials')

OAUTH2_FLOW = oauth2client.client.OAuth2WebServerFlow(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scope=SCOPE,
    user_agent=USER_AGENT,
    oauth_displayname=OAUTH_DISPLAY_NAME, prompt='consent')

def main(argv):
    # Parse command line flags used by the oauth2client library.
    parser = argparse.ArgumentParser(
        description='Auth sample',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[tools.argparser])
    parser.add_argument('--hostname', default='dash-test-1.appspot.com',
        help='FQDN for the appengine app.')
    parser.add_argument('--api', default='greeting', help='The API name.')
    parser.add_argument('--version', default='v1', help='The API version.')

    flags = parser.parse_args(argv[1:])

    # Acquire and store oauth token.
    storage = oauth2client.file.Storage(CREDENTIALS_FILE)
    credentials = storage.get()

    if credentials is None or credentials.invalid:
      credentials = tools.run_flow(OAUTH2_FLOW, storage, flags)
    http = credentials.authorize(httplib2.Http())
    credentials.refresh(http)

    # Build a service object for interacting with the API.
    # NOTE: the default discovery url points to googleapis.com, so we must
    # construct one that points to the appengine app api.
    discovery_url = 'https://{0}/_ah/api/discovery/v1/apis/{1}/{2}/rest'.format(
        flags.hostname, flags.api, flags.version)
    logging.info(discovery_url)

    service = discovery.build(
        flags.api, flags.version, discoveryServiceUrl=discovery_url,
        http=http, cache_discovery=False)

    # Setup datastore.
    response = service.setup2().execute()
    pprint.pprint(response)

    response = service.authcheck().execute()
    pprint.pprint(response)

    response = service.create(body={
        'id':'clientcheck', 'message':'this is another test'}).execute()
    pprint.pprint(response)

    response = service.list().execute()
    pprint.pprint(response)

    response = service.delete(body={}, id='clientcheck').execute()
    pprint.pprint(response)

    response = service.list().execute()
    pprint.pprint(response)


if __name__ == '__main__':
    main(sys.argv)
