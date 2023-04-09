#!/bin/python3

#Script to generate a jail for a user and create all the necessary files. This is provided without waranty or guaranty and use at your own riskkkkkk
import os
import time
import re
import subprocess

#Script must be run as root
if os.geteuid() != 0:
   print("This script must be run as root please retry with sudo in front")
   quit()

#yes no prompt
def yes_or_no(question):
      reply = str(input(question+' [Y/n]: ')).lower().strip()
      try: 
        if reply[:1] == 'y' or reply == "":
            return True
        if reply[:1] == 'n':
            return False
        else:
           print('Invalid Input')
           return  yes_or_no(question)
      except Exception as error:
         print("Please enter valid input")
         print(error)
         return yes_or_no(question)

#more consice ssh work 
def ssh_conf(sshloc,uname,jailing):
     if yes_or_no("Would you like to add the user to the sshd file?"):
        chtext = '\nMatch User ' + uname+'\nChrootDirectory ' +jailing +"\n"
        if yes_or_no("Is your sshd file located in "+sshloc):
          pass
        else:
          sshloc=input("Please provide the full path for the file: ")
        try:
          file_object = open(sshloc,'a')

        except FileNotFound as error:
          print("File Not Found at " + sshloc+", it will start over" )
          print(error)
          return ssh_conf(sshloc,uname,jailing)

        file_object.write(chtext)
        file_object.close()
        subprocess.run(['systemctl','restart','sshd'])
     else:
        print("\nDon't forget to add the user to you sshd file")

#create all the directories and permissions
def createdir(jailing,uname):
   tree = ['/bin','/sbin','/usr','/lib','/lib64','/usr/bin','/lib/x86_64-linux-gnu','/lib64/x86_64-linux-gnu','/usr/sbin','/root','/backups']
   print("These directories are created: ")
   for i in tree:
     print(jailing+i)
     subprocess.run(['mkdir',jailing+i])
#setup the permissions for the folders
   subprocess.run(['cp','/bin/bash',jailing+'/bin/'])
   subprocess.run(['chown',uname+':'+uname,jailing+'/root',jailing+'/backups'])

def getlibs(program):
   #determin all the libraries for these functions and isolate them in an array
   libtext = subprocess.run(['ldd',program], capture_output=True, text=True).stdout.strip("\n")
   libfiles = re.findall(r"(\/.*?)(?=\s)", libtext)
   return libfiles

#want to tidy up the create user and avoid the uncessary adduser and user useradd
def createuser(uname):
   subprocess.run(['useradd','-m','/home/'+uname,'-p',input("Enter new password"),'-s','/bin/bash',uname])


#create a user and save the location of the jail to a variable0
username = input("Please enter a username, the user will be put in the /home directory: ")

if yes_or_no("Does this user need to be created?"):
   print("This username is being passed to linux adduser please complete the the setup\n")
   time.sleep(4)
   subprocess.run(['adduser',username])

jail = '/home/' + username
#Need this to be done so the chroot works
subprocess.run(['chown','root:root',jail])

#Pre determined commands for the jail but additional can be added
commands = ['ls','bash','rsync']
print('\n\nWelcome to the chroot jail creator we have added ls, bash and rsync if you would like to add more please enter them below, one at a time and press enter when done\n Examples could be cp, rm etc')

while True:
   newcommand = input("Enter an additional application, press enter when done: ")
   if newcommand == "":
      #once we get a return without data then exit and execute the building of the jail
      break
   else:
   	#Check for a space and kick it back
     if bool(re.search(r"\s", newcommand)):
       print("Looks like the string contains a space and is unepected please try again")
       continue
     else:
     #if everything passes then add the command to the array
       commands.append(newcommand)

#Make the necessary directories. Some of these are overkill and often not used but better safe than sorry
createdir(jail,username)

#get all the dependancies
for x in commands:
   whr = subprocess.run(['which',x], capture_output=True, text=True).stdout.strip("\n")
   subprocess.run(['cp',whr,jail+whr])
   libfiles = getlibs(whr)
   for y in libfiles:
      subprocess.run(['cp',y,jail+y])

print("\nFiles needed for the chroot jail have been created in the necessary folders please note the errors as some files or libraries may not have copied successfully")


#Add the necessary data to the sshd file
ssh_conf("/etc/ssh/sshd_config",username,jail)

print("\n\nDone!\nBy default you will only be able to write to /root and /backups folder")
