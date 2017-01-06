## Synopsis

This project aims to meet the objectives defined in the README.md at https://github.com/HudsonAlpha/skills-pe.

## Motivation

This was created for a practical skills assessment.

## Installation

Complete the following instructions to meet the defined objectives.

The necessary SSH key pair has already been generated using "ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa.ha-do-chozian -q -N "" -C chozian@TempForHA" and placed in this repo.

First, download and install doctl, a command line tool for DigitalOcean services, on your Mac or Linux box according to the section titled "Option 2 – Download a Release from GitHub" in the README.md at https://github.com/digitalocean/doctl.

Clone this repo by executing "git clone https://github.com/chozian/skills-pe chozian-skills-pe".

Change directory to the cloned repo by executing "cd chozian-skills-pe".

Execute "./setup.sh" to begin the automated setup process.

Enter your DigitalOcean access token when prompted. Then press Enter. If your token is successfully validated, you should receive "Validating token: OK".

Please wait up to 5 minutes for all of the automated setup to complete upon first boot up of the droplet. Then the droplet may be examined to confirm that all objectives have been met.

You may remotely access the droplet via SSH by executing "doctl compute ssh ha-do-chozian --ssh-key-path ./id_rsa.ha-do-chozian".

"docker ps" may be used within the droplet to determine the Docker container ID related to the wannabe user's date/time script. Execute "docker attach [container_id]" to attach to this container. You can detach from this container by pressing CTRL+P, CTRL+Q.

You may log out of the droplet by executing "exit" or shut it down by executing "shutdown -h now".

The droplet may be powered off by executing "doctl compute droplet-action power-off [droplet_ID]". The droplet ID can be obtained by reviewing the output when executing "doctl compute droplet list".

## Contributors

Chris Hozian

## License

Unlicense

