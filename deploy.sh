#!/usr/bin/env bash

set -e

BRANCH_NAME="$(git symbolic-ref HEAD 2>/dev/null)" ||
BRANCH_NAME="(unnamed branch)"
BRANCH_NAME=${BRANCH_NAME##refs/heads/}

DATE=`date +%Y%m%d%H%m`
DOMAIN_PREFIX=$(echo ${BRANCH_NAME//[^[:alpha:]]/\-} | tr '[:upper:]' '[:lower:]')
BUILD_PREFIX=${DOMAIN_PREFIX//[^[:alpha:]]/_}
BUILD_SUFFIX=${BUILD_NUMBER:-$DATE}
#GIT_PROJECT_NAME=`git remote -v | grep origin | grep fetch | awk '{print $2}' | cut -d '/' -f 2 | sed 's/.git//'`
GIT_PROJECT_NAME="super"
BUILD_NAME="${GIT_PROJECT_NAME}_${BUILD_PREFIX}"
BUILD_TAG="${DOMAIN_PREFIX}-b${BUILD_SUFFIX}"

COMPOSE_PROJECT_NAME="${GIT_PROJECT_NAME}_" BUILD_TAG="${BUILD_TAG}" docker-compose build

DOMAIN_PREFIX="${DOMAIN_PREFIX}" BUILD_NAME="${GIT_PROJECT_NAME}_" BUILD_TAG="${BUILD_TAG}" docker stack deploy --prune -c stack.yml "${BUILD_NAME}"
