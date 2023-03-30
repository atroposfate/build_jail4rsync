#!/bin/bash
#Builds and setups an rsync jail with limited user access. Ability to log in and run rsync, ls
#Must change the variables based on your setup
#The root user generates backup files through a cron job and the user below connects to the Jailed folder and a seperate server connects and runs rsync to pull the data


#script assumes you have already created a user (in this case named) mybackup and is the home directory
JAIL=/home/mybackups
USER=mybackups

sudo mkdir $JAIL/usr $JAIL/bin $JAIL/lib $JAIL/lib64
sudo mkdir $JAIL/lib/x86_64-linux-gnu $JAIL/lib64/x86_64-linux-gnu
sudo mkdir $JAIL/usr/bin

sudo cp $(which ls) $JAIL/bin
sudo cp $(which bash) $JAIL/bin
sudo cp $(which rsync) $JAIL/usr/bin

#Add Libraries
sudo cp /lib/x86_64-linux-gnu/libtinfo.so.6 $JAIL/lib/x86_64-linux-gnu/
sudo cp /lib/x86_64-linux-gnu/libdl.so.2 $JAIL/lib/x86_64-linux-gnu/
sudo cp /lib/x86_64-linux-gnu/libc.so.6 $JAIL/lib/x86_64-linux-gnu/
sudo cp /lib64/ld-linux-x86-64.so.2 $JAIL/lib64

sudo cp /lib/x86_64-linux-gnu/libselinux.so.1 $JAIL/lib/x86_64-linux-gnu/
sudo cp /lib/x86_64-linux-gnu/libc.so.6 $JAIL/lib/x86_64-linux-gnu/
sudo cp /lib/x86_64-linux-gnu/libpcre2-8.so.0 $JAIL/lib/x86_64-linux-gnu/
sudo cp /lib/x86_64-linux-gnu/libdl.so.2 $JAIL/lib/x86_64-linux-gnu/
sudo cp /lib/x86_64-linux-gnu/libpthread.so.0 $JAIL/lib/x86_64-linux-gnu/

sudo cp /lib/x86_64-linux-gnu/libacl.so.1 $JAIL/lib/x86_64-linux-gnu/
sudo cp /lib/x86_64-linux-gnu/libz.so.1 $JAIL/lib/x86_64-linux-gnu/
sudo cp /lib/x86_64-linux-gnu/libpopt.so.0 $JAIL/lib/x86_64-linux-gnu/
sudo cp /lib/x86_64-linux-gnu/liblz4.so.1 $JAIL/lib/x86_64-linux-gnu/
sudo cp /lib/x86_64-linux-gnu/libzstd.so.1 $JAIL/lib/x86_64-linux-gnu/
sudo cp /lib/x86_64-linux-gnu/libxxhash.so.0 $JAIL/lib/x86_64-linux-gnu/
sudo cp /lib/x86_64-linux-gnu/libcrypto.so.1.1 $JAIL/lib/x86_64-linux-gnu/
sudo cp /lib/x86_64-linux-gnu/libc.so.6 $JAIL/lib/x86_64-linux-gnu/
sudo cp /lib/x86_64-linux-gnu/libdl.so.2 $JAIL/lib/x86_64-linux-gnu/
sudo cp /lib/x86_64-linux-gnu/libpthread.so.0 $JAIL/lib/x86_64-linux-gnu/

sudo chown root:root $JAIL

#Need to add the following lines (replacing the variables with the names) to sshd_config and restart. If I was smarter probably better to append this in the script
#Match User $USER
#ChrootDirectory $JAIL
