package main

import (
	"encoding/json"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func getKey(w http.ResponseWriter, r *http.Request) {
	key := mux.Vars(r)["key"]
	form := parseForm(r)
	var clientVectorClock map[string]int
	json.Unmarshal([]byte(form["payload"]), &clientVectorClock)

	if k.isKeyExist(key) {
		sendRespondMsg(w, http.StatusOK, &map[string]interface{}{"result": "Success", "value": k.get(key), "payload": clientVectorClock})
	} else {
		sendRespondMsg(w, http.StatusNotFound, &map[string]interface{}{"result": "Error", "msg": "Key does not exist", "payload": form["payload"]})
	}

}

func getAllKey(w http.ResponseWriter, r *http.Request) {
	log.Println(k.Dict)
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(k.Dict)

}
