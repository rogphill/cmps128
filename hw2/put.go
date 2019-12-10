package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"strings"

	"github.com/gorilla/mux"
)

func putKey(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	// get key value pair
	r.ParseForm()
	fmt.Println("r.Form: ", r.Form)

	if len(r.Form) > 0 {
		key := mux.Vars(r)["key"]
		value := r.Form["val"][0]
		if !isPrimary {
			url := "http://" + mainIPPort + "/keyValue-store/" + key
			body := strings.NewReader(`val=` + value)

			client := http.Client{}
			request, err := http.NewRequest(http.MethodPut, url, body)
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
		} else {

			// case 1: key < 0 || > 200
			if !k.isKeyValid(key) {
				w.WriteHeader(411)
				json.NewEncoder(w).Encode(msgError{Msg: "Error",
					Error: "Key not valid"})
			} else {
				// case 3 key exsits in database
				if k.isKeyExist(key) {
					// case 4 value to be updated is the same
					if value == k.get(key) {
						w.WriteHeader(201)
						json.NewEncoder(w).Encode(replacedMsg{Replaced: true,
							Msg: "Updated successfully"})
					} else {
						// case 4 value to be updated is different
						k.put(key, value)
						w.WriteHeader(201)
						json.NewEncoder(w).Encode(replacedMsg{Replaced: true,
							Msg: "Updated successfully"})
					}
				} else {
					// case 5 key does not exist in database
					k.put(key, value)
					w.WriteHeader(http.StatusCreated)
					json.NewEncoder(w).Encode(replacedMsg{Replaced: false,
						Msg: "Added successfully"})
				}
			}
		}
		// }
	} else {
		w.WriteHeader(411)
		json.NewEncoder(w).Encode(msgError{Msg: "Error",
			Error: "Value is missing"})
	}

}
