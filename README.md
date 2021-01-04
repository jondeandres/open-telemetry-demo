# OpenTelemetry demo application

## Running services

```
# Build all images

$ docker-compose build

# Run all services

$ docker-compose up all
```

## Test services

```
# Test web

$ docker-compose curl web:8082/home

# Test users

$ docker-compose curl users:8082/get-user
```
