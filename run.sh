#!/bin/bash

export LANG=ja_JP.UTF-8

cd `dirname $0`
. ./myenv/bin/activate 

python srv.py
