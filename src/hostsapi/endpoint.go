package hostsapi

import (
	"fmt"
	"strings"

	"github.com/GoogleCloudPlatform/go-endpoints/endpoints"
	"golang.org/x/net/context"
	"google.golang.org/api/iterator"
	// "google.golang.org/appengine/datastore"
	"cloud.google.com/go/datastore"
	"google.golang.org/appengine/log"
)

// Only clients using this ClientID are allowed to authenticate.
var PsClientID = "294885104230-ue8r3k8on02m0kjsu8vh5ulnke7imnrf.apps.googleusercontent.com"

// Only administrators in this set are allowed to authenticate.
// TODO: Make this generic, e.g. with flags or storing admin users in Datastore.
var StaticAdminUsers = map[string]bool{
	"soltesz@google.com":        true,
	"stephen.soltesz@gmail.com": true,
}

// A HostsAPI struct defines all the endpoints of the hosts API.
type HostsAPI struct {
}

// Hosts contains a slice of hosts. This type is needed because go-endpoints
// only supports pointers to structs as input and output types.
type HostCollection struct {
	Items []Host `json:"items"`
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
	log.Debugf(c, "Checking for Authentication on: %s", r.URL.Path)
	if strings.HasPrefix(r.URL.Path, "/_ah/spi/BackendService.getApiConfigs") {
		// Allow "backend" requests to discover the endpoints configuration without authentication.
		log.Debugf(c, "Authentication not necessary for: %s", r.URL.Path)
		return c, nil
	}

	// For all other paths, enforce the client ids.
	u, err := endpoints.CurrentBearerTokenUser(
		c, []string{endpoints.EmailScope}, []string{endpoints.APIExplorerClientID, PsClientID})
	if err != nil {
		log.Errorf(c, "Failed to get user for request: %s", err)
		return nil, err
	}
	// Check that the user is authorized.
	if !StaticAdminUsers[u.Email] {
		msg := fmt.Sprintf("User is NOT authorized: %s", u.Email)
		log.Errorf(c, msg)
		return nil, fmt.Errorf(msg)
	}
	msg := fmt.Sprintf("User is authorized: %s", u.Email)
	log.Infof(c, msg)
	return c, nil
}

///////////////////////////////////////////////////////////////////
// Each HostsAPI method.
///////////////////////////////////////////////////////////////////

// Create adds a new host based on the fields in the given Host and stores it in
// the datastore.
func (auth *HostsAPI) Create(c context.Context, r *Host) (*Host, error) {
	h, err := PutHost(c, r.IPAddress)
	if err != nil {
		log.Errorf(c, "Failed to put %s in datastore: %s", r.IPAddress, err)
		return nil, err
	}
	return h, nil
}

func GetAll(client *datastore.Client, c context.Context, hosts *[]Host) error {
	it := client.Run(c, datastore.NewQuery("HostsGo"))
	for {
		var h Host
		_, err := it.Next(&h)
		if err == iterator.Done {
			break
		}
		if err != nil {
			log.Errorf(c, "Query for all Hosts failed: %s", err)
			return err
		}
		*hosts = append(*hosts, h)
		// fmt.Println(key, p)
	}
	return nil
}

// List returns a list of all the existing quotes.
// TODO: support more options for filtering results.
func (auth *HostsAPI) List(c context.Context) (*HostCollection, error) {
	hosts := []Host{}

	// _, err := datastore.NewQuery("HostsGo").GetAll(c, &hosts)
	err := GetAll(GetDSClient(c), c, &hosts)
	if err != nil {
		log.Errorf(c, "Failed to query hostrecords: %s", err)
		return nil, err
	}
	return &HostCollection{hosts}, nil
}

// Deletes a Host record.
func (auth *HostsAPI) Delete(c context.Context, r *Host) (*Host, error) {
	// key := datastore.NewKey(c, "HostsGo", r.IPAddress, 0, nil)
	// err := datastore.Delete(c, key)
	key := datastore.NameKey("HostsGo", r.IPAddress, nil)
	dsClient := GetDSClient(c)
	err := dsClient.Delete(c, key)
	return nil, err
}

// Gets a Host record from the Datastore.
func (auth *HostsAPI) Get(c context.Context, r *GetRequest) (*Host, error) {
	log.Debugf(c, "Request: %#v", r)
	h, err := GetHost(c, r.IPAddress)
	if err != nil {
		log.Errorf(c, "Failed to get Host %s: %s", r.IPAddress, err)
		return nil, err
	}
	return h, nil
}

// Setup the datastore with temporary data for testing.
// TODO(soltesz): remove this function.
func (api *HostsAPI) Setup(c context.Context) (*Host, error) {
	log.Debugf(c, "Adding ip 1")
	h, err := PutHost(c, "172.0.0.2")
	log.Debugf(c, "Adding ip 2")
	h, err = PutHost(c, "129.168.1.200")
	log.Debugf(c, "Adding ip 3")
	h, err = PutHost(c, "20.128.3.7")
	return h, err
}
