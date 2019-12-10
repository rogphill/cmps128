package main

import (
	"log"
	"net/http"
	"strings"
)

func getView(w http.ResponseWriter, r *http.Request) {
	var v string
	for ipport := range view.Set {
		v += ipport + ","
	}
	v = strings.TrimRight(v, ",")

	sendRespondMsg(w, http.StatusOK, &map[string]interface{}{"view": v})
}

func putView(w http.ResponseWriter, r *http.Request) {
	form := parseForm(r)
	ipport := form["ip_port"]

	if !view.isExist(ipport) {
		view.put(ipport)
		if form["broadcast"] == "" {
			sendKVS(w, ipport)
			log.Println(iPPort + ": Change View broadcasted ...")
		} else {
			log.Println(iPPort + ": Broadcasted recieved ...")

		}
		broadcast("view", "PUT", form)
		sendRespondMsg(w, http.StatusOK, &map[string]interface{}{"result": "Success", "msg": "Successfully added " + ipport + " to view"})
	} else {
		sendRespondMsg(w, http.StatusNotFound, &map[string]interface{}{"result": "Error", "msg": ipport + " is not in current view"})
	}
}

func deleteView(w http.ResponseWriter, r *http.Request) {
	form := parseForm(r)
	ipPort := form["ip_port"]

	if view.isExist(ipPort) {
		view.delete(ipPort)
		broadcast("view", "DELETE", form)
		sendRespondMsg(w, http.StatusOK, &map[string]interface{}{"result": "Success", "msg": "Successfully removed " + ipPort + " from view"})
	} else {
		sendRespondMsg(w, http.StatusNotFound, &map[string]interface{}{"result": "Error", "msg": ipPort + " is not in current view"})
	}
}
