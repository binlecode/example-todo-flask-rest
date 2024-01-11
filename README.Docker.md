## docker container image and run

Dockerfile is initialized with `docker init` command.

test build docker image:

```sh
docker build -t example-todo-flask-rest:test .
```

test run docker container in standalone mode:

```sh
docker run --name todo-flask-rest -p 8000:8000 --rm \
  -e "LOG_LEVEL=debug" \
  -e "SCRIPT_NAME=todo-flask-rest" \
  -e "SECRET_KEY=user-a-real-secret-string-for-production" \
  example-todo-flask-rest:test

```

test connection:

```sh
curl -i http://localhost:8000/todo-flask-rest/health
curl -i http://localhost:8000/todo-flask-rest/todos
```

## Docker compose deployment

In compose configuration, the app service has a replicas set to 2.

In Docker Swarm mode, you don't need to specify different ports for each
replica of a service.
Docker Swarm uses a routing mesh that automatically load balances network
traffic between all instances of a service, regardless of the node they are
running on.

However, Docker Desktop for MacOS doesn't fully support the routing mesh
feature, which can lead to "port is already allocated" errors when trying to
run multiple replicas of a service on the same host port.

A workaround for this issue is to use a reverse proxy, such as Nginx or Traefik,
to distribute incoming requests to the replicas of your service.

See [compose.yalm](./compose.yaml) and [nginx.conf](./nginx.conf).

The app service is no longer exposing port 8000 to the host. Instead, it's
exposing port 8000 to the other services in the Docker network.
The nginx service is exposing port 80 to the host, and it's using an Nginx
configuration file (nginx.conf) to forward requests to the app service.

In nginx.conf file, the upstream directive defines a group of servers (in this
case, just the app service) that Nginx can proxy requests to.
The `proxy_pass` directive forwards requests to the `app` service.

```sh
docker compose up --build --remove-orphans -d
```

- `--build` builds images before starting containers
- `--remove-orphans` removes obsolete containers that are no longer related to
  the current Compose configuration
- `-d` starts the containers in detached mode

Application is load balanced and exposed at http://localhost/todo-flask-rest:

```sh
curl -i http://localhost/todo-flask-rest/health
curl -i http://localhost/todo-flask-rest/todos
```

## Deploying your application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

## References

- [Docker's Python guide](https://docs.docker.com/language/python/)
