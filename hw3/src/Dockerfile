FROM golang:1.8
WORKDIR /go/src/app
COPY . .

RUN go get -d -v ./...
RUN go install -v ./...

ENV IP_PORT=nil
EXPOSE 8080

CMD ["app"]
