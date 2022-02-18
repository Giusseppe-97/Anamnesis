#FROM python:3.8
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Set the working directory to /app

WORKDIR /app


#get msodbcsql17 and install it
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update -y
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17 
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools


# install FreeTDS and dependencies
RUN apt-get update \
    && apt-get install unixodbc -y \
    && apt-get install unixodbc-dev -y \
    && apt-get install freetds-dev -y \
    && apt-get install freetds-bin -y \
    && apt-get install tdsodbc -y \
    && apt-get install --reinstall build-essential -y 
# populate "ocbcinst.ini" as this is where ODBC driver config sits
RUN echo "[FreeTDS]\n\
    Description = FreeTDS Driver\n\
    Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
    Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini

RUN pip install --upgrade pip

COPY ./app/requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
#COPY requirements.txt .
RUN pip install -r requirements.txt
#requirements.txt
#COPY ./app /app
# Make port 80 available to the world outside this container

# Copy the current directory contents into the container at /app
COPY ./app /app/

EXPOSE 8000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000","--forwarded-allow-ips","'*'"]
