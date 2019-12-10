package main

import (
	"encoding/json"
	"net/http"

	"github.com/gorilla/mux"
)

// Function deletes data from the kvs, if the given key is valid
func deleteKey(w http.ResponseWriter, r *http.Request) {

	key := mux.Vars(r)["key"]
	// If delete request was not sent to the master instance
	if !isPrimary {
		// Send a delete request to the master instance
		sendRequest(key, "DELETE", w)
	} else {
		w.Header().Set("Content-Type", "application/json") // Response Type
		if !k.isKeyValid(key) {
			w.WriteHeader(http.StatusNotFound)
			json.NewEncoder(w).Encode(resultMsg{Result: "Error",
				Msg: "Error"})
		}
		if k.isKeyExist(key) {
			k.deleteKey(key)
			json.NewEncoder(w).Encode(successDelMsg{Msg: "Success"})
		} else {
			w.WriteHeader(http.StatusNotFound)
			json.NewEncoder(w).Encode(msgError{Msg: "Error",
				Error: "Key does not exist"})
		}
	}
}
