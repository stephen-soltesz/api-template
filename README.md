# api-template


1. Install AppEngine Python SDK

    TODO: add link to steps.

2. Install `endpoints_proto_datastore` module.

    ./setup.sh

3. Run `dev_appserver.py`

    dev_appserver.py .

4. Run query for discovery document

    curl https://dash-test-1.appspot.com/_ah/api/discovery/v1/apis/greeting/v1/rest

5. Run authenticated client request

    ./client.py
