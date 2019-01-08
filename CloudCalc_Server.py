#server
#Team names: Austin Shammas and Joseph Breitner
#Program functions correctly and is interpreted correctly
#produces correct results

import socket
import sys
import math
from thread import *
import threading
import time
from datetime import datetime


HOST = ''
PORT = 8889  # Arbitrary non-privileged port
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print
'Socket created'

# Bind socket to local host and port
try:
	serverSocket.bind(('', PORT))
except socket.error as msg:  # if socket bind fails
	print
	'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()  # exit
print
'Socket bind complete'

# Start listening on socket
serverSocket.listen(10)
print
'Socket now listening'




def threaded(conn):

	while 1:
		conn.send('Type an operator and hit enter: (\'+\' or \'-\' or \'*\' or \'/\' or \'exp\' or \'factorial\' or \'LineCount\' or \'WordCount\' or \'ReverseWords\' or \'OutputFile\')')
		operator = conn.recv(1024)	# receive operator from client
		print('Time at start: \n')
		print datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

		if (operator == '+' or operator == '-' or operator == '*' or operator == '/' or operator == 'exp' or operator == 'factorial' or operator == 'LineCount' or operator == 'WordCount' or operator == 'ReverseWords' or operator == 'OutputFile'):
			if (operator != 'exp' and operator != 'factorial' and operator != 'LineCount' and operator != 'WordCount' and operator != 'ReverseWords' and operator != 'OutputFile'):

				# send a message to the client for entering the first operand
				conn.send('Enter first operand and hit enter: ')	# prompt client for first operand
				firstOperand = conn.recv(1024)	# receive first operand from client
				#firstOperand = 5
				if firstOperand[0] == '-':
					firstOperand = firstOperand[1:]
					firstOperand = float(firstOperand)
					firstOperand = firstOperand * -1
				elif firstOperand.isdigit():
					firstOperand = float(firstOperand)
				else:
					conn.send('Not a valid value.')	# send message and continue
					continue

				conn.send('Enter second operand and hit enter ')	# prompt client for second operand
				secondOperand = conn.recv(1024)	# receive second operand from client
				#secondOperand =12
				if secondOperand[0] == '-':	# check if str input has a negative sign
					secondOperand = secondOperand[1:]	# turn to int
					secondOperand = float(secondOperand)
					secondOperand = secondOperand * -1
				elif secondOperand.isdigit():	# if an integer, turn to float
					secondOperand = float(secondOperand)
				else:
					conn.send('Not a valid value.')	# send message and continue
					continue

			elif (operator == 'exp' or operator == 'factorial'):	# if exp of factorial
				conn.send('Type the operand and hit enter:')  # only one operand is required
				operand = conn.recv(1024)	# receive input from client

				if operand[0] == '-':	# check if negative
					operand = operand[1:] # turn to int
					operand = float(operand)
					operand = operand * -1
				elif operand.isdigit():	# if an int, turn to float
						operand = float(operand)

			elif (operator == 'LineCount' or operator == 'WordCount' or operator == 'ReverseWords' or operator == 'OutputFile'):	# if operator is for txt file
				if operator == 'LineCount':
					conn.send('Type the file name and hit enter: ')	# prompt client for name of txt file
					input_file = conn.recv(1024)  # get the fiel name. this will be prompted no matter which of the 3 operators the user selected
					file_open = open(input_file, "r")  # open and read the file user inputted
					lineCounter = 0 #initialize line counter
					for line in file_open:
						lineCounter = lineCounter +1; #increment our counter based on how many times line is found in our file

				elif operator == 'WordCount':
					conn.send('Type the file name and hit enter: ')  # prompt client for txt file
					input_file = conn.recv(1024)  # get the fiel name. this will be prompted no matter which of the 3 operators the user selected
					file_open = open(input_file, "r")  # open and read the file user inputted
					conn.send('Type the word to count in the file and hit enter: ')
					wordToFind = conn.recv(1024) #get the word to find
					amount = file_open.read().split() #read the user inputted file, then split it into a list
					onecount =0; #initialize our counter of words total in the file
					onecount = onecount + len(amount) #get output words total in file
					#read here for count: https://docs.python.org/3/tutorial/datastructures.html
					amount = amount.count(wordToFind) #.count will count how many times something is found.
													  #in this line, we are searching through the list(amount) to count how many words we are looking to find

				elif operator == 'ReverseWords':

					conn.send('Type the file name and hit enter: ')
					input_file = conn.recv(1024)  # get the fiel name. this will be prompted no matter which of the 3 operators the user selected
					file_open = open(input_file, "r")  # open and read the file user inputted
					conn.send("Type the output file name and hit enter: ")
					output_file = conn.recv(1024)
					outFile = open(output_file, 'w')
					# Opening and reading file into array 'inputArray'
					# read here to reverse words  https://docs.python.org/3/tutorial/datastructures.html
					inputArray = file_open.read().split()
					inputArray.reverse()
					inputArray = "\n".join(inputArray)
					outFile.write(inputArray)
					outFile.close()
				elif operator == 'OutputFile':
					pass	# OutputFile operator handled by client
				else:
					conn.send('Not a valid value.')
					continue	# send error message to client

		elif (operator == 'exit'):
			break	# break the loop if client sends 'exit'
		else:
			conn.send('The operator is not valid.')	# send error and continue
			continue
		try:	# results
			if (operator == '+'):
				result = firstOperand + secondOperand
			elif (operator == '-'):
				result = firstOperand - secondOperand
			elif (operator == '/'):
				result = firstOperand / secondOperand
			elif (operator == '*'):
				result = firstOperand * secondOperand
			elif (operator == 'exp'):
				result = math.exp(operand)
			elif (operator == 'factorial'):
				result = math.factorial(operand)
			elif (operator == 'LineCount'):
				result = lineCounter
			elif (operator == 'WordCount'):
				result = amount
			elif (operator == 'ReverseWords'):
				continue
			elif operator == 'OutputFile':
				continue
			else:
				print ('no response')

			if (operator != 'WordCount'):
				responseMessage = 'The result is ' + str(result) + '\n'
			elif (operator == 'WordCount'): #wordCount has a different message output than the others, according to his example
				responseMessage = 'The result is ' +str(result) + ' out of ' + str(onecount) +' words in the file'
				print('Time at end: \n')
				print datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
		except Exception:

			responseMessage =  'The operands were not valid for the specified operator \n'
		conn.send(responseMessage)
	conn.close()
exitFlag = 0

print('Awaiting Clients')
while 1:
	# wait to accept a connection - blocking call
	conn, prt = serverSocket.accept()
	print 'Connected to: ' + prt[0], ':', prt[1]

	start_new_thread((threaded),(conn,))
serverSocket.close()