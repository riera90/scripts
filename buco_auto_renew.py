#!/usr/bin/python3

# author Diego Rodríguez Riera
# from https://github.com/riera90/scripts
# licenced under BSD 3-Clause License
# date 18/02/19

# auto book renewer for the uco's library (BUCO)


import requests
import re
import os


################################################################################
############################### Configuration ##################################
################################################################################
target_login = "https://medina.uco.es/patroninfo"
# target_renew = "https://medina.uco.es/patroninfo~S6*spi"
user = "i62rorid"
password = "asdasdasasd"

login_html = "login"
password_html = "password"
# target username and password input
################################################################################
########################### end of Configuration ###############################
################################################################################

# this function tests a series of passwords
def renew():
# creates the session (mainly to store cookies)
    bot = requests.session()

    form = {login_html:user,
    password_html:password}
    # makes the post
    response = bot.post(url = target_login, data = form)

    print("\tstatus_code      -->", response.status_code)
    print("\tresponse.history -->", response.history)
    print("\tredirected to    -->",response.url)

    # if the seession is redirected, we got the good password
    if response.url == target_login:
        print("Error!, login could not be made")
        # os._exit(1)

    print("succesfull login")

    # print(target_renew)





renew()
