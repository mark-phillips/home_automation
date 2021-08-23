#!/bin/bash

#
# Work out lcoation of script source
#
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

download=1
#
function usage
{
  echo 
  echo "Usage:"
  echo "  $(basename $0)  [-n|--no_download]  [-f|--full_update] [-h|--help] version"
  echo "Where:"
  echo "  no_download = Using previously downloaded archive"
  echo "  full_update = Update all files instead of just license"
  echo "  version = Version to download"
  echo
}

function process_args
{
  usage_error=0
  while [[ $# -gt 0 ]]
  do
		key="$1"

		case $key in
			"-?"|-h|--help)
				usage
				exit
				shift
				;;
			-f|--full_update)
				full_update=1
				shift
				;;
			-n|--no_download)
				download=0
				shift
				;;
			*)
				version=$1 
				shift
				;;
		esac
  done
  if [ -z ${version} ]; then
    echo "Error: You must specify the version to download."
    usage_error=1
  fi
  if [ ${usage_error} -eq 1 ]; then
    usage
    exit 1
  fi
}
#
# Process arguments
#
process_args $@

filename=mmonit-${version}-linux-arm32.tar.gz 
cd ~/bin
if [ `pwd` != ~/bin ]; then 
  echo "Failed to switch to "~/bin" directory" 
  exit 3 
fi


if [ "${download}" == "1" ]; then 
	curl  https://mmonit.com/dist/${filename} -O
	if [ ! -f  ~/bin/${filename} ]; then 
		echo "Failed to download ${version}"
		exit 2 
	fi
fi

if [ "${full_update}" == "1" ]; then 
  echo ...unpacking complete archive 
  tar  -xzvf ${filename}  > /dev/null
  if [ $? -ne 0 ]; then
    echo Error - unpack failed.
    rm ~/bin/${filename}
    exit 4
  fi
  echo ...linking  ~/bin/mmonit-${version} to /usr/local/mmonit
  sudo rm /usr/local/mmonit
  sudo ln -sf ~/bin/mmonit-${version} /usr/local/mmonit
else
  echo ...unpacking license
  tar --wildcards -xzvf ${filename} "mmonit-*/conf/license.xml" > /dev/null
  if [ $? -ne 0 ]; then
    echo Error - unpack failed.
    rm ~/bin/${filename}
    exit 4
  fi
fi

echo ...restarting mmonit
sudo monit restart mmonit
