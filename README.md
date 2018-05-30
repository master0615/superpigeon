## Superpigeon Development With Docker Compose and Machine

Featuring:

- Docker v17.11.0-ce

First, add the GPG key for the official Docker repository to the system:

`$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -`

Add the Docker repository to APT sources:

`$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"`

Next, update the package database with the Docker packages from the newly added repo:

`$ sudo apt-get update`

Make sure you are about to install from the Docker repo instead of the default Ubuntu 16.04 repo:

`$ apt-cache policy docker-ce`

Install Docker:

`$ sudo apt-get install -y docker-ce`

Docker should now be installed, the daemon started, and the process enabled to start on boot. Check that it's running:

`$ sudo systemctl status docker`

The output should be similar to the following, showing that the service is active and running:

`● docker.service - Docker Application Container Engine
   Loaded: loaded (/lib/systemd/system/docker.service; enabled; vendor preset: enabled)
   Active: active (running) since Sun 2016-05-01 06:53:52 CDT; 1 weeks 3 days ago
     Docs: https://docs.docker.com
 Main PID: 749 (docker)`

- Docker Compose v1.18.0

We'll check the current release and if necessary, update it in the command below:

`$ sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-'uname -s'-'uname -m' -o /usr/local/bin/docker-compose`

Next we'll set the permissions:

`$ sudo chmod +x /usr/local/bin/docker-compose`

Then we'll verify that the installation was successful by checking the version:

`$ docker-compose --version`

- Docker Machine v0.13.0

Please make sure docker has been installed:

If you are running on macOS:

`curl -L https://github.com/docker/machine/releases/download/v0.13.0/docker-machine-`uname -s`-`uname -m` >/usr/local/bin/docker-machine && \
  chmod +x /usr/local/bin/docker-machine`
  
If you are running on Linux:  

`$ curl -L https://github.com/docker/machine/releases/download/v0.13.0/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine &&
chmod +x /tmp/docker-machine &&
sudo cp /tmp/docker-machine /usr/local/bin/docker-machine`

- Python 3.5


### Development Local Instructions

1. Start new machine (please make sure virtualbox installed) - `$ docker-machine create -d virtualbox dev;`
1. Use 'dev' machine docker env - `$ eval $(docker-machine env dev)`
1. Build images - `$ docker-compose build`
1. Start services - `$ docker-compose up -d`
1. Create migrations - `$ docker-compose run web /usr/local/bin/python manage.py migrate`
1. Grab IP - `$ docker-machine ip dev` - and view in your browser
1. Update code - `docker-compose build && docker-compose down && docker-compose up -d`

#### Installing Portainer with docker (docker UI management)

1. `$ docker run -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer`
1. Check on browser `http://localhost:9000`
1. Create admin user in browser

#### Running Django without docker deploy
`virtualenv -p python3 ../venv
../venv/bin/pip install -r web/requirements.txt
cd web
../../venv/bin/python manage.py makemigrations api
../../venv/bin/python manage.py migrate
../../venv/bin/python manage.py jenkins --enable-coverage --debug
../../venv/bin/python manage.py runserver`

### Running Angular without docker deploy