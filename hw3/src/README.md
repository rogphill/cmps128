# File structure and how to run / test things
### Notes about test script
- Before running the test script, need to make sure we have an image tagged `testing` and a subnet tagged `mynet`. Run these commands:
```
sudo make clean
docker network create --subnet=10.0.0.0/16 mynet
docker build -t testing .
```
- Once you have created a subnet, you don't need to create the subnet anymore. Notice in hw3_test.py, the `networkIpAddress` matches the subnet IP, and the `networkName` matches the name of the subnet you've created.
- Before re-running test script after making changes, run the following commands:
```
sudo make clean
docker build -t testing .
```
- Then run 
```
python3 hw3_test.py
```

delete.go
- implements DELETE key method

get.go 
- implements GET method

kvs.go 
- implements getters and setters for kvs

library.go
- implements forwarding and broadcasting 

main.go 
- Initialize kvs
- initialize view

Makefile 
- `make` - create 3 containers 
- `make show<n>` - show the log for the nth container (1, 2, 3)
- `make PUT` - write a PUT request via curl with key=akobir
- `make GET` - write a GET request via curl to get key=akobir
- `make DELETE` - write a DELETE request via curl to delete key=akobir

message.go
- defines different types of messages to be returned 

search.go 
- implements SEARCH method (not used in this HW)

set.go 
- implements getters and setters for VIEWS (a set of views)

view.go
- implements GET method for VIEWS (/views)
- may add PUT and DELETE here 

How to write new methods
- create a new file with the method name 
- make sure we're declaring `package main` so main.go will have access to this method






