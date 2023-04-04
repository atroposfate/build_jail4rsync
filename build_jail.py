#!/bin/python3
#Incomplete python script that does the same things but smarter

import re
import subprocess

#create a user and save the location of the jail to a variable
username = input("Please enter a username, the user will be put in the /home directory: ")
subprocess.call('adduser', username)
jail = '/home/' + username


commands = ['ls','bash','rsync']
print('Welcome to the chroot jail creator we have added ls, bash and rsync if you would like to add more please enter them below, one at a time and enter a blank')
print('Examples could be cp, rm etc..')

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

#testing code to make sure the commands are getting captured
for x in commands:
  print(x)

#Make the necessary directories (need to add some code here to check if the directory still exists)
tree = ['/bin','/usr','/lib','/lib64','/usr/bin']
for i in tree:
   subprocess.call('sudo mkdir', jail+i)


#Once the commands have been created then the library files are generated
