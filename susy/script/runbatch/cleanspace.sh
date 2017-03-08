#!/bin/bash

# This script used to clean the space

if ls *job*sh
then
    echo "You want to clean all the files above? y/n"
    read decis

    if [ "$decis" == "y" ]
    then
        rm *job*sh
        echo "The files have been deleted!"
    else
        echo "Will keep them"
    fi

else
    echo "no *job*sh files to clean!"
fi

if ls *_log
then
    echo "You want to clean all the files/dir above? y/n"
    read decis

    if [ "$decis" == "y" ]
    then
        rm -r *_log
        echo "The files/dir have been deleted!"
    else
        echo "Will keep them"
    fi

else
    echo "no *_log files/dir to clean!"
fi



exit

