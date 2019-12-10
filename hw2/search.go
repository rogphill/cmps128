package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func searchKey(w http.ResponseWriter, r *http.Request) {
	key := mux.Vars(r)["key"]
	w.Header().Set("Content-Type", "application/json")
	if isPrimary {
		log.Println("Primary received the request")
		if k.isKeyExist(key) {
			w.WriteHeader(200)
			json.NewEncoder(w).Encode(msgExists{Msg: "Success",
				IsExist: "true"})
		} else {
			w.WriteHeader(404)
			json.NewEncoder(w).Encode(msgExists{Msg: "Error",
				IsExist: "false"})
		}
	} else {
		url := "http://" + mainIPPort + "/keyValue-store/search/" + key
		client := http.Client{}
		request, err := http.NewRequest(http.MethodGet, url, nil)
		request.Header.Set("Content-Type", "application/x-www-form-urlencoded")
		if err != nil {
			log.Fatalln(err)
		}
		resp, err := client.Do(request)
		if err != nil {
			log.Fatalln(err)
		}
		var result map[string]interface{}
		w.WriteHeader(resp.StatusCode)
		json.NewDecoder(resp.Body).Decode(&result)
		fmt.Println(result)
		json.NewEncoder(w).Encode(result)
	}
}
