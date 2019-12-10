package main

import (
	"net/http"

	"github.com/gorilla/mux"
)

func deleteKey(w http.ResponseWriter, r *http.Request) {
	key := mux.Vars(r)["key"]
	form := parseForm(r)
	if k.isKeyExist(key) {
		k.deleteKey(key)
		sendRespondMsg(w, http.StatusOK, &map[string]interface{}{"result": "Success", "msg": "Key deleted", "payload": form["payload"]})
	} else {
		sendRespondMsg(w, http.StatusNotFound, &map[string]interface{}{"result": "Error", "msg": "Key does not exist", "payload": form["payload"]})
	}
	broadcast("keyValue-store/"+key, "DELETE", form)
}
