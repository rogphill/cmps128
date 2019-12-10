package main

import (
	"encoding/json"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func isKeyExist(w http.ResponseWriter, r *http.Request) {
	key := mux.Vars(r)["key"]
	w.Header().Set("Content-Type", "application/json")
	if isPrimary {
		log.Println("Primary received the request")
		if k.isKeyExist(key) {
			w.WriteHeader(200)
			json.NewEncoder(w).Encode(msgValue{Msg: "Success", Value: k.get(key)})
		} else {
			w.WriteHeader(404)
			json.NewEncoder(w).Encode(msgError{Msg: "Error", Error: "Key does not exist"})
		}
	} else {
		sendRequest(key, "GET", w)
	}
}
