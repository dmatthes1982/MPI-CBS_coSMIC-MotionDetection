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
import parallel
from coSMIC_SensDataSaving import SensDataSaving

from pymetawear.client import MetaWearClient
from pymetawear.exceptions import PyMetaWearException, PyMetaWearDownloadTimeout

address1 = 'E3:53:A4:26:93:0F'
address2 = 'F4:94:79:03:D2:93'

useTwoClients = True

'''
Subfunction: Reconnect client
'''
def bt_reconnect(client):
        bt_disconnect(client)
        try:
                bt_connect(client)
        except RuntimeError as e:
                raise e
        time.sleep(0.5)

'''
Subfunction: Connect client
'''
def bt_connect(client):
        time.sleep(0.5)
        try:
                client.mw.connect()
        except RuntimeError as e:
                raise e

'''
Subfunction: Disconnect client
'''
def bt_disconnect(client):
        time.sleep(0.5)
        client.mw.disconnect()

'''
Establish connections
'''
try:
        client1 = MetaWearClient(str(address1), debug=False)
except RuntimeError as e:
        print(e)
        quit()

print("New client created: {0}".format(client1))

if useTwoClients:
	try:
	        client2 = MetaWearClient(str(address2), debug=False)
	except RuntimeError as e:
                print(e)
                client1.disconnect()
                quit()
	print("New client created: {0} \n".format(client2))

'''
Get accelerometer settings
'''

print("Get possible accelerometer settings of client 1...")
settings = client1.accelerometer.get_possible_settings()
print(settings)

time.sleep(1.0)

if useTwoClients:
	print("Get possible accelerometer settings of client 2...")
	settings = client2.accelerometer.get_possible_settings()
	print(settings)

        time.sleep(1.0)

'''
Set accelerometer settings
'''

print("\nWrite accelerometer settings...")
client1.accelerometer.set_settings(data_rate=400, data_range=4.0)

time.sleep(1.0)

if useTwoClients:
	client2.accelerometer.set_settings(data_rate=400, data_range=4.0)

client1.accelerometer.high_frequency_stream = False
client2.accelerometer.high_frequency_stream = False

parPort = parallel.Parallel()

time.sleep(1.0)

'''
Start logging accelerometer data
'''

logging_started = False
attempt = 1
while not logging_started:
        try:
                client1.accelerometer.start_logging()
        except PyMetaWearException as inst:
                print(inst)
                attempt += 1
                if attempt == 4:
                        break
                print("Reconnecting, try number {0}...".format(attempt))
                try:
                        bt_reconnect(client1)
                except RuntimeError as e:
                        print(e)
                        bt_disconnect(client2)
                        quit()
        else:
                print("\nLogging accelerometer data at client 1...")
                parPort.setData(0x64)
                print("Client 1 startet - 0x64 send\n")
                time.sleep(0.05)
                parPort.setData(0x00)
                logging_started = True


if not logging_started:
        client1.disconnect()
        client2.disconnect()
        quit()

time.sleep(1.0)

logging_started = False
attempt = 1
if useTwoClients:
        while not logging_started:
                try:
                        client2.accelerometer.start_logging()
                except PyMetaWearException as inst:
                        print(inst)
                        attempt += 1
                        if attempt == 4:
                                break
                        print("Reconnecting, try number {0}...".format(attempt))
                        try:
                                bt_reconnect(client2)
                        except RuntimeError as e:
                                print(e)
                                bt_disconnect(client1)
                                quit()
                else:
                        print("Logging accelerometer data at client 2...")
                        parPort.setData(0x66)
                        print("Client 2 startet - 0x66 send\n")
                        time.sleep(0.05)
                        parPort.setData(0x00)
                        logging_started = True

        if not logging_started:
                client1.accelerometer.stop_logging()
                client1.disconnect()
                client2.disconnect()
                quit()

        time.sleep(1.0)

'''
Check accelerometer settings
'''

print("Check accelerometer settings of client 1...")
settings = client1.accelerometer.get_current_settings()
print(settings)

time.sleep(1.0)

if useTwoClients:
	print("Check accelerometer settings of client 2...")
	settings = client2.accelerometer.get_current_settings()
	print(settings)

time.sleep(1.0)

'''
Disconnect all bluetooth connection during logging process
'''
print("\nDisconnect all bluetooth connections during the recording session\n")
bt_disconnect(client1)
bt_disconnect(client2)

'''
Waiting until q pressed
'''

prompt = "Press q and Enter to quit logging...\n\n"
message = ""
while message != 'q':
    message = raw_input(prompt)

'''
Reconnect with client 1
'''

try:
        print("\nConnecting with client 1...")
        bt_connect(client1)
except RuntimeError as e:
        print(e)
        quit()

'''
Stop logging accelerometer data in client 1
'''

client1.accelerometer.stop_logging()
print("Logging stopped at client 1.")
parPort.setData(0x65)
print("Client 1 stopped - 0x65 send")
time.sleep(0.05)
parPort.setData(0x00)

'''
Reconnect with client 2, disconnect client 1
'''

print("Disconnect client 1.")
bt_disconnect(client1)
try:
        print("\nConnecting with client 2...")
        bt_connect(client2)
except RuntimeError as e:
        print(e)
        quit()

'''
Stop logging accelerometer data in client 2
'''

if useTwoClients:
        client2.accelerometer.stop_logging()
        print("Logging stopped at client 2.")
        parPort.setData(0x67)
        print("Client 2 stopped - 0x67 send")
        time.sleep(0.05)
        parPort.setData(0x00)

'''
Disconnect client 2
'''
print("Disconnect client 2.")
bt_disconnect(client2)

'''
Download accelerometer data
'''

filename1 = 'sensor1.cvs'
filename2 = 'sensor2.cvs'
sens1 = SensDataSaving(filename1)
if useTwoClients:
	sens2 = SensDataSaving(filename2)

'''
Reconnect with client 1
'''
try:
        print("\nConnecting with client 1...")
        bt_connect(client1)
except RuntimeError as e:
        print(e)
        quit()

print("Downloading data from client 1...\n")
download_complete = False
attempt = 1
while not download_complete:
        try:
                data = client1.accelerometer.download_log()
        except PyMetaWearDownloadTimeout as inst:
                print(inst)
                attempt += 1
                if attempt == 4:
                        break
                print("Reconnecting, try number {0}...".format(attempt))
                try:
                        bt_reconnect(client1)
                except RuntimeError as e:
                        print(e)
        else:
                download_complete = True
                for d in data:
                        sens1.data2cvs(d, filename1)

'''
Reconnect with client 2, disconnect client 1
'''

print("\nDisconnect client 1.")
bt_disconnect(client1)
try:
        print("\nConnecting with client 2...")
        bt_connect(client2)
except RuntimeError as e:
        print(e)
        quit()

print("Downloading data from client 2...\n")
download_complete = False
attempt = 1
if useTwoClients:
        while not download_complete:
                try:
                        data = client2.accelerometer.download_log()
                except PyMetaWearDownloadTimeout as inst:
                        print(inst)
                        attempt += 1
                        if attempt == 4:
                                break
                        print("Reconnecting, try number {0}...".format(attempt))
                        try:
                                bt_reconnect(client2)
                        except RuntimeError as e:
                                print(e)
                else:
	                download_complete = True
	                for d in data:
	                        sens2.data2cvs(d, filename2)

'''
Reconnect with client 1
'''
try:
        print("\nConnecting with client 1...")
        bt_connect(client1)
except RuntimeError as e:
        print(e)
        bt_disconnect(client2)
        quit()

'''
Let Green LED blinking
'''

print("\nGreen LEDs of both sensors are blinking for visualization that the whole recording process was successful")

pattern1 = client1.led.load_preset_pattern('blink', repeat_count=10)
if useTwoClients:
        pattern2 = client2.led.load_preset_pattern('blink', repeat_count=10)

client1.led.write_pattern(pattern1, 'g')
if useTwoClients:
        client2.led.write_pattern(pattern2, 'g')

client1.led.play()
if useTwoClients:
        client2.led.play()

time.sleep(5.0)

client1.led.stop_and_clear()
if useTwoClients:
        client2.led.stop_and_clear()

sens1.close_csv()
if useTwoClients:
        sens2.close_csv

'''
Disconnect
'''

print("\nDisconnecting all clients...")
client1.disconnect()
if useTwoClients:
	client2.disconnect()

