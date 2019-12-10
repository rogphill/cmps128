all: clean
	@echo Build started ...
	$(shell docker build -t testing . > null )
	@echo Build finished ...
run: all
	$(shell docker run -d -p 8081:8088 -e VIEW="10.0.0.20:8088,10.0.0.21:8088,10.0.0.22:8088" -e IP_PORT="10.0.0.20:8088" --net=mynet --ip=10.0.0.20 --name c1 testing > /null)
	@echo Created one container
	$(shell docker run -d -p 8082:8088 -e VIEW="10.0.0.20:8088,10.0.0.21:8088,10.0.0.22:8088" -e IP_PORT="10.0.0.21:8088" --net=mynet --ip=10.0.0.21 --name c2 testing > /null)
	@echo Created second container
	$(shell docker run -d -p 8083:8088 -e VIEW="10.0.0.20:8088,10.0.0.21:8088,10.0.0.22:8088" -e IP_PORT="10.0.0.22:8088" --net=mynet --ip=10.0.0.22 --name c3 testing > /null)
	@echo Created third container
	$(shell docker run -d -p 8084:8088 -e VIEW="10.0.0.20:8088,10.0.0.21:8088,10.0.0.22:8088,10.0.0.23:8088" -e IP_PORT="10.0.0.23:8088" --net=mynet --ip=10.0.0.23 --name c4 testing > /null)
	@echo Created fourth container

clean:rm
	$(shell docker rmi -f testing > /null 2>&1)
	@echo Removed image TESTING
rm:
	$(shell docker stop `docker ps -aq` > /null 2>&1)
	@echo Stopped all containers
	$(shell docker rm `docker ps -aq` > /null 2>&1)
	@echo Removed all containers
check:
	$(eval YAY = $(shell docker images -q testing) )
	@echo MY CAR IS $(YAY)
	
show1:
	$(shell docker logs -f c1)
show2:
	$(shell docker logs -f c2)
show3:
	$(shell docker logs -f c3)
show4:
	$(shell docker logs -f c4)
show:
	docker logs c1
	docker logs c2
	docker logs c3

GET81:
	curl -X GET localhost:8081/keyValue-store/
GET84:
	curl -X GET localhost:8084/keyValue-store/
GET:
	curl -X GET localhost:8081/keyValue-store/vien
PUT:
	curl -X PUT -d "val=hollycow" localhost:8081/keyValue-store/x 
DELETE:
	curl -X DELETE localhost:8081/keyValue-store/akobir -d "val=khamidov"
SEARCH:
	curl -X GET localhost:8081/keyValue-store/search/akobir -d "payload=5"

NEWNODE:
	$(shell docker run -d -p 8084:8088 -e VIEW="10.0.0.20:8088,10.0.0.21:8088,10.0.0.22:8088,10.0.0.23:8088" -e IP_PORT="10.0.0.23:8088" --net=mynet --ip=10.0.0.23 --name c4 testing > /null)
	@echo Created third container
PUTVIEW:
	curl -X PUT localhost:8081/view -d "ip_port=10.0.0.23:8088"

GETVIEW:
	curl -X GET localhost:8081/view

DELETEVIEW:
	curl -X DELETE localhost:8081/view -d "ip_port=10.0.0.23:8088"