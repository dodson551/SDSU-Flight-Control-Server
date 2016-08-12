#!/usr/bin/python

import socket
import sys
import serial
import thread
import threading

# create a serial connection to arduino
ser = serial.Serial('/dev/ttyACM0', 9600)

# create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostIp = "192.168.1.227"
port = 6969
serverAddress = (hostIp, port)
sock.bind(serverAddress)

print "Socket setup: %s | %s" % serverAddress
print "Listening..."

# set global variables that will hold the values from serial connection
mostRecentX = 0.0;
mostRecentY = 0.0;

def MAIN():
	try:

		
		# main listening loop
		while True:
			data, address = sock.recvfrom(4096)
			
			# when a UDP packet arrives...
			if data:
				# convert received bytes to string
				decodedStr = data.decode("utf-8")
				
				print "Message Received: %s" % decodedStr

				if 's' in decodedStr:
					output = update_settings(decodedStr)
					print output

				
				# # use string to find the function to callable
				# if decodedStr == "Start X Pattern":
				# 	print "Calling XPattern..."
				# 	sock.sendto("Starting X Pattern", address)
					
				# 	# start X Pattern
				# 	try:
				# 		thread.start_new_thread( StartPattern, ('1', ser, ) )
				# 	except: 
				# 		print "Error Starting Thread..."
						
				# elif decodedStr == "Get Values":
				# 	msg = FormatXYValuesMessage(mostRecentX, mostRecentY)
				# 	sent = sock.sendto(msg, address)
				
				# else: 
				# 	msg = "Incorrect Command.  Try Again..."
				# 	sent = sock.sendto(msg, address)
					
				# # when command has been executed, update console...
				# print "Waiting for Command..."
				
	except KeyboardInterrupt:
		print "\nClosing serial connection..."
		ser.close()
		print "Closing socket..."
		sock.close()
		print "\n"
		sys.exit()
# end MAIN()

def update_settings(string):
	# s|100:200:300:400:500:600
	ser.write(string)
	outputStr = ser.readline()
	return outputStr

def StartPattern(pattern, ser):
	global mostRecentX
	global mostRecentY
	# start the pattern execution on Arduino
	ser.write(pattern)
	
	lock = threading.Lock()
	
	# loop until the arduino stops outputting values
	coordinate = "x"
	while coordinate != "z":
		line = ser.readline()
		coordinate, value = line.split(":")
		
		if coordinate == "x":
			with lock:
				mostRecentX = float(value)
		elif coordinate == "y":
			with lock:
				mostRecentY = float(value)
		
# end StartPattern()

#def ParseSerialMessage(msg)
	
# end ParseSerialMessage()

def FormatXYValuesMessage(x, y):
	msg = "X:%f|Y:%f" % (x, y)
	
	return msg
# end FormatXYValuesMessage()

#==================================================================
#
#	Actually Runs the Main Function
#
#==================================================================	

MAIN()

#==================================================================
#	End Script
#==================================================================