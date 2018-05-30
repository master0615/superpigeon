#!/usr/bin/env bash


if [ ! -d ./node_modules/ ]; then
  echo "installing dependencies"
  npm install

fi

node ./node_modules/@angular/cli/bin/ng serve --host 0.0.0.0 --port 8000 --disable-host-check
