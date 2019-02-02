#!/bin/bash

export LANG=ja_JP.UTF-8

cd `dirname $0`
. ./myenv/bin/activate

function check_env {
    while [ "$1" != "" ]; do
        if [ ! -f $1 ]; then
            echo "$1 not found. exit"
            exit 1
        fi
        shift
    done
}


mkdir -p bin/img

check_env bin/demo bin/fontlist
check_env

python srv.py
