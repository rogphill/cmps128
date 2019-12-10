package main

import (
	"io"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func helloWorld(w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "Hello world!")
	w.WriteHeader(http.StatusOK)
}

func checkPost(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusMethodNotAllowed)
	w.Write([]byte("Should not support this method"))

}

func checkTest(w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "GET request received")

}

func testMsg(w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "POST message received: "+mux.Vars(r)["msg"])
	w.WriteHeader(http.StatusOK)
}

func main() {
	r := mux.NewRouter()
	r.HandleFunc("/hello", helloWorld).Methods("GET")
	r.HandleFunc("/hello", checkPost).Methods("POST")
	r.HandleFunc("/test", checkTest).Methods("GET")
	r.HandleFunc("/test", testMsg).Queries("msg", "{msg}").Methods("POST")
	r.HandleFunc("/test", testMsg).Methods("POST")

	log.Fatal(http.ListenAndServe(":8080", r))
}
