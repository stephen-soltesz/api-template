# Golang api-template

1. DO NOT INSTALL The Go AppEngine SDK

   <strike>https://cloud.google.com/appengine/docs/go/download</strike>

  Instead, install the full Google Cloud SDK, and then install the
  `app-engine-go` component.

        ./setup.sh
        gcloud components install app-engine-go

  Then make the `goapp` command executable (as of google-cloud-sdk-135.0.0):

        chmod 755 /usr/local/google-cloud-sdk/platform/google_appengine/goapp
        export PATH=$PATH:/usr/local/google-cloud-sdk/platform/google_appengine/

1. Verify that you have `go` installed.

  Version 1.7+ is preferred.

        go version

1. Setup and serve the AppEngine app locally.

        GOPATH=$PWD
        goapp get hostsapi
        goapp serve src/hostsapi/app.yaml

  If `goapp get` reports errors like these, they may be safely ignored:

        go install appengine_internal/github.com/golang/protobuf/proto: open /usr/local/google-cloud-sdk/platform/google_appengine/goroot/pkg/linux_amd64_appengine/appengine_internal/github.com/golang/protobuf/proto.a: permission denied
        go install runtime/cgo: open /usr/local/google-cloud-sdk/platform/google_appengine/goroot/pkg/linux_amd64_appengine/runtime/cgo.a: permission denied

  If all packages are not available, you may see errors from `goapp serve` like these:

        2016/11/23 04:11:20 Can't find package "golang.org/x/net/context" in $GOPATH: cannot find package "golang.org/x/net/context" in any of:
          /usr/local/google-cloud-sdk/platform/google_appengine/goroot/src/golang.org/x/net/context (from $GOROOT)
          /vagrant/src/golang.org/x/net/context (from $GOPATH)

1. Check that the REST discovery document is served by the local dev server.

        DISCOVERY=http://localhost:8080/_ah/api/discovery/v1/apis/hosts/v1/rest
        curl $DISCOVERY

1. Deploy app to AppEngine.

        goapp deploy src/hostsapi/app.yaml

  And, check the discovery doc again.

        DISCOVERY=https://dash-test-1.appspot.com/_ah/api/discovery/v1/apis/hosts/v1/rest
        curl $DISCOVERY

1. Run a basic, authenticated client request:

        cd clients
	    ./client_discovery.py

1. Generate the apitools, python client library, and install it locally.

        $ sudo pip install --upgrade google-apputils google-apitools
        $ gen_client --discovery_url=$DISCOVERY \
	        --overwrite --outdir=hosts --root_package=. pip_package
		$ cd hosts
		$ sudo python setup.py install

1. Test the API using a client.

        $ cd clients
		$ ./client_apitools.py
