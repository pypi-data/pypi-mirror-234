#!/bin/bash

usage() { echo "Usage: $0 [-c <config_file>]" 1>&2; exit 1; }

while getopts ":c:d:" o; do
    case "${o}" in
        c)
            c=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z "${c}" ]; then
    usage
fi

litenchat=`which litenchat.py`
echo "litenchat = ${litenchat} config_file = ${c}"

panel serve ${litenchat} --autoreload --show --args ${c}

