#!/bin/bash
set -eu
# This script will output one set of creds in the current directory.
# The script creates a nats resolver config file called resolver.conf

# Setup NSC env
NSC_ROOT=$(pwd)/nsc
export NKEYS_PATH=$NSC_ROOT/nkeys
export NSC_HOME=$NSC_ROOT/accounts
nsc env -s "${NSC_HOME}/nats"
nsc env

# Create Operator
nsc add operator --sys --name truefoundry

# Create tfy-controlplane account. The seed for this account is provided as an environment variable
# to servicefoundry-server
nsc add account --name tfy-controlplane
# enable JS
nsc edit account --name tfy-controlplane --js-disk-storage 512M

# Create user to create a stream.
nsc add user --account tfy-controlplane --name js-creator
nsc generate creds > "${NSC_ROOT}/user.creds"

# Store account info.
nsc generate config --mem-resolver --config-file "${NSC_ROOT}/resolver.conf"

# Get seed of the account
NKEYS_EXPORT_DIR=$NSC_ROOT/exported-keys
nsc export keys --account tfy-controlplane --accounts --dir "${NKEYS_EXPORT_DIR}"
NKEYS_FILE_NAME=$(ls "${NKEYS_EXPORT_DIR}" | grep "A*.nk" | head -1)
NKEYS_PATH="${NKEYS_EXPORT_DIR}/${NKEYS_FILE_NAME}"
SEED=$(cat "${NKEYS_PATH}")
cat "${NKEYS_PATH}" > nsc/tfy.seed

# Create K8s config map to store the account resolver.
# This will be imported by the main config file.
kubectl create configmap nats-accounts --from-file "nsc/resolver.conf" -n truefoundry -o yaml --dry-run | kubectl apply -f -
