#!/usr/bin/python


import argparse
import pprint
import sys

from apiclient import discovery
import httplib2
import oauth2client
from oauth2client import tools


SCOPE = 'https://www.googleapis.com/auth/userinfo.email'
USER_AGENT = 'sample-cmdline-tool/1.0'
OAUTH_DISPLAY_NAME = 'Sample API Commandline Tool'
CLIENT_ID = '294885104230-a8i6fnv7pcgsg0chm0r8vtihcftkcurj.apps.googleusercontent.com'
CLIENT_SECRET = 'pK_9Txg8jRP9ll_ttYxwxlzk'

def main(argv):
  # Parse command line flags used by the oauth2client library.
  parser = argparse.ArgumentParser(
      description='Auth sample',
      formatter_class=argparse.RawDescriptionHelpFormatter,
      parents=[tools.argparser])
  flags = parser.parse_args(argv[1:])

  # Acquire and store oauth token.
  storage = oauth2client.file.Storage('guestbook.dat')
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    flow = oauth2client.client.OAuth2WebServerFlow(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope=SCOPE,
        user_agent=USER_AGENT,
        oauth_displayname=OAUTH_DISPLAY_NAME)
    credentials = tools.run_flow(flow, storage, flags)
  http = httplib2.Http()
  http = credentials.authorize(http)
  credentials.refresh(http)

  # Build a service object for interacting with the API.
  # api_root = 'http://192.168.0.116:8080/_ah/api'
  api_root = 'https://dash-test-1.appspot.com/_ah/api'
  api = 'greeting'
  version = 'v1'
  discovery_url = '%s/discovery/v1/apis/%s/%s/rest' % (api_root, api, version)
  print discovery_url
  service = discovery.build(
      api, version, discoveryServiceUrl=discovery_url,
      http=http, cache_discovery=False)

  response = service.authcheck().execute()
  pprint.pprint(response)
  response = service.list().execute()
  pprint.pprint(response)


if __name__ == '__main__':
    main(sys.argv)
