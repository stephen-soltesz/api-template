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
func (api *HostsAPI) Create(c context.Context, r *AddRequest) (*HostRecord, error) {
	// u, err := endpoints.CurrentBearerTokenUser(c, []string{endpoints.EmailScope}, []string{endpoints.APIExplorerClientID})
	// if err != nil {
	// 	log.Errorf(c, "Failed to get user for add request: %s", err)
	// 	return nil, err
	// }
	// log.Infof(c, "User: %s", u.ID)
	// log.Infof(c, "User: %s", u.Email)
	// log.Infof(c, "User: %s", u.ClientID)

	h, err := PutHost(c, r.IPAddress)
	if err != nil {
		log.Errorf(c, "Failed to put %s in datastore: %s", r.IPAddress, err)
		return nil, err
	}

	return h, nil
}

// List returns a list of all the existing quotes.
func (api *HostsAPI) List(c context.Context) (*Hosts, error) {
	// u, err := endpoints.CurrentBearerTokenUser(c, []string{endpoints.EmailScope}, []string{endpoints.APIExplorerClientID})
	// if err != nil {
	// 	log.Errorf(c, "Failed to get user for add request: %s", err)
	// 	return nil, err
	// }
	// log.Infof(c, "User: %s", u.ID)
	// log.Infof(c, "User: %s", u.Email)
	// log.Infof(c, "User: %s", u.ClientID)

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

type DeleteRequest struct {
	IPAddress string `json:"id"`
}

func (api *HostsAPI) Delete(c context.Context, r *DeleteRequest) (*HostRecord, error) {
	key := datastore.NewKey(c, "hostrecord", r.IPAddress, 0, nil)
	err := datastore.Delete(c, key)
	return nil, err
}

func (api *HostsAPI) Setup(c context.Context) (*HostRecord, error) {
	h, err := PutHost(c, "127.0.0.1")
	h, err = PutHost(c, "192.168.1.100")
	h, err = PutHost(c, "10.128.3.7")
	return h, err
}

type GetRequest struct {
	IPAddress string `json:"id"`
}

// defined with "hosts/{id}" path template
func (api *HostsAPI) Get(c context.Context, r *GetRequest) (*HostRecord, error) {
	// u, err := endpoints.CurrentBearerTokenUser(c, []string{endpoints.EmailScope}, []string{endpoints.APIExplorerClientID})
	//err := nil
	// if false { // err != nil {
	// log.Errorf(c, "Failed to get user for add request: %s", err)
	// } else {
	// log.Infof(c, "User: %s", u.ID)
	// log.Infof(c, "User: %s", u.Email)
	// log.Infof(c, "User: %s", u.ClientID)
	// }
	log.Infof(c, "Request: %#v", r)
	h, err := GetHost(c, r.IPAddress)
	if err != nil {
		log.Errorf(c, "Failed to get Host %s: %s", r.IPAddress, err)
		return nil, err
	}
	return h, nil
}
