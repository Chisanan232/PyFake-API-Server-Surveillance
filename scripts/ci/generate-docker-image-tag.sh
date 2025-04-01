#!/usr/bin/env bash

#####################################################################################################################
#
# Target:
# Automate to get the software version of Python package and generate as the specific format for Docker image tag.
#
# Description:
# Use the version regex to get the software version of Python package, and output, re-generate docker version info from it.
#
# Allowable options:
#  -r [Release type]              Release type of project. Different release type it would get different version format. [options: python-package]
#  -p [Python package name]       The Python package name. It will use this naming to get the package info module (__pkg_info__.py) to get the version info.
#  -v [Version format]            Which version format you should use. [options: general-2, general-3, date-based]
#  -d [Run mode]                  Running mode. Set 'dry-run' or 'debug' to let it only show log message without exactly working. [options: general, dry-run, debug]
#  -h [Argument]                  Show this help. You could set a specific argument naming to show the option usage. Empty or 'all' would show all arguments usage. [options: r, p, v, i, d, h]
#
#####################################################################################################################

show_help() {
    echo "Shell script usage: bash ./scripts/ci/generate-docker-image-tag.sh [OPTION] [VALUE]"
    echo " "
    echo "This is a shell script for generating tag by software version which be recorded in package info module (__pkg_info__) from Python package for building Docker image."
    echo " "
    echo "options:"
    if [ "$OPTARG" == "r" ] || [ "$OPTARG" == "h" ] || [ "$OPTARG" == "all" ]; then
        echo "  -r [Release type]              Release type of project. Different release type it would get different version format. [options: python-package]"
    fi
    if [ "$OPTARG" == "p" ] || [ "$OPTARG" == "h" ] || [ "$OPTARG" == "all" ]; then
        echo "  -p [Python package name]       The Python package name. It will use this naming to get the package info module (__pkg_info__.py) to get the version info."
    fi
    if [ "$OPTARG" == "v" ] || [ "$OPTARG" == "h" ] || [ "$OPTARG" == "all" ]; then
        echo "  -v [Version format]            Which version format you should use. [options: general-2, general-3, date-based]"
    fi
    echo "  -h [Argument]                  Show this help. You could set a specific argument naming to show the option usage. Empty or 'all' would show all arguments usage. [options: r, p, v, d]"
}

# Show help if no arguments provided
if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

# Handle arguments
if [ $# -gt 0 ]; then
    case "$1" in
        -h|--help)    # Help for display all usage of each arguments
            show_help
            exit 0
            ;;
    esac
fi

while getopts "r:p:v:d:?" argv
do
     case $argv in
         "r")    # Release type
           Input_Arg_Release_Type=$OPTARG
           ;;
         "p")    # Python package name
           Input_Arg_Python_Pkg_Name=$OPTARG
           ;;
         "v")    # Software version format
           Input_Arg_Software_Version_Format=$OPTARG
           ;;
         "d")    # Dry run
           Running_Mode=$OPTARG
           ;;
         ?)
           echo "Invalid command line argument. Please use option *h* to get more details of argument usage."
           exit
           ;;
     esac
done

New_Release_Version=$(bash ./scripts/ci/generate-software-version.sh -r "$Input_Arg_Release_Type" -p "$Input_Arg_Python_Pkg_Name" -v "$Input_Arg_Software_Version_Format" -d "$Running_Mode")
echo "v$New_Release_Version"
