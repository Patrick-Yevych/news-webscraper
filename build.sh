#!/bin/bash
docker build -f ./service-mysql/dockerfile -t mysql-database .
docker build -f ./service-webapp/dockerfile -t web-app .
docker build -f ./service-scache/dockerfile -t scraper-cache .
docker-compose up