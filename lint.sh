#!/usr/bin/bash

set -e

for i in /repo/*/*.spec; do
  rpmlint "$i"
done

shellcheck /repo/**.sh
