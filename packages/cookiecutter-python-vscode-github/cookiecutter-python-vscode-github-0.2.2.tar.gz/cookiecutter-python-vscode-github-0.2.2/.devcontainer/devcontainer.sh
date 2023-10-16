#!/bin/bash

DEVCONTAINER=$(docker ps --all | grep vsc-cookiecutter-python-vscode-github | awk '{print $1}')
docker stop ${DEVCONTAINER}
docker rm ${DEVCONTAINER}
docker volume rm cookiecutter-python-vscode-github_vscode-server
exit 0