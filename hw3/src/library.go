package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"
	"strings"
)

func broadcast(route string, typeReq string, form map[string]string) {
	if form["broadcast"] == "" {
		form["broadcast"] = "true"

		var body string
		for key, val := range form {
			body += key + "=" + val + "&"
		}
		body = strings.TrimRight(body, "&")
		for ipport := range view.Set {
			if ipport != iPPort {
				url := "http://" + ipport + "/" + route
				client := http.Client{}

				request, err := http.NewRequest(typeReq, url, strings.NewReader(body))
				request.Header.Set("Content-Type", "application/x-www-form-urlencoded")
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
}

func parseForm(r *http.Request) map[string]string {
	body, _ := ioutil.ReadAll(r.Body)
	strBody, _ := url.QueryUnescape(string(body))
	fmt.Println("ReceivedBody", strBody)
	form := make(map[string]string)
	if strBody != "" {
		for _, elm := range strings.Split(strBody, "&") {
			s := strings.Split(elm, "=")
			form[s[0]] = s[1]
		}
	}
	return form
}

func sendKVS(w http.ResponseWriter, ipport string) {
	encodedKVS, _ := json.Marshal(k.Dict)
	url := "http://" + ipport + "/view"
	client := http.Client{}

	request, err := http.NewRequest("POST", url, bytes.NewBuffer(encodedKVS))
	request.Header.Set("Content-Type", "application/json")
	if err != nil {
		log.Println(err)
	}
	_, err = client.Do(request)
	if err != nil {
		log.Println(err)
	}

}

func receiveKVS(w http.ResponseWriter, r *http.Request) {
	json.NewDecoder(r.Body).Decode(&k.Dict)
	print("Received KVS:", k.Dict)
}

func sendRespondMsg(w http.ResponseWriter, statusCode int, msg *map[string]interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(statusCode)
	json.NewEncoder(w).Encode(msg)
}
