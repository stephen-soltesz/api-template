#!/bin/bash

set -ex

SDK=google-cloud-sdk-135.0.0-linux-x86_64.tar.gz
if [[ ! -f ${SDK} ]] ; then
    wget "https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/${SDK}"
fi

if [[ ! -d ${HOME}/local/google-cloud-sdk ]] ; then
    mkdir -p ${HOME}/local/google-cloud-sdk
    tar -C ${HOME}/local -xvf "${SDK}"
fi

${HOME}/local/google-cloud-sdk/install.sh

echo "Log out of your current shell, or add the SDK to your PATH:"
echo ""
echo "    export PATH=\$PATH:\${HOME}/local/google-cloud-sdk/bin/"
echo "Then run:"
echo "    gcloud init"
