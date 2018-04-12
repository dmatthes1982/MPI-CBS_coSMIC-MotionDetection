#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:'coSMIC_SensDataProc'
==================
Created by dmatthes1982 <dmatthes@cbs.mpg.de>
Created on 2018-04-11
"""

import numpy as np
from numpy_ringbuffer import RingBuffer
import pdb

class SensDataProc: 
	def __init__(self):
		self.ringBuffer = RingBuffer(capacity=10, dtype=np.float)

	def dataProcessing(self, data, num):
		epoch = data['epoch']	
		accel = data['value']
		self.ringBuffer.append(abs(accel.x) + abs(accel.y) + abs(accel.z))
		meanAccel = np.mean(np.array(self.ringBuffer))
		print("[%i, %i] - %f" % (num, epoch, meanAccel))
