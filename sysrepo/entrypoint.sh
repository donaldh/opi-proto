#!/usr/bin/bash

if [ -z "${PUBKEY}" ]
then
    echo "Please run OPI container with '-e PUBKEY=${key}'"
    exit 1
fi
mkdir /root/.ssh
echo ${PUBKEY} > /root/.ssh/authorized_keys
netopeer2-server -d -v${V}
