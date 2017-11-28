
## Motivation

This project allows a developper to use an environment from a docker image directly, either from a virtual machine
when the OS is work on is not compatible with docker (from windows 7 by example).

## Synopsis

This repository contains a hadoop working environment with the following components

* hadoop
* hdfs
* hive
* hue
* spark through livy

## Usage

As people on Linux or Mac can use docker directly, there is two way to provision
a working environment from this repository.

* docker *(recommanded)*
* vagrant

docker is way more efficient way to host the cluster.

### docker

1) start the containers

```bash
cd docker
docker-compose up
```

2) stop the containers

```bash
cd docker
docker-compose down
```

all the cluster services will be exposed on localhost.

* hue : http://localhost:8888
* hdfs : http://localhost:8020
* hive : http://localhost:10000

### vagrant

1) run the virtual machine, execute :

    vagrant up

2) run installation scripts and docker compose :

    vagrant provision

ansible will keep running on the task.

```
default: TASK [docker-host : configure docker image from docker-compose] ****************
```

operation log is available is the file `docker-compose.log`.

3) check docker compose is up on the vm

```bash
vagrant ssh -c "docker ps"
```


4) stop the virtual machine, execute :

    vagrant halt

5) To reload the virtual machine, execute :

    vagrant reload

6) remove the virtual machine from your disk, execute :

    vagrant destroy

all the cluster services will be exposed on localhost.

* hue : http://192.168.35.10:8888
* hdfs : http://192.168.35.10:8020
* hive : http://192.168.35.10:10000

## Testing

You can check playbook syntax and list tasks running by ansible by using :

    make tests

If it doesn't work due to missing ``ansible`` or ``ansible-galaxy roles``, use :

    apt-get install -y python-pip
    pip install -U ansible
    make install_requirements
