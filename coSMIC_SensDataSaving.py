#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:'coSMIC_SensDataSaving'
==================
Created by dmatthes1982 <dmatthes@cbs.mpg.de>
Created on 2018-04-25
"""

from datetime import datetime
import csv

class SensDataSaving:
        def __init__(self, filename):
                self.csvfile = open(filename, "wb")
                self.datawriter = csv.writer(self.csvfile, delimiter=';',               
                                                        quoting=csv.QUOTE_NONE)
                self.datawriter.writerow(['epoch', 'timestamp', 'x', 'y', 'z'])
  
        def download_callback(self, data, filename):
                epoch = float(data['epoch']) / 1000
                accel = data['value']
                timeVal = datetime.fromtimestamp(epoch)
                millisec = timeVal.microsecond/1000
                epoch = "%d-%02d-%02d %02d:%02d:%02d,%03d" % (timeVal.year, 
                        timeVal.month, timeVal.day, timeVal.hour, timeVal.minute, 
                        timeVal.second, millisec)
                timestamp = data['epoch']
                data['epoch'] = epoch
                print(data)
                self.datawriter.writerow([epoch, timestamp, accel.x, accel.y, accel.z])
        
        def close_csv(self):
                self.csvfile.close()
