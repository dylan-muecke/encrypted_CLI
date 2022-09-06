# This is udpclient.py file

#Import socket programming module
import socket
import json
from function import *

# Cryptographic Key
n = 83 * 61
My_Public = [53,n]
My_Private = [557,n]
Server_Public = [0,0]

# Available Commands
    # REGISTER
    # LOG_IN
    # VIEW_REGISTRATION
    # DISCONNECT
    
# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# Set destination port
port = 9999

# Include the server Address 
serverAddr = ('localhost', port)

command = input("Press Enter to Connect")

# Send My Public Key to Server
s.sendto(str(My_Public[0]).encode(), serverAddr)
s.sendto(str(My_Public[1]).encode(), serverAddr)

# Receive Public Key from Server
msg, addr = s.recvfrom(1024)
Server_Public[0] = int(msg.decode())
msg, addr = s.recvfrom(1024)
Server_Public[1] = int(msg.decode())

print("Key Exchange Complete")
# Choose Function
#command = input("->")
#s.sendto(command.encode(), serverAddr)
command="waiting"
while (command != "DISCONNECT"):
    complete=False
    # Choose Function
    command = input("->")
    s.sendto(RSA(command,Server_Public).encode(), serverAddr)
    if "DISCONNECT" in command:
        complete = True
        s.close
        print("Bye!")
    # Process Response
    while (complete==False):
        msg, addr = s.recvfrom(1024)
        message = RSA(msg.decode(),My_Private)
        if "EOT" in message:
            print(message.replace("EOT",""))
            complete=True
            s.close()
            command = "DISCONNECT"
            break
        elif "LOGGED" in message:
            print(message.replace("LOGGED",""))
            complete=True
            break
        elif "FILE" in message:
            msg_file, addr = s.recvfrom(1024)
            print("message recieved:\n",msg_file.decode())
            json_file = eval(RSA(msg_file.decode(),My_Private))
            print("message decrypted:\n",json_file)
            break
        elif "PRINT" in message:
            output, addr = s.recvfrom(1024)
            print_out=RSA(output.decode(),My_Private)
            print(print_out)
            print(print_out.replace("PRINT",""))
            break
        else:
            response = input(message)
            sent = RSA(response,Server_Public)
            s.sendto(sent.encode(), serverAddr)
            print("sent:",response)

# Close connection
s.close()
