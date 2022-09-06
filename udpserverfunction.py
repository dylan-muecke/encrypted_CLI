# This is udpserver.py file
import socket
import hashlib
import json
from function import *

def runServer():
# Cryptographic Key
    n = 47 * 71
    My_Public = [97,n]
    My_Private = [1693,n]
    Client_Public = [0,0]

    # Initializations

    users = []
    logged_in = -1

    # create a UDP socket object
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    # Get local machine address
    ip = "localhost"                          

    # Set port number for this server
    port = 9999                                           

    # Bind to the port
    serversocket.bind((ip, port))                                  
    open_socket = True

    while open_socket:  
       print("Waiting to receive command on port " + str(port) + '\n')
       if Client_Public[0]==0:
          # Recieve Public Key from Client
          data, addr = serversocket.recvfrom(1024)
          Client_Public[0] = int(data.decode())
          data, addr = serversocket.recvfrom(1024)
          Client_Public[1] = int(data.decode())
          # Send Public Key
          serversocket.sendto(str(My_Public[0]).encode(), addr)
          serversocket.sendto(str(My_Public[1]).encode(), addr)
          print('Key Exchange Complete')

       # Receive the data of 1024 bytes maximum. Need to use recvfrom because there is not connecction
       data, addr = serversocket.recvfrom(1024)
       
       command = RSA(data.decode(),My_Private)
       print("received: " + command)
       
       if "REGISTER" in command:
          userdata = {
          'Last Name':0,
          'First Name':0,
          'Major':0,
          'Hometown':0,
          'Username':0,
          'Password':0
          }
          
          # Last Name
          serversocket.sendto(RSA("Last Name:",Client_Public).encode(), addr)
          data, addr = serversocket.recvfrom(1024)
          userdata['Last Name'] = RSA(data.decode(),My_Private)
          # First Name
          serversocket.sendto(RSA("First Name:",Client_Public).encode(), addr)
          data, addr = serversocket.recvfrom(1024)
          userdata['First Name'] = RSA(data.decode(),My_Private)
          # Major
          serversocket.sendto(RSA("Major:",Client_Public).encode(), addr)
          data, addr = serversocket.recvfrom(1024)
          userdata['Major'] = RSA(data.decode(),My_Private)
          # Hometown
          serversocket.sendto(RSA("Hometown:",Client_Public).encode(), addr)
          data, addr = serversocket.recvfrom(1024)
          userdata['Hometown'] = RSA(data.decode(),My_Private)
          # Username
          serversocket.sendto(RSA("Username:",Client_Public).encode(), addr)
          data, addr = serversocket.recvfrom(1024)
          userdata['Username'] = RSA(data.decode(),My_Private)
          # Password
          serversocket.sendto(RSA("Password:",Client_Public).encode(), addr)
          data, addr = serversocket.recvfrom(1024)
          password = RSA(data.decode(),My_Private)
          hash_object = hashlib.sha256(password.encode('utf8'))
          userdata['Password'] = hash_object.hexdigest()

          # Save Registration Data to JSON file
          with open("userdatalogs.json", "a+") as logfile:
             json.dump(userdata, logfile)
             logfile.write("\n")
          logfile.close()
          
          print(userdata)
          serversocket.sendto(RSA("Registration was successful. Thank you for registering!EOT",Client_Public).encode(), addr)
          serversocket.close()
          open_socket = False

       #LOG_IN   
       elif "LOG_IN" in command:
          users=[]
          with open("userdatalogs.json","r") as logfile:
            for x in logfile:
              users.append(eval(x))
          logfile.close()
          # Resets default "logged_out" state
          logged_in = -1 
          correct_username = False
          correct_password = False
          # Username
          serversocket.sendto(RSA("Username:",Client_Public).encode(), addr)
          while not correct_username:
             data, addr = serversocket.recvfrom(1024)
             username = RSA(data.decode(),My_Private)
             for user_id in range(len(users)):
                if username == users[user_id]['Username']:
                   correct_username = True
                   print(user_id)
                   break
             if not correct_username:
                serversocket.sendto(RSA("Username Incorrect\nUsername:",Client_Public).encode(), addr)
          # Password
          serversocket.sendto(RSA("Password:",Client_Public).encode(), addr)
          while not correct_password:
             data, addr = serversocket.recvfrom(1024)
             password = RSA(data.decode(),My_Private)
             hash_object = hashlib.sha256(password.encode('utf8'))
             if hash_object.hexdigest() == users[user_id]['Password']:
                correct_password = True
             if not correct_password:
                print('Password does not match')
                serversocket.sendto(RSA("Password does not match\nPassword:",Client_Public).encode(), addr)
          if (correct_username and correct_password):
             logged_in = user_id
             print("Logged in as user",user_id)
             serversocket.sendto(RSA("Log in successfulLOGGED",Client_Public).encode(), addr)
       # VIEW_REGISTRATION
       elif "VIEW_REGISTRATION" in command:
          if logged_in == -1:
             serversocket.sendto(RSA("Please LOG_IN to VIEW_REGISTRATION\n->",Client_Public).encode(), addr)
          else:
             send_file = RSA(str(users[user_id]),Client_Public).encode()
             serversocket.sendto(RSA("FILE",Client_Public).encode(), addr)
             serversocket.sendto(send_file, addr)
       elif "DISCONNECT" in command:
          logged_in == -1
          serversocket.close()
          open_socket = False
       else:
          serversocket.sendto(RSA("Please input a valid command\n ~ REGISTER\n ~ LOG_IN\n ~ VIEW_REGISTRATION\n ~ DISCONNECT\n->",Client_Public).encode(), addr)

   

