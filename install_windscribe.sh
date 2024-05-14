#!/bin/bash

# Set the username/email and password
username="metaaaaaaaa"
password="uHAry1gk23XZ"
echo "0000" | sudo -S apt-get install expect -y
# expect -c "spawn windscribe login expect \"Username:\" send \"$username\r\" expect \"Password:\" send \"$password\r\" expect eof"
expect -c " 
spawn windscribe login
expect \"Username:\"
send \"metaaaaaaaa\r\"
expect \"Password:\"
send \"uHAry1gk23XZ\r\"
expect eof
"