#!/usr/bin/bash

set -e

dnf install -y rpmlint

for i in /repo/*/*.spec
do
  rpmlint $i
done