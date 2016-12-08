# Python api-template

1. Install Google Cloud SDK (which includes AppEngine Python SDK)

        ./setup.sh

2. Install `endpoints_proto_datastore` module.

        cd python
        ./setup_python.sh

3. Run `dev_appserver.py`

        dev_appserver.py .

4. Check that the REST discovery document is served by the local dev server.

        DISCOVERY=http://localhost:8080/_ah/api/discovery/v1/apis/hosts/v1/rest
        curl $DISCOVERY

5. Run query for discovery document

        DISCOVERY=https://dash-test-1.appspot.com/_ah/api/discovery/v1/apis/hosts/v1/rest
        curl $DISCOVERY

6. Run an authenticated client request

        cd clients
	    ./client_discovery.py

7. Generate the apitools, python client library, and install it locally.

        $ DISCOVERY=https://dash-test-1.appspot.com/_ah/api/discovery/v1/apis/hosts/v1/rest
        $ gen_client --discovery_url=$DISCOVERY \
            --overwrite --outdir=hosts --root_package=. pip_package
	    $ cd hosts
	    $ sudo python setup.py install

8. Run an authenticated apitools client request.

        cd clients
	    ./client_apitools.py

## Linux

When using apitools

        sudo pip install --upgrade pip
        sudo pip install google-apitools python-gflags google-apputils

## Mac OS X

If you encounter stack traces like those below, there may be a problem with
permissions on the httplib2 cacerts.txt file.

        sudo easy_install --upgrade google-api-python-client
        sudo chmod o+r /Library/Python/2.7/site-packages/httplib2-0.9.2-py2.7.egg/httplib2/cacerts.txt

Example Traceback:

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
