# Walkthrough Instructions

These instructions should walk you through using the dont script to setup a digital ocean droplet

### Prerequisites

Make sure you have your Digital Ocean api key available. Once you have that, copy `misc/dorc.example` to `~/.dorc` and paste your key on the api line in the config file. Otherwise, you'll have to supply the key every time you run the dont command (installed below).


You'll need to have some commands available to start. Consult your local package manager if they aren't:
1. python 2.7
2. pip
3. virtualenv
4. gcc
5. rsync

The following development packages are needed as well:
1. python
2. openssl

There are minimal instructions for centos 7 here that should get you going fairy quickly, execute these commands as root to bootstrap the machine quickly:
```
yum -y install http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
yum -y update
yum -y install python-pip gcc python-devel openssl-devel rsync
pip install virtualenv
```

Also, git mangles the permission on the ssh keys, correct them with: `chmod 0600 misc/hudsonalpha*`

### Installing

1. Use virtualenv to create a local environment to work in and activate it: `virtualenv env && . env/bin/activate`
2. Use pip to install ansible: `pip install ansible`
3. Locally install dont: `./do/setup.py install`

To make sure that you have everything, you should have `ansible-playbook` and `dont` commands in your path

### Deploying

* Use `dont` to create a Centos machine
  1. Use `dont list` (run the command without any arguments, it has some minimalist help included to get you started), to list all available droplet sizes, images, and datacenters. At the time of this writing, the id for each of the 'chosen' items were 0 (for 512mb image), 46 (for CentOS 7.3.1611 x6), and 0 (for New York 1)
  2. `dont create` has a few flags that need to be given to create a machine: `--size`, `--image`, `--datacenter` (short forms are `-n`, `-i`, and `-d`, respectively). To create a machine, the following command should suffice: `dont create --size 0 --image 46 --datacenter 0 examplehostname`, where examplehostname is a droplet hostname of your choosing
  3. If the command was successful, issue `dont listnodes` to list all active droplets. You should be able to see the hostname, ip address, status, and unique identifier for that machine. Take note of the ip, and place it in a file called `inventory.ini` under `playbooks`, which should look like this:
```
[default]
your_ip_address_here
```
A helpful bash one-liner for this would look like: `echo [default] > playbooks/inventory.ini && dont listnodes | grep -i $hostname | egrep --only-matching '([0-9]+\.){3}[0-9]+' >> playbooks/inventory.ini`
* Use ansible to configure the machine
  1. To run ansible against the remote machine, issue the ansible-playbook command:
```
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook --key-file=/full/path/to/skills-pe/misc/hudsonalpha -i playbooks/inventory.ini playbooks/site.yml
```
  To break this into parts:
    1. `ANSIBLE_HOST_KEY_CHECKING=False` is to prevent ansible from checking the remote hosts against `~/.ssh/known_hosts`. If this is important to you, please leave it out.
    2. `ansbile-playbook` is the command
    3. `--key-file=/full/path/to/skills-pe/misc/hudsonalpha` There is a bug with --key-file if you're manually specifying a key where some ansible modules (like the module that depend on rsync) fail to find the ssh key. Specifying the full path overcomes this.
    4. `-i playbooks/inventory.ini` specifies the 'inventory file', which is ansible parlance for the list of machines you want to run a playbook on
    5. `playbooks/site.yml` is the playbook to execute against
  2. After a while, the playbooks should complete after telling you the status of each task (creating user, installing docker, building docker containers, etc). To log into the machine, use `ssh -i misc/hudsonalpha root@your_ip_address` to login to the machine and verify anything you need to

## Assumptions

There are a few assumptions made throughout this document:
* The user has, at minimum, the ability to install software (locally or administratively) to meet the requirements for the software to run (openssl development packages, rsync, etc)
* The user will execute all commands listed from the 'root' of the cloned directory
* While every effort was made to identify packages and test on a variety of platforms, ultimately this was created and tested on a debian 7 VM (xen) and Mac OS X Sierra with brew installed. Both these machines were previously configured for development. A Centos 7 VM (vmware fusion) was created and tested; instructions for that platform were specifically provided
* Some minimal error-checking is preformed, but this guide assumes some competence with either following the directions pretty closely or being willing to troubleshoot some issues
* The reader has some tolerance for speeling mistakes, as vim's spell checking feature uses a dictionary with some idiosyncrasies

## Further improvements that could be made

* The `dont` script could be made more robust, and accept the string names for creation instead of mapped ids. This would be a trivial change only requiring an extra lookup on the image names, since the distribution and actual name of the image are separated in the object provided
* The `dont` script could have some better ssh key management
* The ansbile playbooks, while reusable as-is, aren't fully worked out. Adding some global variables that optionally override the role variables would be useful and promote more reuse.
