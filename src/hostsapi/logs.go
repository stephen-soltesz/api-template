package hostsapi

import (
	"fmt"
	"log"

	"cloud.google.com/go/logging"
	"golang.org/x/net/context"
)

var logProjectID string = "dash-test-1"
var logClient *logging.Client
var logger *logging.Logger

func init() {
	// var err error
	// ctx := context.Background()

	// Your Google Cloud Platform project ID

	// Creates a client
	// logClient, err = logging.NewClient(ctx, projectID)
	// if err != nil {
	// 	log.Fatalf("Failed to create client: %v", err)
	// }

	// The name of the log to write to
	// logName := "sample-dash-test-1-log"

	// Selects the log to write to
	// logger := logClient.Logger(logName)

	// The data to log
	// text := "Hello, world!"

	// Adds an entry to the log buffer
	// logger.Log(logging.Entry{
	// 	Payload:  text,
	// 	Severity: logging.Critical,
	// })

	// Closes the client and flushes the buffer to the Stackdriver Logging service
	// err = client.Close()
	// if err != nil {
	// 	log.Fatalf("Failed to close client: %v", err)
	// }
	// fmt.Printf("Logged: %v", text)
}

func GetLogger(c context.Context) *logging.Logger {
	var err error
	logClient, err = logging.NewClient(c, logProjectID)
	if err != nil {
		log.Fatalf("Failed to create client: %v", err)
		panic(err)
	}
	// Selects the log to write to
	return logClient.Logger("appengine.googleapis.com/request_log")
}

func logDebugf(c context.Context, format string, a ...interface{}) {
	logger := GetLogger(c)
	logger.LogSync(c, logging.Entry{
		Payload:  fmt.Sprintf(format, a...),
		Severity: logging.Debug,
	})
}
