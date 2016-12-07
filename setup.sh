#!/bin/bash

FILE=google-cloud-sdk-135.0.0-linux-x86_64.tar.gz
if [[ ! -f $FILE ]] ; then
    wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/${FILE}
fi

if [[ ! -d /usr/local/google-cloud-sdk ]] ; then
    sudo tar -C /usr/local -xvf "${FILE}"
fi

sudo /usr/local/google-cloud-sdk/install.sh

export PATH=$PATH:/usr/local/google-cloud-sdk/bin/
echo "export $PATH"
echo "gcloud init"
