## Introduction

The purpose of this readme file is to detail the needed steps in order to run the 
django backend

There are 3 main steps:

1. Setting up the virtual environment
2. Installing the dependencies
2. Running the server

### 1. Creating  the virtual environment

> **NOTE**: This project requires that you have python 3.10 installed


#### 2.1. Install virtualenv globally

```
pip install virtualenv
```

#### 2.2. Creating the virtual environment

You'll need to cd into the root directory of the project.

The root directory in our case is called `backend`

> **NOTE**: There are 2 folders `backend`, you'll need to be in the parent one

Create the virtual environment by running the following

```bash
virtualenv .
```

#### 2.3. Activating the virtual environment

```bash
.\Scripts\activate
```
### 3. Installing the requirements
Install the project dependencies by running
```bash
pip install -r requirements.txt
```
### 4. Running the server

#### 4.1 Run database migrations
You first need to run the database migrations in order to create your database models
```bash
python manage.py migrate
```

#### 4.2 Running the server
FINALLY, run the server using this command

```bash
python manage.py runserver
```