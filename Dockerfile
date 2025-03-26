########################################################################################################################
#
# Description:
# Build and run Fake-API-Server-Surveillance for monitoring API server
#
# Environment variables:
# * CONFIG_PATH: The configuration path.
#         - Default values: './fake-api-server-surveillance.yaml'
# * GITHUB_TOKEN: The GitHub token of fake server repository. It must have 2 prioroties: `contents` and `pull-requests`.
#
# Example running docker command line:
# >>> docker build ./ -t <image name>:<image tag>
# >>> docker run --name <container name> \
#                -v <API configuration root directory>:/mit-pyfake-api-server-surveillance/<API configuration root directory> \
#                -e CONFIG_PATH=<API configuration path>
#                <image name>:<image tag>
#
########################################################################################################################

FROM python:3.12

WORKDIR mit-pyfake-api-server-surveillance/

# # Prepare the runtime environment for Python
RUN pip install -U pip
RUN pip install -U poetry
RUN poetry --version

# # Copy needed files and directory to container
COPY . /mit-pyfake-api-server-surveillance/

# # Install the Python dependencies for PyFake-API-Server-Surveillance package
RUN poetry install --without test
# # It already in a virtual runtime environment --- a Docker container, so it doesn't need to create another independent
# # virtual enviroment again in Docker virtual environment
RUN poetry config virtualenvs.create false

# # Run the Fake-API-Server-Surveillance for monitoring API server
#ENTRYPOINT poetry run
CMD poetry run run-fake-server-surveillance

# # For debug
#ENTRYPOINT ["tail", "-f", "/dev/null"]
