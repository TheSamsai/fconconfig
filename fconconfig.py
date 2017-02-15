#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2017 Sami Lahtinen <thesamsai@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from evdev import InputDevice, categorize, ecodes
import evdev
import os
import time

# An object to hold our controller settings and to generate the shell script
class Controller:
	button_a = None
	button_b = None
	button_x = None
	button_y = None
	button_rb = None
	button_rt = None
	button_lb = None
	button_lt = None
	buton_start = None
	button_back = None
	button_tl = None
	button_tr = None
	dpad_x = None
	dpad_y = None
	x1 = None
	y1 = None
	x2 = None
	y2 = None
	invert_y = None
	
	
	# Setters for all the buttons and inputs
	def set_button_a(self, event):
		self.button_a = event
	def set_button_b(self, event):
		self.button_b = event
	def set_button_x(self, event):
		self.button_x = event
	def set_button_y(self, event):
		self.button_y = event
	def set_button_rb(self, event):
		self.button_rb = event
	def set_button_rt(self, event):
		self.button_rt = event
	def set_button_lb(self, event):
		self.button_lb = event
	def set_button_lt(self, event):
		self.button_lt = event
	def set_button_start(self, event):
		self.button_start = event
	def set_button_back(self, event):
		self.button_back = event
	def set_button_tl(self, event):
		self.button_tl = event
	def set_button_tr(self, event):
		self.button_tr = event
	def set_dpad_x(self, event):
		self.dpad_x = event
	def set_dpad_y(self, event):
		self.dpad_y = event
	def set_x1(self, event):
		self.x1 = event
	def set_y1(self, event):
		self.y1 = event
	def set_x2(self, event):
		self.x2 = event
	def set_y2(self, event):
		self.y2 = event
	def set_inverted(self, inverted):
		self.inverted = inverted
	
	# Generate a script to run xboxdrv with the correct configurations
	def generate_config(self, device_path):
		# Map X and Y axes
		absmaps = self.x1 + "=x1," + self.y1 + "=y1," + self.x2 + "=x2," + self.y2 + "=y2," + self.dpad_x + "=dpad_x," + self.dpad_y + "=dpad_y"
		# Map buttons
		keymaps = self.button_a + "=a," + self.button_b + "=b," + self.button_x + "=x," \
				+ self.button_y + "=y," + self.button_back + "=back," \
				+ self.button_start + "=start," + self.button_lb + "=lb," \
				+ self.button_lt + "=lt," + self.button_rb + "=rb," \
				+ self.button_rt + "=rt," + self.button_tl + "=tl," \
				+ self.button_tr + "=tr"
		# If we are inverted, negate Y values
		if self.inverted:
			axismap = "-Y1=Y1,-Y2=Y2"
		else:
			axismap = "Y1=Y1,Y2=Y2"
		
		# Compile our inputs into a single command
		command = "xboxdrv --evdev " + device_path + " --evdev-absmap " + absmaps + " --axismap " + axismap + " --evdev-keymap " + keymaps + " --mimic-xpad --silent"
		
		fob = open("xboxdrv.sh", "w")
		
		# Shell script writing begins
		fob.write("#!/bin/sh\n")
		# The part below has been commented out because doing changes like that
		# to a foreign system is not polite. However, other js devices can cause
		# problems with some games.
		#fob.write("rm /dev/input/js*\n")
		fob.write(command)
		
		fob.close()
		
		# Let's make the script executable, just to be polite
		os.system("chmod +x xboxdrv.sh")

def read_button_event(device):
	for event in device.read_loop():
		# Make sure we are looking at a key press
		if event.type == ecodes.EV_KEY:
			s = str(categorize(event))
			
			if "up" in s:
				keyevent = s[s.find("(")+1:s.find(")")]
				
				# Some events have some special nonsense we need to deal with
				if "[" in keyevent:
					keyevent = keyevent[keyevent.find(", '")+1:s.find("']")].replace(" ", "").replace("'", "").replace("]", "")
				
					print(keyevent)
					return keyevent
				# Others don't
				else:
					print(keyevent)
					return keyevent

def read_js_event(device):
	for event in device.read_loop():
		# This time we want an ABS event (horizontal and vertical axes)
		if event.type == ecodes.EV_ABS:
			s = str(categorize(event))
			
			keyevent = s[s.find("(")+1:s.find(")")].split(", ")[1]
			
			print(keyevent)
			return keyevent

def main(args):
	devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
	
	print("Devices found: ")
	x = 1
	
	for device in devices:
		print(str(x) + ": " + device.fn, device.name, device.phys)
		x += 1
	
	selection = int(input("Which device to capture? "))
	
	device = devices[selection - 1]
	gamepad = Controller()
	
	print("Device selected.\n")
	
	print("Buttons will now be configured.\n")
	
	print("Press the A button on the gamepad.")
	gamepad.set_button_a(read_button_event(device))
	
	print("Press the B button on the gamepad.")
	gamepad.set_button_b(read_button_event(device))
	
	print("Press the X button on the gamepad.")
	gamepad.set_button_x(read_button_event(device))
	
	print("Press the Y button on the gamepad.")
	gamepad.set_button_y(read_button_event(device))
	
	print("Press the Back button on the gamepad.")
	gamepad.set_button_back(read_button_event(device))
	
	print("Press the Start button on the gamepad.")
	gamepad.set_button_start(read_button_event(device))
	
	print("Press the LB button on the gamepad.")
	gamepad.set_button_lb(read_button_event(device))
	
	print("Press the LT button on the gamepad.")
	gamepad.set_button_lt(read_button_event(device))
	
	print("Press the RB button on the gamepad.")
	gamepad.set_button_rb(read_button_event(device))
	
	print("Press the RT button on the gamepad.")
	gamepad.set_button_rt(read_button_event(device))
	
	print("Press the Left Thumbstick on the gamepad.")
	gamepad.set_button_tl(read_button_event(device))
	
	print("Press the Right Thumbstick button on the gamepad.")
	gamepad.set_button_tr(read_button_event(device))
	
	print("\nButtons configured, moving to axis configuration.\n")
	time.sleep(2)
	
	# Axis input is fidly, we need to read these twice to get a proper reading
	# Second input is the important one
	print("Move Left Thumbstick Left")
	gamepad.set_x1(read_js_event(device))
	gamepad.set_x1(read_js_event(device))
	time.sleep(3)
	
	print("Move Left Thumbstick Up")
	gamepad.set_y1(read_js_event(device))
	gamepad.set_y1(read_js_event(device))
	time.sleep(3)
	
	print("Move Right Thumbstick Left")
	gamepad.set_x2(read_js_event(device))
	gamepad.set_x2(read_js_event(device))
	time.sleep(3)
	
	print("Move Right Thumbstick Up")
	gamepad.set_y2(read_js_event(device))
	gamepad.set_y2(read_js_event(device))
	time.sleep(3)
	
	print("Press Left on the DPAD")
	gamepad.set_dpad_x(read_js_event(device))
	gamepad.set_dpad_x(read_js_event(device))
	time.sleep(3)
	
	print("Press Up on the DPAD")
	gamepad.set_dpad_y(read_js_event(device))
	gamepad.set_dpad_y(read_js_event(device))
	
	# Some gamepads start with inverted controls, I have no idea why
	# Anyway, we need to take this into account
	inverted = input("Invert Y axis? (y/n): ")
	
	if inverted == "y":
		print("Y axis will be inverted.")
		gamepad.set_inverted(True)
	else:
		print("Y axis will be default.")
		gamepad.set_inverted(False)
	
	gamepad.generate_config(device.fn)
	
	print("Gamepad configured. Run './xboxdrv.sh' to use your gamepad with the new configuration.")
	
	return 0

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
