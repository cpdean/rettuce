import docker
import pytest
import redis

import docker.tls as tls
import os
from os import path
import time


@pytest.fixture(scope="session")
def docker_client():
    DOCKER_CERTS = os.environ.get("DOCKER_CERT_PATH")
    DOCKER_HOST = "https://" + os.environ.get("DOCKER_HOST").split("//")[-1]

    tls_config = tls.TLSConfig(
        client_cert=(
            path.join(DOCKER_CERTS, 'cert.pem'),
            path.join(DOCKER_CERTS, 'key.pem')
        ),
        ca_cert=path.join(DOCKER_CERTS, 'ca.pem'),
        # because ssl uses hostname, which you have not set up ever
        verify=False
    )

    client = docker.Client(base_url=DOCKER_HOST, tls=tls_config)
    return client


@pytest.yield_fixture()
def native_redis(docker_client):
    redis_container = docker_client.create_container(
        "redis",
        host_config=docker_client.create_host_config(port_bindings={
            6379: None
        }),
        detach=True
    )
    docker_client.start(redis_container.get("Id"))
    hostname = docker_client.base_url.split("//")[-1].split(":")[0]
    port = docker_client.port(
        redis_container.get("Id"),
        6379
    )[0]["HostPort"]
    # wait until redis is ready
    attempt = 0
    while True:
        try:
            redis.Redis(hostname, int(port)).get('fake')
            break
        except redis.exceptions.ConnectionError:
            if attempt > 3:
                raise
            time.sleep(1)
    yield hostname, int(port)
    docker_client.kill(redis_container.get("Id"))


def test_redis_connection_works(native_redis):
    h, p = native_redis
    client = redis.Redis(host=h, port=p)
    client.set("a", "test")
    assert client.get("b") is None
    assert client.get("a") == b"test"
