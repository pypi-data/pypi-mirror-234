#!/bin/bash

#pythonpath=$PYTHONPATH

pythonpath=$1
action=$2
port=$3

echo 'pythonpath is' $pythonpath
echo 'action is' $action
echo 'port is' $port
if [ $action == 'start' ]
    then
    echo 'starting start'
    if [[ -z "$port" ]]
        then
        port=9999
        echo 'default port is' $port
    fi
    python $pythonpath runserver $port --settings=PromptManager.settings.dev
    echo 'starting end'
else
    echo 'stopping start'
    kill $(ps aux | grep 'manage.py runserver' | awk '{print $2}')
    echo 'stopping end'
fi

