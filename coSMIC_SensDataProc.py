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
		self.motion = False;

	def dataProcessing(self, data, num):
		epoch = data['epoch']	
		accel = data['value']
		self.ringBuffer.append(abs(accel.x) + abs(accel.y) + abs(accel.z))
		variance = np.var(np.array(self.ringBuffer));		
		if variance <= 0.000001:
			motionVal = -6
		else:		
			motionVal = np.log10(variance)
		
		#print("[%i, %i]: %0.2f" % (num, epoch, motionVal))
				
		if motionVal > -2 and not self.motion:
			if num == 1:			
				print("[%i, %i]: %x" % (num, epoch, 0x64))
				self.lpt.setData(0x64)
			if num == 2:			
				print("[%i, %i]: %x" % (num, epoch, 0x66))
				self.lpt.setData(0x66)

			self.motion = True

		if motionVal < -3 and self.motion:
			if num == 1:			
				print("[%i, %i]: %x" % (num, epoch, 0x65))
				self.lpt.setData(0x65)
			if num == 2:			
				print("[%i, %i]: %x" % (num, epoch, 0x67))
				self.lpt.setData(0x67)
			
			self.motion = False
		
