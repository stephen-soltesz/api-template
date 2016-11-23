package hello

import (
	"golang.org/x/net/context"
	"google.golang.org/appengine/datastore"
	"google.golang.org/appengine/log"
)

// A HostsAPI struct defines all the endpoints of the hosts API.
// It will have functions for CRUD like Add, List etc.
type HostsAPI struct {
}

// Hosts contains a slice of hosts. This type is needed because go-endpoints
// only supports pointers to structs as input and output types.
type Hosts struct {
	Hosts []HostRecord `json:"hosts"`
}

// AddRequest contains all the fields needed to create a new Host.
type AddRequest struct {
	IPAddress string
}

// Add creates a new host based on the fields in AddRequest, stores it in the
// datastore, and returns it.
func (api *HostsAPI) Add(c context.Context, r *AddRequest) (*HostRecord, error) {

	h, err := PutHost(c, r.IPAddress)
	if err != nil {
		log.Errorf(c, "Failed to put %s in datastore: %s", r.IPAddress, err)
		return nil, err
	}

	return h, nil
}

// List returns a list of all the existing quotes.
func (api *HostsAPI) List(c context.Context) (*Hosts, error) {
	hosts := []HostRecord{}

	_, err := datastore.NewQuery("hostrecord").GetAll(c, &hosts)
	if err != nil {
		log.Errorf(c, "Failed to query hostrecords: %s", err)
		return nil, err
	}

	// for i, k := range keys {
	// 	quotes[i].UID = k
	// }
	return &Hosts{hosts}, nil
}
