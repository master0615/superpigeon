#!/usr/bin/python
import commands
import sys
import os

print commands.getoutput('docker system prune')
print commands.getoutput('docker image prune')
out = commands.getoutput('eval $(docker-machine env live)')
print out
if "does not exist" not in out:
    print commands.getoutput('docker stop $(docker ps -aq)')
    print commands.getoutput('docker rm $(docker ps -aq) --force')
    print commands.getoutput('docker rmi $(docker images -q) --force')

#checking docker version
print commands.getoutput('docker -v && docker-machine -v && docker-compose -v')
#remove existing docker machine live
print commands.getoutput('docker-machine rm live --force')
#create docker machine remote to live
print commands.getoutput('docker-machine create --driver=generic --generic-ip-address=69.5.96.78 --generic-ssh-user=datepalm --generic-ssh-port=2121 --generic-engine-port=9901 --generic-ssh-key=/var/lib/jenkins/.ssh/id_rsa live')
#use docker dev environment
print commands.getoutput('eval $(docker-machine env live)')
#checking docker available machine
print commands.getoutput('docker-machine ls')
#make down all container first
print commands.getoutput('docker-compose down')
#build container to docker machine dev
print commands.getoutput('docker-compose build --no-cache')
#running container services
print commands.getoutput('COMPOSE_PROJECT_NAME=develop-${BUILD_NUMBER}-superpigeon docker-compose up -d')
#check container status
print commands.getoutput('docker-compose ps')