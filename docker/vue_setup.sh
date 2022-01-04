#!/usr/bin/env bash

set -xue

yarn install
yarn serve --host 0.0.0.0
