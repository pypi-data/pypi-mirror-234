# base image  
FROM python:3.10 as base
# setup environment variable  

ENV DockerHOME=/home/app/webapp

# set work directory  
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME 

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies  
RUN pip install --upgrade pip

# copy whole project to your docker home directory. 
COPY requirements.txt $DockerHOME

# run this command to install all dependencies  
COPY . ${DockerHOME}

RUN SETUPTOOLS_SCM_PRETEND_VERSION=100 pip install .

FROM base as test

# install the dev requirements 
COPY requirements_dev.txt $DockerHOME

RUN pip install -r requirements_dev.txt

CMD ["pytest"]
