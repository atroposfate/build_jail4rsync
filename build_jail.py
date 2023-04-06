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

#create a user and save the location of the jail to a variable
username = input("Please enter a username, the user will be put in the /home directory: ")

if yes_or_no("Does this user need to be created?"):
   print("This username is being passed to linux adduser please complete the the setup\n")
   time.sleep(4)
   subprocess.run(['adduser',username])

jail = '/home/' + username

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
tree = ['/bin','sbin','/usr','/lib','/lib64','/usr/bin','/lib/x86_64-linux-gnu','/lib64/x86_64-linux-gnu','/usr/sbin/']
for i in tree:
   print(jail+i)
   subprocess.run(['mkdir',jail+i])


for x in commands:
   whr = subprocess.run(['which',x], capture_output=True, text=True).stdout.strip("\n")
   subprocess.run(['cp',whr,jail+whr])
   #determin all the libraries for these functions and isolate them in an array
   libtext = subprocess.run(['ldd',whr], capture_output=True, text=True).stdout.strip("\n")
   libfiles = re.findall(r"(\/.*?)(?=\s)", libtext)
   #once the libraries are identified then copy them into the jail
   for y in libfiles:
      subprocess.run(['cp',y,jail+y])

print("\nFiles needed for the chroot jail have been created in the necessary folders please note the errors as some files or libraries may not have copied successfully")

chtext = '\nMatch User ' + username+'\nChrootDirectory ' +jail

#Add the necessary data to the sshd file
if yes_or_no("You will need to add some lines to your sshd_config file for this to work, would you like me to do that?"):
   ssh_loc = input("Assuming the location is /etc/ssh/sshd_config, please provide alternate path if incorrect")
   if ssh_loc == '':
     ssh_loc='/etc/ssh/sshd_config'

   file_object = open(ssh_loc,'a')
   file_object.write(chtext)
   file_object.close()
   subprocess.run(['systemctl','restart','sshd'])
else:
   print("Don't forget to add the following to your sshd config file"+chtext)

print("\n\nDone!")
