#!/bin/bash

if [ -z "$1" ]; then 
  echo "Error: "
  echo "Usage: $0 command"
  exit
fi

for host in home pi-zero1 status landing fileserver 
do
	echo
  echo "Running on ${host}"
  echo "===================================================="
  echo "$ $@"
  ssh ${host} "$@"
  echo "===================================================="
done
