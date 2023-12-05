# FixTime

[![License MIT](https://img.shields.io/badge/licence-MIT-green)](https://opensource.org/license/mit/)
[![Code style black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![Python versions](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C3.11-blue)](#)
[![Django versions](https://img.shields.io/badge/Django-3.2-blue?logo=django)](#)
[![Nginx version](https://img.shields.io/badge/Nginx-1.22-blue?logo=nginx)](#)
[![Postgres version](https://img.shields.io/badge/PSQL-14-blue?logo=postgresql)](#)

"Fix time" - A time tracker that allows monitoring the time spent on tasks.


## Features

Time control
![dashboard](https://github.com/andprov/fix_time/blob/main/tracker/static_front/img/dashboard.png)

Project control
![project](https://github.com/andprov/fix_time/blob/main/tracker/static_front/img/project.png)

Report
![report](https://github.com/andprov/fix_time/blob/main/tracker/static_front/img/report.png)


## Installation

### Running the project locally

Clone a repository:
```shell
git clone git clone <https or SSH URL>
```

Go to the project directory:
```shell
cd fix_time
```

Create `.env` file:
```shell
touch .env
```

Template for `.env` file:
```shell
# Django settings
DEBUG=True
SECRET_KEY=<django_secret_key>
ALLOWED_HOSTS=127.0.0.1;localhost;<example.com;xxx.xxx.xxx.xxx>

# DB
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=fixtime
DB_HOST=db
DB_PORT=5432

# Superuser
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@admin.com
ADMIN_PASSWORD=admin
```

Deploy the application:
```shell
docker compose -f docker-compose.dev.yml up -d
```

### Running a project on a remote server
To deploy to a remote server, you need to clone the repository to a local machine. 
Prepare and upload images to the Docker Pub.

Clone a repository:
```shell
git clone git clone <https or SSH URL>
```

Go to the project directory:
```shell
cd fix_time
```

Create `.env` file:
```shell
touch .env
```

Template for `.env` file:
```shell
# Django settings
DEBUG=False
SECRET_KEY=<django_secret_key>
ALLOWED_HOSTS=127.0.0.1;localhost;<example.com;xxx.xxx.xxx.xxx>

# SMTP
EMAIL_HOST=<smtp.example.com>
EMAIL_PORT=<port>
EMAIL_HOST_USER=<username>
EMAIL_HOST_PASSWORD=<password>

# DB
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=fixtime
DB_HOST=db
DB_PORT=5432

# Docker images
BACKEND_IMAGE=<username>/tracker_back
GATEWAY_IMAGE=<username>/tracker_gateway

# Superuser
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@admin.com
ADMIN_PASSWORD=admin
```

Create docker images images:
```shell
sudo docker build -t <username>/tracker_back tracker/
sudo docker build -t <username>/tracker_gateway gateway/
```

Upload images to Docker Hub:
```shell
sudo docker push <username>/tracker_back
sudo docker push <username>/tracker_gateway
```

Copy the `.env` and `docker-compose.prod.yml` files to a remote server
```shell
scp .env docker-compose.prod.yml <username>@<server_address>:/home/<username>/<app_name>
```

Deploy the application on the server:
```shell
sudo docker compose -f docker-compose.prod.yml up -d
```
