## Introduction

The purpose of this readme file is to detail the needed steps in order to run the 
django backend

Before any of the following steps are made, some environment variables need to be set.
Please follow [this guide](./environment.variables.readme.md) on what those variables are and how to set them up.

You can either do this manually, or set it up using docker.

# Manual setup
There are 3 main steps:

1. Setting up the virtual environment
2. Installing the dependencies
3. Running the server

### 1. Creating  the virtual environment

> **NOTE**: This project requires that you have python 3.10 installed


#### 1.1. Install virtualenv globally

```
pip install virtualenv
```

#### 1.2. Creating the virtual environment

You'll need to cd into the root directory of the project.

The root directory in our case is called `backend`

> **NOTE**: There are 2 folders `backend`, you'll need to be in the parent one

Create the virtual environment by running the following

```bash
virtualenv .
```

#### 1.3. Activating the virtual environment

```bash
.\Scripts\activate
```
### 2. Installing the requirements
Install the project dependencies by running
```bash
pip install -r requirements.txt
```
### 2. Running the server

#### 2.1 Run database migrations
You first need to run the database migrations in order to create your database models
```bash
python manage.py migrate
```

#### 2.2 Running the server
FINALLY, run the server using this command

```bash
python manage.py runserver
```

# Using docker

This should be as simple as running the `docker compose up` in the `backend` root directory of the application.