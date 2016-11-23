# api-template

## golang

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
