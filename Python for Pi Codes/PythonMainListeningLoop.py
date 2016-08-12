#!/usr/bin/python

import socket
import sys
import serial
import thread
import threading

# global variable to check if GUI requests exit from program
exitReq = False

# buffer size global variable 
BUF = 4096

# create a serial connection to arduino
ser = serial.Serial('/dev/ttyACM0', 9600)

# socket setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

exitsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
exitsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

# create UDP socket for listener
hostIp = "192.168.1.227"
port = 6969
serverAddress = (hostIp, port)
sock.bind(serverAddress)

# create seperate UDP socket for exit thread
exitport = 7979
exitserverAddress = (hostIp, exitport)
exitsock.bind(exitserverAddress)

print "Socket setup: %s | %s" % serverAddress
print 
print "Listening..."

# set global variables that will hold the values from serial connection
mostRecentX = 0.0;
mostRecentY = 0.0;

def MAIN():

	try:

		exit_trd = threading.Thread(target=exit_thread())
		exit_trd.start()
		print "Exit thread started."

		# main listening loop
		while True:
			if exitReq is True:
				print "Exiting listening loop."
				print "\nClosing serial connection..."
				ser.close()
				print "Closing socket..."
				sock.close()
				print "\n"
				sys.exit()
			else:
				data, address = sock.recvfrom(BUF)
				
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

def exit_thread():
	while True:
		data, address = exitsock.recvfrom(BUF)
		if data:
			if 'exit' in data:
				print data
				exitReq = True
			else:
				exitReq = False
		return

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