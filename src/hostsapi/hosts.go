// Copyright 2016 Google Inc. All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
package hostsapi

import (
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/GoogleCloudPlatform/go-endpoints/endpoints"

	"golang.org/x/net/context"
	"google.golang.org/appengine/datastore"
)

// Host records represent a single machine.
type Host struct {
	IPAddress string    `json:"id" endpoints:"req" datastore:"id"`
	Created   time.Time `json:"created" datastore:"created"`
}

// RegisterMethod adds metadata to map the RPCService to an endpoints discovery document.
func RegisterMethod(api *endpoints.RPCService, realName, httpMethod, httpPath, scope string) {
	info := api.MethodByName(realName).Info()
	info.Name = strings.ToLower(realName)
	info.HTTPMethod = httpMethod
	info.Path = httpPath
	info.Scopes = append(info.Scopes, scope)
}

func init() {
	// register the quotes API with cloud endpoints.
	api, err := endpoints.RegisterService(&HostsAPI{}, "hosts", "v1", "Hosts API (Golang)", true)
	if err != nil {
		panic(err)
	}

	// Setup the endpoint for each API function.
	RegisterMethod(api, "List", "GET", "hosts", endpoints.EmailScope)
	RegisterMethod(api, "Create", "POST", "hosts", endpoints.EmailScope)
	RegisterMethod(api, "Delete", "POST", "hosts/{id}", endpoints.EmailScope)
	RegisterMethod(api, "Get", "GET", "hosts/{id}", endpoints.EmailScope)
	RegisterMethod(api, "Setup", "GET", "setup", endpoints.EmailScope)

	// Start handling cloud endpoint requests.
	endpoints.DefaultServer.ContextDecorator = AuthDecorator
	endpoints.HandleHTTP()

	// http.HandleFunc("/v1/hosts/127.0.0.1/proofOfConcept", Handler)
	http.HandleFunc("/", HelloHandler)
}

// GetHost retrieves a Host record from Datastore.
func GetHost(ctx context.Context, ipaddr string) (*Host, error) {
	var h Host
	key := datastore.NewKey(ctx, "HostsGo", ipaddr, 0, nil)
	if err := datastore.Get(ctx, key, &h); err != nil {
		return nil, err
	}
	return &h, nil
}

// PutHost saves a Host record to Datstore.
func PutHost(ctx context.Context, ipaddr string) (*Host, error) {
	h := Host{
		IPAddress: ipaddr,
		// NOTE: python clients fail to decode the format of the 'date-time' type at nanosecond resolution.
		Created: time.Now().UTC().Truncate(time.Second),
	}
	key := datastore.NewKey(ctx, "HostsGo", ipaddr, 0, nil)
	if _, err := datastore.Put(ctx, key, &h); err != nil {
		return nil, err
	}
	return &h, nil
}

// A generic request handler.
func HelloHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello, world")
}
