#! /bin/bash

path_to_doctl=$(which doctl)
if [ ! -x "$path_to_doctl" ] ; then
	echo "doctl is not in your path! Follow the README.md."
	exit 1
fi

repo_dir=${PWD##*/}
if [ $repo_dir != "chozian-skills-pe" ] ; then
	echo "You are not in the chozian-skills-pe directory! Follow the README.md."
	exit 1
fi

echo
echo "Setting correct permissions for the SSH private key ..."
chmod 0600 ./id_rsa.ha-do-chozian && \
echo && \
echo "Initializing your authorization with DigitalOcean ..." && \
doctl auth init && \
echo && \
echo "Importing the necessary SSH public key to DigitalOcean ..." && \
doctl compute ssh-key import chozian --public-key-file id_rsa.ha-do-chozian.pub && \
echo && \
echo "Creating the droplet according to the objective requirements ..." && \
doctl compute droplet create ha-do-chozian --image centos-7-0-x64 --region nyc1 --size 512mb --ssh-keys 64:26:ef:16:da:fb:b7:71:a1:27:25:2c:5d:bc:4c:6e --user-data-file ./cloud-config --wait && \
echo && \
echo "Please wait up to 5 minutes for all of the automated configuration to complete upon first boot up of the droplet. Then the droplet may be examined to confirm that all objectives have been met." && \
echo && \
echo "Logging you in via SSH as root in 10 seconds ..." && \
sleep 2 && \
echo "..." && \
sleep 2 && \
echo "..." && \
sleep 2 && \
echo "..." && \
sleep 2 && \
echo "..." && \
sleep 2 && \
doctl compute ssh ha-do-chozian --ssh-key-path ./id_rsa.ha-do-chozian
