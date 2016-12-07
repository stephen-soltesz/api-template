package hostsapi

import (
	"fmt"
	"testing"

	"net/http/httptest"

	"google.golang.org/appengine/aetest"
)

func TestHandler(t *testing.T) {
	inst, err := aetest.NewInstance(nil)
	if err != nil {
		t.Fatalf("Failed to create instance: %v", err)
	}
	defer inst.Close()

	req, err := inst.NewRequest("GET", "/hello", nil)
	if err != nil {
		t.Fatalf("Failed to create req: %v", err)
	}
	// The test instance of dev_appserver does not add this header automatically.
	req.Header.Set("X-Appengine-Remote-Addr", "127.0.0.1")

	w := httptest.NewRecorder()
	Handler(w, req)
	fmt.Printf("%d - %s", w.Code, w.Body.String())

	// h := HostRecord{
	// 	IPAddress: "127.0.0.1",
	// 	Created:   time.Now(),
	// }
	// key := datastore.NewKey(ctx, "hostrecord", "127.0.0.1", 0, nil)
	// if _, err := datastore.Put(ctx, key, &h); err != nil {
	// 	t.Fatal(err)
	// }

	// w := httptest.NewRecorder()
	// Handler(w, req)
	// fmt.Printf("%d - %s", w.Code, w.Body.String())
}
