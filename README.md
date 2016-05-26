# Swarm Announcer

It will check at regular interval the docker containers using a specified docker network and
register these containers as services and nodes in a consul server.

## Development

### Local

* Install the dependencies with `make deps`
* Run the announcer with `make run --network <network name>`

### With docker

```bash
docker build -t wizcorp/swarm_announcer .
docker run -rm -ti \
    -e DOCKER_HOST=<docker url> \
    -e CONSUL_HOST=<consul host address> \
    -e NETWORK=<network name> \
    wizcorp/swarm_announcer
```

## Updating the image

* Build the docker container with `docker build -t wizcorp/swarm_announcer .`
* Push the image with `docker push wizcorp/swarm_announcer`

_Note:_ You can use a private registry by prepending the registry address to the image name.
```bash
docker build -t registry.in.wizcorp.jp:5000/wizcorp/swarm_announcer .
docker push registry.in.wizcorp.jp:5000/wizcorp/swarm_announcer
```

## Deployment

Deploy with the following command:
```bash
docker pull wizcorp/swarm_announcer
docker run -d --restart=always \
    -e DOCKER_HOST=<docker url> \
    -e CONSUL_HOST=<consul host address> \
    -e NETWORK=<network name> \
    wizcorp/swarm_announcer
```

For example, you can use the following:
```bash
docker pull registry.in.wizcorp.jp:5000/wizcorp/swarm_announcer
docker run -d --restart=always \
    -e DOCKER_HOST=tcp://docker.in.wizcorp.jp:2376 \
    -e CONSUL_HOST=consul.service.swarm.wizcorp.jp \
    -e NETWORK=mybridge \
    registry.in.wizcorp.jp:5000/wizcorp/swarm_announcer
```

Available options:
* `NETWORK`: Specify the docker network used by the containers you want to register.
* `DOCKER_HOST`: The Docker API URL to use. The format is the one expected by [docker-py](http://docker-py.readthedocs.io/en/latest/api/#client-api).
* `CONSUL_HOST`: The Consul host address. See the [python-consul documentation](http://python-consul.readthedocs.io/en/latest/#consul).
* `CONSUL_PORT`: The Consul server port. See the [python-consul documentation](http://python-consul.readthedocs.io/en/latest/#consul).
* `CONSUL_SCHEME`: The scheme to use to contact the Consul server. See the [python-consul documentation](http://python-consul.readthedocs.io/en/latest/#consul).
