FROM python:3.11 AS base_image
# Install g++ and unixodbc-dev: required for installing pyodbc on Linux
RUN apt-get update
RUN apt-get install g++ -y
RUN apt-get install unixodbc-dev -y
# Install Python packages
# Using the 'req_file' parameter (Docker 'ARG') we can build the image based on an arbitrary
# requirements file:
# docker build --build-arg req_file=requirements_2.txt -t cube-backend . 
ARG req_file=requirements.txt
COPY $req_file requirements.txt
# Install the packages into /root/.local in order to easily copy them into the final image
RUN pip install --user --no-warn-script-location -r requirements.txt

# Final image - Python packages are copied from the base_image
FROM python:3.11-slim AS final_image
# Working directory inside the container
WORKDIR /app
# Install ODBC driver (with all the necessary Linux packages)
RUN apt-get update
RUN apt-get install gnupg gnupg1 gnupg2 gunicorn3 curl -y
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17
# Memcached for caching
RUN apt-get install memcached -y
# Copy previously installed Python packages
COPY --from=base_image /root/.local /root/.local
# Append the new location to PATH environment variable
ENV PATH=/root/.local:$PATH
# Copy the contents of the Dockerfile's dir to container's workdir
# Please maintain the .dockerignore file to optimize images!
COPY . .
# Expose port
EXPOSE ${SERVER_PORT_BACKEND}
# Container startup script - stored in a separate file to handle multiple commands
CMD ["sh","-c","./container_startup.sh"]
