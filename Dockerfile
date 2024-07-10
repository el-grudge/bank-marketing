FROM mageai/mageai:latest


ENV PROJECT_NAME=mlops
ENV MAGE_CODE_PATH=/home/src
ENV USER_CODE_PATH=${MAGE_CODE_PATH}/${PROJECT_NAME}

WORKDIR ${MAGE_CODE_PATH}


# Note: this overwrites the requirements.txt file in your new project on first run. 
# You can delete this line for the second run :) 
COPY requirements.txt requirements.txt

# Create the destination directory
# RUN mkdir -p ${USER_CODE_PATH}

# Copy files from the host to the container
# COPY mage_data ${USER_CODE_PATH}