#!/usr/bin/env bash

# Update Packages
sudo apt update
sudo apt upgrade

# Install MySQL
sudo apt install mysql-server

# Check if MySQL was successfully installed by running
mysql --version

# Securing MySQL
sudo mysql_secure_installation

# Check if MySQL Service Is Running
sudo systemctl status mysql
