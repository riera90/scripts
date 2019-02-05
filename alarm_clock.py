#!/usr/bin/python3

''''
author Diego Rodríguez Riera
from https://github.com/riera90/scripts
licenced under BSD 3-Clause License
date 31/01/19


This is my personal alarm clock, it calculates at what time i have to wake up
from from my class and method of transport timetables (train in my case)
yeah, I'm lazy...
'''


from datetime import datetime, timedelta
import json
import time
from pygame import mixer
import codecs
import RPi.GPIO as GPIO

################################################################################
############################### Configuration ##################################
################################################################################

max_time_to_wake_up = timedelta(minutes=10)
time_from_wake_up_to_ready = timedelta(minutes=30)
time_from_home_to_station = timedelta(minutes=15)

time_from_station_to_station = timedelta(minutes=7)
time_from_Station_to_class = timedelta(minutes=7)

repeat_alarm_after = timedelta(minutes=5)

################################################################################
########################### end of Configuration ###############################
################################################################################

# max_time_to_wake_up = timedelta(seconds=10)
# time_from_wake_up_to_ready = timedelta(seconds=10)
# time_from_home_to_station = timedelta(seconds=2)
# 
# time_from_station_to_station = timedelta(seconds=2)
# time_from_Station_to_class = timedelta(seconds=2)
# 
# repeat_alarm_after = timedelta(seconds=5)

'''
the alarm status can be:
	armed: tha alarm is ready to wake up
	waking_up: the alarm is waking you up
	preparing: the alarm is waiting to get the yo out signal
	disarmed: the alarm has done it's job
'''

def time_plus(time, timedelta):
    dummy_date = datetime.today()
    full_datetime = datetime.combine(dummy_date, time)
    added_datetime = full_datetime + timedelta
    return added_datetime.time()


def time_minus(time, timedelta):
    dummy_date = datetime.today()
    full_datetime = datetime.combine(dummy_date, time)
    added_datetime = full_datetime - timedelta
    return added_datetime.time()


def get_first_class_at(day):
	actual_day = str(day)
	horario = codecs.open('./horario.json', 'r','UTF-8')
	horario = json.load(horario)['calendar']
	horario = horario[actual_day]
	min_class = None
	for clas in horario:
		if min_class is None:
			min_class = datetime.strptime(clas, "%H:%M:%S").time()
		if (datetime.strptime(clas, "%H:%M:%S").time() < min_class):
			min_class = datetime.strptime(clas, "%X").time()
			
	return min_class


def calculate_train(class_time):
	
	trains = codecs.open('./trains.json', 'r','UTF-8')
	trains = json.load(trains)['Cordoba-Rabanales']
	
	if (int(datetime.today().weekday()) < 5):
		trains = trains['entreSemana']
	else:
		trains = trains['finDeSemana']
	
	delta = time_from_station_to_station + time_from_Station_to_class
	latest_train_ok = None
	for train in trains:
		train = datetime.strptime(train, "%H:%M:%S").time()
		if latest_train_ok is None:
			if class_time >= time_plus(train, delta):
				latest_train_ok = train
		if (train > latest_train_ok):
			if class_time >= time_plus(train, delta):
				latest_train_ok = train
	return latest_train_ok


def calculate_wake_up(train):
	delta = time_from_home_to_station + time_from_wake_up_to_ready
	return time_minus(train, delta)


def calculate_go_out(train):
	return time_minus(train, time_from_home_to_station)


def calculate_first_alarm(train):
	delta = time_from_home_to_station + time_from_wake_up_to_ready + max_time_to_wake_up
	return time_minus(train, delta)
	

def ring_alarm(sound, timeout):
	max_time = time_plus(datetime.now().time(), timeout)
	ringing = True
	ret_val = False
	mixer.init()
	mixer.music.load(sound)
	mixer.music.play()
	while( (max_time > datetime.now().time()) and (ringing) ):
		#ringing=False
		#ret_val=True
		time.sleep(0.1)
		if GPIO.input(8) == GPIO.HIGH:
			ringing = False
			i = 0
			while GPIO.input(8) == GPIO.HIGH:
				i = i + 1
				time.sleep(0.1)
			if i > 15:
				ret_val = True
	
	mixer.music.stop()
	if ret_val:
		print("stoping")
	else:
		print("pausing")
	return ret_val



def main():
	GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
	GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

	alarm_status = "armed"
	actual_time = datetime.now().time()
	today = datetime.today().weekday()
	
	# train = time_plus(actual_time, timedelta(minutes=55)) #TODO delete this
	
	train = calculate_train(get_first_class_at(int(datetime.today().weekday())))
	
	first_alarm_time = calculate_first_alarm(train)
	wake_up_time = calculate_wake_up(train)
	go_out_time = calculate_go_out(train)
	
	next_alarm = first_alarm_time
	
	print("train:",train)
	print("go out:",go_out_time)
	print("wake up:",wake_up_time)
	print("first alarm:",first_alarm_time)
	
	while True:
		
		print(alarm_status, actual_time,"untill",next_alarm)
		
		if alarm_status is "disarmed":
			time.sleep(60)
		else:
			time.sleep(5)
			
		
		actual_time = datetime.now().time()
		
		
		if alarm_status is "armed":#the alarm is ready for fucking up your sleep
			if(actual_time > first_alarm_time):#woops is fking ur sleep already!
				print("get up lazy")
				#not enought time to ring alarm
				if(wake_up_time < time_plus(actual_time,repeat_alarm_after)):
					delta = timedelta(minutes=wake_up_time.minute-actual_time.minute)
					print("ringing shorter alarm!")
					ring_alarm('sound.flac', delta)
					alarm_status = "waking_up"
					next_alarm = wake_up_time
					
				else:#ring the alarm
					print("ringing alarm!")
					if (ring_alarm('bittersweet.mp3', repeat_alarm_after)):
						alarm_status = "waking_up"
						next_alarm = wake_up_time
					else:
						if(wake_up_time > time_plus(actual_time,repeat_alarm_after)):
							print("waiting")
							time.sleep(60*5)
	
		
		
		
		elif alarm_status is "waking_up":#currently fucking up your sleep
			if(actual_time > wake_up_time):
				print("ok, now you have to get up")
				#not enought time to ring alarm
				if(go_out_time < time_plus(actual_time,repeat_alarm_after)):
					delta = timedelta(minutes=wake_up_time.minute-actual_time.minute)
					print("ringing shorter alarm!")
					ring_alarm('sound.flac', delta)
					alarm_status = "preparing"
					next_alarm = go_out_time
					
				else:#ring the alarm
					print("ringing alarm!")
					if (ring_alarm('sound.flac', repeat_alarm_after)):
						alarm_status = "preparing"
						next_alarm = go_out_time
					else:
						if(go_out_time > time_plus(actual_time,repeat_alarm_after)):
							print("waiting")
							time.sleep(60*5)
			
		
		
		
		elif alarm_status is "preparing":#fucking up your coffee
			if(actual_time > go_out_time):
				print("you beter be prepared")
				print("ringing alarm!")
				ring_alarm('hector.mp3', timedelta(seconds=5))
				alarm_status = "disarmed"
		
		
		
		elif alarm_status is "disarmed":#your sleep has been fckd up succesfully
			if today is not datetime.today().weekday():
				print("reseting alarm")
				today = datetime.today().weekday()
				train = calculate_train(get_first_class_at(int(datetime.today().weekday())))
				alarm_status = "armed"
				
		
		
		
		
		
		


if __name__ == "__main__":
	main()


