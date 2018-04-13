#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:mod:'coSMIC_SensDataProc'
==================
Created by dmatthes1982 <dmatthes@cbs.mpg.de>
Created on 2018-04-11
"""

import parallel
import numpy as np
from numpy_ringbuffer import RingBuffer
import pdb

class SensDataProc:
	def __init__(self, par):
		self.ringBuffer = RingBuffer(capacity=10, dtype=np.float)
		self.lpt = par
		self.prevMeanAccel = 1;

	def dataProcessing(self, data, num):
		epoch = data['epoch']	
		accel = data['value']
		self.ringBuffer.append(abs(accel.x) + abs(accel.y) + abs(accel.z))
		meanAccel = np.mean(np.array(self.ringBuffer))
		#print("[%i, %i] - %0.2f" % (num, epoch, meanAccel))
		if meanAccel > 2 and self.prevMeanAccel < 2:
			print("[%i, %i] - %x" % (num, epoch, 0x64))
			self.lpt.setData(0x64)
		if meanAccel < 2 and self.prevMeanAccel > 2:
			print("[%i, %i] - %x" % (num, epoch, 0x65))
			self.lpt.setData(0x65)
			
		self.prevMeanAccel = meanAccel	
