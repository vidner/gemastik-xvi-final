#!/bin/sh
CGO_ENABLED=1 GOOS=linux GOARCH=amd64 go build -o gw.app .
/app/src/gw.app