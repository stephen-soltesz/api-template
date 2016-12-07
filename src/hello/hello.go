package hello

import (
	"fmt"
	"net/http"
	"time"

	"github.com/GoogleCloudPlatform/go-endpoints/endpoints"

	// --logs_path=your-path/your-logfile-name

	// "google.golang.org/appengine"
	"golang.org/x/net/context"
	"google.golang.org/appengine"
	"google.golang.org/appengine/datastore"
	"google.golang.org/appengine/log"
)

type HostRecord struct {
	IPAddress string    `json:"ip_address" endpoints:"req"`
	Created   time.Time `json:"created"`
}

func init() {
	// register the quotes API with cloud endpoints.
	api, err := endpoints.RegisterService(&HostsAPI{}, "hosts", "v1", "Hosts API", true)
	if err != nil {
		panic(err)
	}

	// adapt the name, method, and path for each method.
	info := api.MethodByName("List").Info()
	info.Name, info.HTTPMethod, info.Path = "list", "GET", "hosts"

	info = api.MethodByName("Create").Info()
	info.Name, info.HTTPMethod, info.Path = "create", "POST", "hosts"

	info = api.MethodByName("Delete").Info()
	info.Name, info.HTTPMethod, info.Path = "delete", "POST", "hosts/{id}"

	info = api.MethodByName("Get").Info()
	info.Name, info.HTTPMethod, info.Path = "get", "GET", "hosts/{id}"

	info = api.MethodByName("Setup").Info()
	info.Name, info.HTTPMethod, info.Path = "setup", "GET", "setup"

	// Start handling cloud endpoint requests.
	endpoints.DefaultServer.ContextDecorator = AuthDecorator
	endpoints.HandleHTTP()

	// http.HandleFunc("/v1/hosts/127.0.0.1/proofOfConcept", Handler)
	http.HandleFunc("/", HelloHandler)
}

func GetHost(ctx context.Context, ipaddr string) (*HostRecord, error) {
	var h HostRecord
	key := datastore.NewKey(ctx, "hostrecord", ipaddr, 0, nil)
	if err := datastore.Get(ctx, key, &h); err != nil {
		return nil, err
	}
	return &h, nil
}

func PutHost(ctx context.Context, ipaddr string) (*HostRecord, error) {
	h := HostRecord{
		IPAddress: ipaddr,
		// NOTE: python fails to decode the format of the 'date-time' type at nanosecond resolution.
		Created: time.Now().UTC().Truncate(time.Second),
	}
	key := datastore.NewKey(ctx, "hostrecord", ipaddr, 0, nil)
	if _, err := datastore.Put(ctx, key, &h); err != nil {
		return nil, err
	}
	return &h, nil
}

func HelloHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello, world")
}

func Handler(w http.ResponseWriter, r *http.Request) {
	ctx := appengine.NewContext(r)

	// Get remote IP.
	remoteIp, ok := r.Header["X-Appengine-Remote-Addr"]
	if !ok {
		log.Errorf(ctx, "Found no host address for header: X-Appengine-Remote-Addr")
		return
	}
	log.Infof(ctx, "This is a test request for %s.", remoteIp[0])

	// Log all headers for fun.
	for k, v := range r.Header {
		log.Infof(ctx, "%s %s", k, v)
	}

	// Try to get a pre-defined host record.
	log.Infof(ctx, "About to call datastore.Get()")
	h, err := GetHost(ctx, remoteIp[0])
	if err != nil {
		log.Infof(ctx, "Did not find %s in datastore: %s", remoteIp[0], err)

		log.Infof(ctx, "Trying to datastore.Put() new record for: %s", remoteIp[0])
		h, err = PutHost(ctx, remoteIp[0])
		if err != nil {
			log.Infof(ctx, "Failed to put %s in datastore: %s", remoteIp[0], err)
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		log.Infof(ctx, "Saved the HostRecord for %#v", h)
	}
	log.Infof(ctx, "Retrieved the HostRecord for %#v", h)

	// Basic response.
	w.Header().Set("Content-Type", "application/json")
	fmt.Fprint(w, `{"Stage2URL": "https://storage.googleapis.com/dash-test-1/stage2/stage2.json"}`)

}
