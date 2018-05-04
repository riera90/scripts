#!/bin/bash
sudo systemctl start docker.socket
sudo docker run --name=ManageYourAirport --rm -it --net=host -v $(pwd):/ManageYourAirport riera90/symfony-dev
