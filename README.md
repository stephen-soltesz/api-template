# api-template

## golang

1. Download the Go AppEngine SDK

   https://cloud.google.com/appengine/docs/go/download

2. Deploy app

    goapp deploy src/hello/app.yaml

3. Check REST document.

    DISCOVERY=https://dash-test-1.appspot.com/_ah/api/discovery/v1/apis/hosts/v1/rest
    curl $DISCOVERY

4. Install / update apitools (and dependencies)

    $ sudo pip install --upgrade google-apputils google-apitools

5. Generate the python client library.

    $ gen_client --discovery_url=$DISCOVERY \
	    --overwrite --outdir=hosts_py --root_package=. client

6. Add a host record to the api

    $ python -m hosts_py.hosts_v1 add --IPAddress 127.0.0.1

   List all host records in the api

    $ python -m hosts_py.hosts_v1 list
