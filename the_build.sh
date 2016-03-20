#!/bin/bash -e

# i wish i could do multiple targets but whatever

pushd python/toy
tox
popd
pushd systems
tox
