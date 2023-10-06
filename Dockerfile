FROM python:3.9-alpine3.13
LABEL maintainer="Sanjit Khanal"  
#Telss who is maintaining the image

ENV PYTHONUNBUFFERED 1
#This is to tell python to run in unbuffered mode which is recommended when running python within docker containers.
#It tells python to not buffer the outputs but rather print them directly.

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV= false
RUN python -m venv /py && \ 
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# RUN python -m venv /py && \  
# This is to create a virtual environment in python to store all the dependencies of the project.
# safegaurds against conflicting dependencies that may come with the base image.    

#     /py/bin/pip install --upgrade pip && \
#     specify full path and then upgrade pip to the latest version.

#     /py/bin/pip install -r /tmp/requirements.txt && \
#    install all the dependencies from the requirements.txt file.

#     rm -rf /tmp && \
#     remove the temporary directory. we do not want any extra dependencies in our image once it has been created.
#     Remove tmp file to keep docker image small, this will save speed when deploying.

#     adduser \
#     We donot want to run our application as root user. So we create a new user called django-user.
#     If the application does get compraromised, the attacker will not have root access to the container.

#         --disabled-password \
#         --no-create-home \
#         django-user

#WE avoid using multiple run commands because it will create
#multiple layers in the docker image which will increase the size of the image.
#So we use && to run multiple commands in a single layer.


ENV PATH="/py/bin:$PATH"
#This is to tell docker to use the virtual environment we created to run the application.

USER django-user
#This is to tell docker to run the application as django-user and not as root user.
#should be the last command in the docker file.

