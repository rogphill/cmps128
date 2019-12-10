package main

import (
	"encoding/json"
	"log"
	"net/http"
)

func sendRequest(route string, typeReq string, w http.ResponseWriter) {
	url := "http://" + mainIPPort + "/keyValue-store/" + route
	client := http.Client{}
	request, err := http.NewRequest(typeReq, url, nil)
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
	json.NewEncoder(w).Encode(result)

}
