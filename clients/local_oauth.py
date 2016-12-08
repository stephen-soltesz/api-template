"""Simple utility for loading OAuth2 credentials."""

import argparse
import httplib2
import oauth2client
from oauth2client import tools
import os


# Allow the service to view user's email address for authorization.
SCOPE = 'https://www.googleapis.com/auth/userinfo.email'
USER_AGENT = 'sample-cmdline-tool/1.0'

OAUTH_DISPLAY_NAME = 'Sample API Commandline Tool'

CLIENT_ID = '294885104230-ue8r3k8on02m0kjsu8vh5ulnke7imnrf.apps.googleusercontent.com'
CLIENT_SECRET = 'g1bLl_oz-2bGqI12Blvr3tLU'

# Save to a common location for re-use.
CREDENTIALS_FILE = os.path.join(os.environ['HOME'], '.api_credentials')

# When credentialas are not yet saved, or otherwise invalid, we will need to
# run an interactive "OAuth2 authentication workflow".
OAUTH2_FLOW = oauth2client.client.OAuth2WebServerFlow(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scope=SCOPE,
    user_agent=USER_AGENT,
    oauth_displayname=OAUTH_DISPLAY_NAME, prompt='consent')


def GetOAuth2OptionsParser():
    # Parse command line flags used by the oauth2client library.
    return argparse.ArgumentParser(
        description='Auth sample',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[tools.argparser])

def GetCredentials(options):
    # Acquire and store oauth token.
    storage = oauth2client.file.Storage(CREDENTIALS_FILE)
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(OAUTH2_FLOW, storage, options)

    http = credentials.authorize(httplib2.Http())
    credentials.refresh(http)

    return credentials, http

def GetDiscoveryURL(hostname, api, version, https=True):
    # NOTE: the default discovery url points to googleapis.com, so we must
    # construct one that points to our appengine API.
    protocol = 'https' if https else 'http'
    return '{}://{}/_ah/api/discovery/v1/apis/{}/{}/rest'.format(
        protocol, hostname, api, version)
