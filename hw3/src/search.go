package main

import (
	"net/http"

	"github.com/gorilla/mux"
)

func searchKey(w http.ResponseWriter, r *http.Request) {
	sendRespondMsg(w, http.StatusOK, &map[string]interface{}{"isExists": k.isKeyExist(mux.Vars(r)["key"]), "result": "Success", "payload": parseForm(r)["payload"]})
}
