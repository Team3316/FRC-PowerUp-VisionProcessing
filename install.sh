#!/bin/sh
local_path=$(pwd)'/vision.service'
systemd_path='/etc/systemd/system/vision.service'

if [ ! -f $local_path ]; then
	echo " [!] Local file missing. Aborting."
	exit
fi

if [ -L $systemd_path ]; then
	echo " [-] Link exists. Overwriting."
	sudo rm $systemd_path
fi

echo " [+] Linking service file."
sudo ln -s $local_path $systemd_path

echo " [+] Reloading systemd daemons"
sudo systemctl daemon-reload
