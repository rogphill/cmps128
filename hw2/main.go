package main

/* Credits:
 * http://polyglot.ninja/golang-making-http-requests/ Custom Clients/Request
 */

import (
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
)

var isPrimary bool
var mainIPPort string
var k = newKvs()

func main() {
	r := mux.NewRouter()
	isPrimary = os.Getenv("MAINIP") == "nil"
	mainIPPort = os.Getenv("MAINIP")
	r.HandleFunc("/keyValue-store/{key}", isKeyExist).Methods("GET")
	r.HandleFunc("/keyValue-store/search/{key}", searchKey).Methods("GET")
	r.HandleFunc("/keyValue-store/{key}", putKey).Methods("PUT")
	r.HandleFunc("/keyValue-store/{key}", deleteKey).Methods("DELETE")
	if isPrimary {
		log.Println("Primary Server is running...")
	} else {
		log.Println("Instance Server is running...")
	}
	log.Fatal(http.ListenAndServe(":"+os.Getenv("PORT"), r))
}
