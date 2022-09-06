import socket
import hashlib
import json

# This function can be used for both Encryption and Decryption.
# For encryption, input plaintext and public key
# For decryption, input ciphertext and private key
def RSA(input_text, key):
  output_text = ""
  for character in input_text:
    output_text = output_text + (chr((ord(character)**key[0])%key[1]))
  return output_text

def register(serversocket,Client_Public,My_Private):
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