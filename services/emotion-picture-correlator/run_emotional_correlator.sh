#!/bin/bash

root=$(dirname "$0")

docker-compose build && docker-compose up -d