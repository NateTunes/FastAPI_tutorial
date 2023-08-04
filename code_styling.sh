#!/usr/bin/env sh

code_style(){
    echo "Executing black on $1 :"
    black $1 --config .codestyle.conf
    echo "Executing isort on $1 :"
    isort $1 
    echo "Executing flake8 on $1 :"
    flake8 $1 --config .flake8
}

for var in "$@"
do
    echo "Start code styling: $var"
    code_style $var
    echo "Done code styling: $var"
done
