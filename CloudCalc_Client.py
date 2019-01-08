#client
#Team names: Austin Shammas and Joseph Breitner
#Program functions correctly and is interpreted correctly
#produces correct results
import socket

HOST = '127.0.0.1'
PORT = 8889  # Arbitrary non-privileged port
size = 1024

# Connect the clientSocket to the server
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to HOST IP and PORT number
clientSocket.connect((HOST, PORT))

while 1:
    receivedMessage = clientSocket.recv(1024)  # Get the message from the Server
    print receivedMessage  # Print the Message on the screen

    if (receivedMessage.find('enter') >= 0):  # If there is a need for input from user
        inputFromKeyboard = raw_input()  # Get the input from the keyboard
        clientSocket.send(inputFromKeyboard)  # and send it to the Server
        if (inputFromKeyboard == 'exit'):  # If the input is 'exit', close the client
            break
        elif (inputFromKeyboard == 'OutputFile'): # if user enters 'OutputFile'
            print("Type the file name you want to display and hit enter")
            output_name = raw_input()	# take input from user
            fileToOpen = open(output_name, 'r')	# open file
            openFile = fileToOpen.read().split()	# split file into array
            fileN = "\n".join(openFile)	# join array into string
            print(fileN)	# print the file

clientSocket.close()