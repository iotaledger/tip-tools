#!/bin/bash

## Functions
_bold=$(tput bold)
_reset=$(tput sgr0)

_red=$(tput setaf 1)
_green=$(tput setaf 2)

function print_ok   { printf "${_bold}${_green}%s${_reset}\n" "$@"; }
function print_err  { printf "${_bold}${_red}%s${_reset}\n" "$@"; }

print_ok "Updating Packages..."
sudo apt update

print_ok "Installing packages for Python3 virtual environment..."
sudo apt install -y virtualenv python3-dev python3-pip python3-virtualenv python3-venv

print_ok "Creating python virtual environment..."
python3 -m venv .pyenv
. .pyenv/bin/activate
pip install setuptools --upgrade
pip install wheel
pip install -r requirements.txt
print_ok "Creating python virtual environment done!"
