# Agent World Control
Educational project for agent management using Flask, PostgreSQL, Docker, Nginx with SSL and Vagrant.
Keepalived, Corosync and Pacemaker, and Redis message exchange.

## Run
git clone https://github.com/GeneralYosif/agent-world-control.git
cd agent-world-control
vagrant up
vagrant ssh
sudo systemctl enable docker
sudo systemctl start docker
cd /vagrant
docker compose up --build


## Access
https://192.168.56.10 - application
http://192.168.56.10:19999/ - netdata
https://github.com/GeneralYosif/agent-world-control - GitHub repository