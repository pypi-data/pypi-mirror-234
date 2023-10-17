#!/usr/bin/env bash

function set_config() {
  sudo sed -i "s#\($1 *= *\).*#\1$2#" $3
}


sudo yum update -y
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install hostname pkg-config git wget python3-pip yum-utils docker-ce docker-ce-cli \
  containerd.io docker-buildx-plugin docker-compose-plugin -y
#sudo pip install -r $TD/api/requirements.txt

sudo systemctl enable docker
sudo systemctl start docker

wget https://github.com/apple/foundationdb/releases/download/7.3.3/foundationdb-clients-7.3.3-1.el7.x86_64.rpm -q
sudo rpm -U foundationdb-clients-7.3.3-1.el7.x86_64.rpm --quiet --reinstall
rm -f foundationdb-clients-7.3.3-1.el7.x86_64.rpm

sudo mkdir -p /etc/foundationdb/data /etc/foundationdb/logs
sudo chown -R foundationdb:foundationdb /etc/foundationdb
sudo chmod 777 /etc/foundationdb

DEV_IPS=($(hostname -I))
DEV_IP=${DEV_IPS[0]}

if [[ -z $(grep "tcp://${DEV_IP}:2375" /usr/lib/systemd/system/docker.service) ]]
then
  set_config ExecStart "/usr/bin/dockerd --containerd=/run/containerd/containerd.sock -H tcp://${DEV_IP}:2375 -H unix:///var/run/docker.sock -H fd://" /usr/lib/systemd/system/docker.service
  sudo systemctl daemon-reload
  sudo systemctl restart docker
  sleep 10
fi

sudo modprobe nvme-tcp