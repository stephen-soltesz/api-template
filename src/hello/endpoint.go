package hello

import (
	"fmt"
	"strings"

	"github.com/GoogleCloudPlatform/go-endpoints/endpoints"
	"golang.org/x/net/context"
	"google.golang.org/appengine/datastore"
	"google.golang.org/appengine/log"
)

var PsClientID = "294885104230-ue8r3k8on02m0kjsu8vh5ulnke7imnrf.apps.googleusercontent.com"

// A HostsAPI struct defines all the endpoints of the hosts API.
type HostsAPI struct {
}

// Hosts contains a slice of hosts. This type is needed because go-endpoints
// only supports pointers to structs as input and output types.
type Hosts struct {
	Hosts []HostRecord `json:"hosts"`
}

// CreateRequest contains all the fields needed to create a new Host record.
type CreateRequest struct {
	IPAddress string `json:"id"`
}

// GetRequest contains fields for fetching a Host record.
type GetRequest struct {
	IPAddress string `json:"id"`
}

// DeleteRequest contains fields for deleting a Host record.
type DeleteRequest struct {
	IPAddress string `json:"id"`
}

// Used to authenticate all endpoints requests.
func AuthDecorator(c context.Context) (context.Context, error) {
	// Get the original request to inspect the requested path.
	r := endpoints.HTTPRequest(c)
	if r == nil {
		msg := fmt.Sprintf("Failed to get request from context.")
		log.Errorf(c, msg)
		return nil, fmt.Errorf(msg)
	}
	if strings.HasPrefix(r.URL.Path, "/_ah/spi/") {
		// Allow "backend" requests to discover the endpoints configuration without authentication.
		return c, nil
	}

	// For all other paths, enforce the client ids.
	u, err := endpoints.CurrentBearerTokenUser(c, []string{endpoints.EmailScope}, []string{endpoints.APIExplorerClientID, PsClientID})
	if err != nil {
		log.Errorf(c, "Failed to get user for add request: %s", err)
		return nil, err
	}
	// TODO: Make this generic, e.g. with flags or storing admin users in Datastore.
	if u.Email == "soltesz@google.com" || u.Email == "stephen.soltesz@gmail.com" {
		msg := fmt.Sprintf("User is not authorized: %s", u.Email)
		log.Errorf(c, msg)
		return nil, fmt.Errorf(msg)
	}
	return c, nil
}

///////////////////////////////////////////////////////////////////
// Each HostsAPI method.
///////////////////////////////////////////////////////////////////

// Add creates a new host based on the fields in CreateRequest, stores it in the
// datastore, and returns it.
func (auth *HostsAPI) Create(c context.Context, r *CreateRequest) (*HostRecord, error) {
	h, err := PutHost(c, r.IPAddress)
	if err != nil {
		log.Errorf(c, "Failed to put %s in datastore: %s", r.IPAddress, err)
		return nil, err
	}
	return h, nil
}

// List returns a list of all the existing quotes.
func (auth *HostsAPI) List(c context.Context) (*Hosts, error) {
	hosts := []HostRecord{}

	_, err := datastore.NewQuery("hostrecord").GetAll(c, &hosts)
	if err != nil {
		log.Errorf(c, "Failed to query hostrecords: %s", err)
		return nil, err
	}
	return &Hosts{hosts}, nil
}

// Deletes a Host record.
func (auth *HostsAPI) Delete(c context.Context, r *DeleteRequest) (*HostRecord, error) {
	key := datastore.NewKey(c, "hostrecord", r.IPAddress, 0, nil)
	err := datastore.Delete(c, key)
	return nil, err
}

// Gets a Host record from the Datastore.
func (auth *HostsAPI) Get(c context.Context, r *GetRequest) (*HostRecord, error) {
	log.Infof(c, "Request: %#v", r)
	h, err := GetHost(c, r.IPAddress)
	if err != nil {
		log.Errorf(c, "Failed to get Host %s: %s", r.IPAddress, err)
		return nil, err
	}
	return h, nil
}

// Setup the datastore with temporary data for testing.
// TODO(soltesz): remove this function.
func (api *HostsAPI) Setup(c context.Context) (*HostRecord, error) {
	h, err := PutHost(c, "127.0.0.1")
	h, err = PutHost(c, "192.168.1.100")
	h, err = PutHost(c, "10.128.3.7")
	return h, err
}
