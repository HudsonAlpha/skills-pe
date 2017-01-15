#!/bin/sh

# run as user "wannabe" at startup to as launch the docker service with the date inside the digital ocean droplet

while true;
do
 systemctl enable docker;
 systemctl start  docker;
 docker run -itdv /usr/local/bin/:/usr/local/bin/ centos /usr/local/bin/date.sh -u wannabe;   
 sleep 5 | echo "please wait while the container is being create";
 docker ps;
 exit 0
done

