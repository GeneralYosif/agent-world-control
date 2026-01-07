# Agent World Control

## Overview
Microservice-based system for managing agents, built with Flask, PostgreSQL, Redis, Nginx and Docker.

## Architecture
- Flask API – main application
- PostgreSQL – persistent storage
- Redis – message broker (pub/sub)
- Worker – background message processor
- Nginx – reverse proxy + SSL
- Netdata – monitoring

## Run
docker compose up --build

## Messaging
When a new agent is created, an event is published to Redis and processed asynchronously by a worker service.