#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:'coSMIC_AccelerationLogging.py'
==================
Created by dmatthes1982 <dmatthes@cbs.mpg.de>
Created on 2018-04-10
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import time
from coSMIC_SensDataSaving import SensDataSaving

from pymetawear.client import MetaWearClient

address1 = 'E3:53:A4:26:93:0F'
address2 = 'F4:94:79:03:D2:93'

useTwoClients = True

client1 = MetaWearClient(str(address1), debug=True)
print("New client created: {0}".format(client1))

if useTwoClients:
	client2 = MetaWearClient(str(address2), debug=True)
	print("New client created: {0} \n".format(client2))

print("Get possible accelerometer settings of client 1...")
settings = client1.accelerometer.get_possible_settings()
print(settings)

if useTwoClients:
	print("Get possible accelerometer settings of client 2...")
	settings = client2.accelerometer.get_possible_settings()
	print(settings)

time.sleep(1.0)

print("\nWrite accelerometer settings...")
client1.accelerometer.set_settings(data_rate=400, data_range=4.0)
if useTwoClients:
	client2.accelerometer.set_settings(data_rate=400, data_range=4.0)

time.sleep(1.0)

print("\nCheck accelerometer settings of client 1...")
settings = client1.accelerometer.get_current_settings()
print(settings)

if useTwoClients:
	print("Check accelerometer settings of client 2...")
	settings = client2.accelerometer.get_current_settings()
	print(settings)


client1.accelerometer.logging = True
if useTwoClients:
	client2.accelerometer.logging = True

client1.accelerometer.start_logging()
if useTwoClients:
	client2.accelerometer.start_logging()
print("\nLogging...")

#prompt = "\nPress q and Enter to quit logging...\n\n" 
#message = "" 
#while message != 'q': 
#    message = raw_input(prompt) 

time.sleep(0.25)
print("Logging stopped.")

filename1 = 'sensor1.cvs'
filename2 = 'sensor2.cvs'
sens1 = SensDataSaving(filename1)
if useTwoClients:
	sens2 = SensDataSaving(filename2)

print("\nDownloading Data...")
client1.accelerometer.download_log(lambda data : sens1.download_callback(data, filename1))
if useTwoClients:
	client2.accelerometer.download_log(lambda data : sens2.download_callback(data, filename2))

time.sleep(5.0)

sens1.close_csv()
if useTwoClients:
        sens2.close_csv

print("\nDisconnecting...")
client1.disconnect()
if useTwoClients:
	client2.disconnect()

