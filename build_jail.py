#!/bin/python3
#Incomplete python script that does the same things but smarter
import time
import re
import subprocess

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
if yes_or_no("Does this username need to be created?"):
   print("This username is being passed to linux adduser please complete the the setup\n")
   time.sleep(4)
   subprocess.run(['sudo','adduser',username])

jail = '/home/' + username


commands = ['ls','bash','rsync']
print('\n\nWelcome to the chroot jail creator we have added ls, bash and rsync if you would like to add more please enter them below, one at a time and press enter when done')
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
tree = ['/bin','/usr','/lib','/lib64','/usr/bin','/lib/x86_64-linux-gnu','/lib64/x86_64-linux-gnu']
for i in tree:
   print(jail+i)
   subprocess.run(['sudo','mkdir',jail+i])


#Once the commands have been created then the library files are generated
