FROM python:3.9

RUN pip install -U pip
RUN python -m pip install -U --force-reinstall pip


ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# RUN mkdir /var/log/

# set a directory for the app
WORKDIR employee_portal

COPY requirements.txt /employee_portal/

# install dependencies
RUN pip install -r requirements.txt


# tell the port number the container should expose
EXPOSE 8000

# copy all the files to the container
COPY . /employee_portal/
RUN apt-get install bash
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
