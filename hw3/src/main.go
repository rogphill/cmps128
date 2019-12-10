package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gorilla/mux"
)

var k = newKvs()
var view = newSet(os.Getenv("VIEW"))
var iPPort = os.Getenv("IP_PORT")
var gossipNumber = -1
var amIGossiper = false

func main() {
	r := mux.NewRouter()
	r.HandleFunc("/keyValue-store/{key}", putKey).Methods("PUT")
	r.HandleFunc("/keyValue-store/{key}", getKey).Methods("GET")
	r.HandleFunc("/keyValue-store/{key}", deleteKey).Methods("DELETE")
	r.HandleFunc("/keyValue-store/search/{key}", searchKey).Methods("GET")
	r.HandleFunc("/keyValue-store/", getAllKey).Methods("GET")

	r.HandleFunc("/view", getView).Methods("GET")
	r.HandleFunc("/view", putView).Methods("PUT")
	r.HandleFunc("/view", deleteView).Methods("DELETE")

	// --------- Internal Routes -----------  \\
	r.HandleFunc("/view", receiveKVS).Methods("POST")
	r.HandleFunc("/gossip", receiveGossip).Methods("PUT")

	if selectGossiper() == iPPort {
		amIGossiper = false
	}

	if amIGossiper {
		ticker := time.NewTicker(1 * time.Second)
		quit := make(chan struct{})
		go func() {
			for {
				select {
				case <-ticker.C:
					gossipNumber++
					startGossip()
				case <-quit:
					ticker.Stop()
					return
				}
			}
		}()
	}
	log.Println(iPPort, ": Server is running...")
	log.Fatal(http.ListenAndServe(iPPort, r))
}

func receiveGossip(w http.ResponseWriter, r *http.Request) {
	var body map[string]interface{}
	b, _ := ioutil.ReadAll(r.Body)

	json.Unmarshal(b, &body)
	body = body["kvs"].(map[string]interface{})
	body = body["Dict"].(map[string]interface{})
	fmt.Println("Received kvs:", body)
}

func startGossip() {
	body, _ := json.Marshal(map[string]interface{}{"kvs": k, "gossipNum": gossipNumber})
	for ipport := range view.Set {
		if ipport != iPPort {
			url := "http://" + ipport + "/gossip"
			client := http.Client{}

			request, err := http.NewRequest("PUT", url, bytes.NewReader(body))
			request.Header.Set("Content-Type", "application/json")
			if err != nil {
				log.Println(err)
			}
			_, err = client.Do(request)
			if err != nil {
				log.Println(err)
			}
		}
	}

}

func selectGossiper() string {
	gossiper := iPPort
	for key := range view.Set {
		if gossiper > key {
			gossiper = key
		}
	}
	return gossiper
}
