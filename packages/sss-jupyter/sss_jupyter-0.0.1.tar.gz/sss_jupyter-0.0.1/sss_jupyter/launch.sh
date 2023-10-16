#!/bin/bash

set -e

port="8888"
token_length=50

while getopts p:l: OPT; do
    case $OPT in
        p) port=${OPTARG} ;;
        l) token_length=${OPTARG} ;;
    esac
done

if ! python3 -m jupyterlab --version > /dev/null 2>&1; then
    echo "Error: JupyterLab is not installed."
    exit 1
fi

if ! ls ~/.jupyterkey > /dev/null 2>&1; then
    echo "generate ssh key in ~/.jupyterkey..."
    mkdir ~/.jupyterkey
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ~/.jupyterkey/mykey.key -out ~/.jupyterkey/mycert.pem -subj "/C=JA" > /dev/null 2>&1
fi

token=$(cat /dev/urandom | tr -dc '0-9a-f' | fold -w ${token_length} | head -n 1)

nohup python3 -m jupyterlab \
    --ip=0.0.0.0 \
    --port=${port} \
    --certfile="~/.jupyterkey/mycert.pem" \
    --keyfile="~/.jupyterkey/mykey.key" \
    --IdentityProvider.token="${token}" \
    --no-browser \
    > ~/.jupyter.log 2>&1 &

external_ip=$(curl -s ifconfig.me)

echo "JupyterLab server is runnning at:"
echo "    https://${external_ip}:${port}/?token=${token}"
echo ""
echo "JupyterLab logs are stored in ~/.jupyter.log"


