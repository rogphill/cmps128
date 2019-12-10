FROM golang:1.8
WORKDIR /go/src/app
COPY . .

RUN go get -d -v ./...
RUN go install -v ./...

ENV IP=nil PORT=8080 MAINIP=nil 

CMD ["app"]
