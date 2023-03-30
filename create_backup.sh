#!/bin/bash

#Assumed a user is created already named mybackups and there is a folder in the home directory called mybackups.
#this is run as a cron job as root to back up to the necessary folder and put is somewhere safe to be pulled from


DATE=$(date '+%F')
USER=mybackups
JAIL=/home/mybackups/backup

#this is for the mail server but the host name can be changed, initial line checks for old files and deletes them so they don't just pile up on the remote system
find $JAIL -type f -name 'MailServer_var-*.tar.gz' -mtime +15 -exec rm {} \;
#In this example creating seperate files backed for the key folders
#Could be changed to a simplier "tar -czvf $JAIL/MailServer-$DATE.tar.gz /etc/ /var/ if you want to keep it all in one file
tar -czvf $JAIL/MailServer_etc-$DATE.tar.gz /etc/
tar -czvf $JAIL/MailServer_var-$DATE.tar.gz /var/
chown -R $USER:$USER $JAIL
