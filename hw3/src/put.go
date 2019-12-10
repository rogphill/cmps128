package main

import (
	"fmt"
	"net/http"
	"time"

	"github.com/gorilla/mux"
)

func putKey(w http.ResponseWriter, r *http.Request) {
	key := mux.Vars(r)["key"]
	form := parseForm(r)
	replaced := false
	msg := "Added successfully"
	statusCode := http.StatusOK
	if k.isKeyExist(key) {
		replaced = true
		msg = "Updated successfully"
		statusCode = http.StatusCreated
	}

	var t time.Time
	if form["timeStamp"] == "" {
		t = time.Now()
		form["timeStamp"] = t.String()
	} else {
		t, _ = time.Parse(time.Now().String(), form["timeStamp"])
	}

	k.put(key, form["val"], t)
	if form["broadcast"] == "" {
		k.incVectorClock(key)
	} else {
		fmt.Println("Mergine Vector", form["vectorClock"])
		k.mergeVectorClock(key, form["vectorClock"])
		k.incVectorClock(key)
	}

	sendRespondMsg(w, statusCode, &map[string]interface{}{"replaced": replaced, "msg": msg, "payload": k.getVectorClock(key).Set})
	broadcast("keyValue-store/"+key, "PUT", form)
}
