ARG VERSION

FROM mageai/mageai:latest

# Add non-root user for Mage service
RUN adduser --disabled-password --gecos '' mage && adduser mage mage

# Grant the user permissions to the Mage related directories
RUN mkdir /home/src/mage_data; chown -R mage /home/src/mage_data
RUN mkdir /home/src/default_repo; chown -R mage /home/src/default_repo

RUN pip3 install -r path/to/requirements.txt

# Set the Mage user
USER mage

ENV PYTHONPATH="${PYTHONPATH}:/home/mage/.local/lib/python3.10/site-packages"

WORKDIR /home/src

CMD ["/bin/sh", "-c", "/app/run_app.sh"]