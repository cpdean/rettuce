import os
from os import path
import time

import docker
import docker.tls as tls
import requests
import pytest

import eserver


@pytest.fixture(scope="session")
def docker_client():
    if "DOCKER_HOST" not in os.environ:
        client = docker.Client(
            base_url='unix://var/run/docker.sock'
        )
        return client
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
def echo_server(docker_client):
    echo_port = 50000
    try:
        guys = docker_client.build(
            path=".",
            rm=True,
            tag="testing_echo_server"
        )
        for i in guys:
            print(i)
        container = docker_client.create_container(
            "testing_echo_server",
            host_config=docker_client.create_host_config(port_bindings={
                echo_port: None
            }),
            detach=True
        )
        docker_client.start(container.get("Id"))
        port = docker_client.port(
            container.get("Id"),
            echo_port
        )[0]["HostPort"]
        if "https" not in docker_client.base_url:
            hostname = "localhost"
        else:
            hostname = docker_client.base_url.split("//")[-1].split(":")[0]
        # wait until redis is ready
        time.sleep(3)
        yield hostname, int(port)
        docker_client.kill(container.get("Id"))
    except requests.exceptions.ConnectionError:
        if 'DOCKER_HOST' not in os.environ:
            raise RuntimeError(
                "failed to connect to docker agent, are you on OSX and forget "
                "to run 'eval $(docker-machine env)' ?"
            )
        else:
            raise


def test_redis_connection_works(echo_server):
    h, p = echo_server
    resp = eserver.client(h, p, b"sup")
    assert resp == b"sup:sup"
