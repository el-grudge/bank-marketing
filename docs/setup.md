## Setup Instructions

This project was created on an Ubuntu machine. If you are using a different OS you can find more details on how to install these tools here:

1. [Docker](https://docs.docker.com/engine/install/)
2. [Docker-compose](https://docs.docker.com/compose/install/standalone/)

The following are step-by-step instructions for setting up various tools and environments on Ubuntu. 

Follow the sections below to install and configure each tool.

### 1. Docker

Remove any Docker installations

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

Add Docker's official GPG key

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

Add the repository to Apt sources and install the docker packages

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo docker run hello-world
```

Post installation steps

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
docker run hello-world
```

### 2. Docker-compose

```bash
sudo wget https://github.com/docker/compose/releases/download/v2.28.1/docker-compose-linux-x86_64 -O /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose 
which docker-compose 
```

Follow these instructions to set up the required tools and environments on your Ubuntu system. 

If you encounter any issues during the installation process, refer to the documentation provided by each tool for troubleshooting guidance.