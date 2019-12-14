#!/bin/bash

command=$1
env=$2
worker=$3

function rep_ok(){
    echo -e '\e[32m'$1'\e[m'
}
function rep_warn(){
    echo -e '\e[1;33mWARNING: '$1'\e[m'
}
function rep_die(){
    echo -e '\e[1;31mERROR: '$1'\e[m'
    exit
}


function export_env(){
    export APP_HOST=0.0.0.0
    export APP_PORT=5002
    export APP_RELEASE=ADRINI_IOT
    export APP_CREATED=ADRINI
    export FLASK_DEBUG=True

    export DB_DRIVER=mysql
    export MYSQL_DB=billing
    export MYSQL_HOST=192.168.3.10
    export MYSQL_USER=billing
    export MYSQL_PASSWORD=adrini@BILLING

    export APP_REDIS_URL=redis://:pass@session:6379/0
    export SECRET_KEY=asdsagdasgdasf@asfdasgvdasda@
    export NINJA_TOKEN=qg5ncpfctdqz3h9hagwogadhcrk6vcsl
    export NINJA_HOST=192.168.3.11
    export NINJA_API_VERSION=v1
}

function run_gunicorn(){
    apphost=$1
    port=$2
    worker=$3
    if [[ -z $1 ]]; then
        rep_warn "Using Default Host"
        apphost=localhost
    fi

    if [[ -z $2 ]]; then
        rep_warn "Using Default Port"
        port=5000
    fi

    if [[ -z $3 ]]; then
        rep_warn "Using Default Worker"
        worker=2
    fi
    gunicorn production:app -b $apphost:$port -w $worker
}


if [ $command = 'server' ]
    then
    if [ $env = 'production' ]
        then
        rep_ok 'STARTING | SERVER'
        run_gunicorn $APP_HOST $APP_PORT $worker

    elif [ $env = 'staging' ]
        then
        rep_ok 'STARTING | SERVER'
        python3 manage.py server
    elif [ $env = 'development' ]
        then
        rep_warn "EXPORTING VARIABLE ENVIRONMENT"
        export_env
        rep_ok "EXPORTING VARIABLE ENVIRONMENT"
        echo ""
        rep_ok 'STARTING | SERVER'
        python manage.py server
    else
        rep_die '[env] : production | development'
    fi
else
    rep_die 'USAGE : ./run.sh server [env].'
fi

