#!/bin/bash
echo "running docker daemon"
sudo systemctl start docker.socket
echo "launching docker"
sudo docker run --name=SynfonyApplication --rm -it --net=host -v $(pwd):/application riera90/symfony-dev
