#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:'coSMIC_MotionDetection'
==================
Created by dmatthes1982 <dmatthes@cbs.mpg.de>
Created on 2018-04-10
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from coSMIC_SensDataProc import SensDataProc
import parallel
import time

from pymetawear.client import MetaWearClient

address1 = 'E3:53:A4:26:93:0F'
address2 = 'F4:94:79:03:D2:93'

useTwoClients = True

client1 = MetaWearClient(str(address1), debug=False)
print("New client created: {0}".format(client1))

if useTwoClients:
	client2 = MetaWearClient(str(address2), debug=False)
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
client1.accelerometer.set_settings(data_rate=25, data_range=4.0)
if useTwoClients:
	client2.accelerometer.set_settings(data_rate=25, data_range=4.0)

time.sleep(1.0)

print("\nCheck accelerometer settings of client 1...")
settings = client1.accelerometer.get_current_settings()
print(settings)

if useTwoClients:
	print("Check accelerometer settings of client 2...")
	settings = client2.accelerometer.get_current_settings()
	print(settings)

parPort = parallel.Parallel()
sens1 = SensDataProc(parPort)
if useTwoClients:
	sens2 = SensDataProc(parPort)

print("\nSubscribing to accelerometer signal notifications...")
client1.accelerometer.high_frequency_stream = False
if useTwoClients:
	client2.accelerometer.high_frequency_stream = False

client1.accelerometer.notifications(lambda data : sens1.dataProcessing(data, 1))
if useTwoClients:
	client2.accelerometer.notifications(lambda data : sens2.dataProcessing(data, 2))

prompt = "\nPress q and Enter to quit the programm...\n\n" 
message = "" 
while message != 'q': 
    message = raw_input(prompt) 

print("Unsubscribe to notification...")
client1.accelerometer.notifications(None)
if useTwoClients:
	client2.accelerometer.notifications(None)

time.sleep(5.0)

client1.disconnect()
if useTwoClients:
	client2.disconnect()

