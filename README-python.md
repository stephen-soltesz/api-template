# api-template

## PYTHON

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

6. Regenerate the apitools library

    gen_client --discovery_url=https://dash-test-1.appspot.com/_ah/api/discovery/v1/apis/greeting/v1/rest \
        --overwrite --outdir=greeting --root_package=. client

### Linux

When using apitools

    sudo pip install --upgrade pip
    sudo pip install google-apitools python-gflags google-apputils


### Mac OS X

    sudo easy_install --upgrade google-api-python-client
    sudo chmod o+r /Library/Python/2.7/site-packages/httplib2-0.9.2-py2.7.egg/httplib2/cacerts.txt


    Traceback (most recent call last):
      File "./client.py", line 62, in <module>
        main(sys.argv)
      File "./client.py", line 39, in main
        credentials = tools.run_flow(flow, storage, flags)
      File "build/bdist.macosx-10.11-intel/egg/oauth2client/_helpers.py", line 133, in positional_wrapper
      File "build/bdist.macosx-10.11-intel/egg/oauth2client/tools.py", line 242, in run_flow
      File "build/bdist.macosx-10.11-intel/egg/oauth2client/_helpers.py", line 133, in positional_wrapper
      File "build/bdist.macosx-10.11-intel/egg/oauth2client/client.py", line 2047, in step2_exchange
        
      File "build/bdist.macosx-10.11-intel/egg/oauth2client/transport.py", line 282, in request
      File "/Library/Python/2.7/site-packages/httplib2-0.9.2-py2.7.egg/httplib2/__init__.py", line 1610, in request
        (response, content) = self._request(conn, authority, uri, request_uri, method, body, headers, redirections, cachekey)
      File "/Library/Python/2.7/site-packages/httplib2-0.9.2-py2.7.egg/httplib2/__init__.py", line 1352, in _request
        (response, content) = self._conn_request(conn, request_uri, method, body, headers)
      File "/Library/Python/2.7/site-packages/httplib2-0.9.2-py2.7.egg/httplib2/__init__.py", line 1273, in _conn_request
        conn.connect()
      File "/Library/Python/2.7/site-packages/httplib2-0.9.2-py2.7.egg/httplib2/__init__.py", line 1037, in connect
        self.disable_ssl_certificate_validation, self.ca_certs)
      File "/Library/Python/2.7/site-packages/httplib2-0.9.2-py2.7.egg/httplib2/__init__.py", line 81, in _ssl_wrap_socket
        cert_reqs=cert_reqs, ca_certs=ca_certs)
      File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/ssl.py", line 911, in wrap_socket
        ciphers=ciphers)
      File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/ssl.py", line 520, in __init__
        self._context.load_verify_locations(ca_certs)
    IOError: [Errno 13] Permission denied

## GOLANG

1. DO NOT INSTALL THE Go AppEngine SDK

   <strike>https://cloud.google.com/appengine/docs/go/download</strike>

  Install the full AppEngine SDK, and install the `app-engine-go` component.

        gcloud components install app-engine-go

  Then make the `goapp` command executable (as of google-cloud-sdk-135.0.0):

        chmod 755 /usr/local/google-cloud-sdk/platform/google_appengine/goapp 
        export PATH=$PATH:/usr/local/google-cloud-sdk/platform/google_appengine/

1. Setup and serve app

        GOPATH=$PWD
        goapp get hello
        goapp serve src/hello/app.yaml

  If all packages are not available, you may see errors from `goapp serve` like these:

        2016/11/23 04:11:20 Can't find package "golang.org/x/net/context" in $GOPATH: cannot find package "golang.org/x/net/context" in any of:
          /usr/local/google-cloud-sdk/platform/google_appengine/goroot/src/golang.org/x/net/context (from $GOROOT)
          /vagrant/src/golang.org/x/net/context (from $GOPATH)

  If `goapp get` reports errors like these, they may be safely ignored:

        go install appengine_internal/github.com/golang/protobuf/proto: open /usr/local/google-cloud-sdk/platform/google_appengine/goroot/pkg/linux_amd64_appengine/appengine_internal/github.com/golang/protobuf/proto.a: permission denied
        go install runtime/cgo: open /usr/local/google-cloud-sdk/platform/google_appengine/goroot/pkg/linux_amd64_appengine/runtime/cgo.a: permission denied

1. Check REST document.

        DISCOVERY=http://localhost:8080/_ah/api/discovery/v1/apis/hosts/v1/rest
        curl $DISCOVERY

1. Deploy app

        goapp deploy src/hello/app.yaml
 
  And, check the discovery doc again.

        DISCOVERY=https://dash-test-1.appspot.com/_ah/api/discovery/v1/apis/hosts/v1/rest
        curl $DISCOVERY

1. Install / update apitools (and dependencies)

        $ sudo pip install --upgrade google-apputils google-apitools

1. Generate the python client library.

        $ gen_client --discovery_url=$DISCOVERY \
	    --overwrite --outdir=hosts_py --root_package=. client

1. Add a host record to the api

        $ python -m hosts_py.hosts_v1 add --IPAddress 127.0.0.1

   List all host records in the api

        $ python -m hosts_py.hosts_v1 list
