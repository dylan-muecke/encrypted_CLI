Secure Command Line Interface
by Dylan Muecke
April 2022

I took a slightly different approach to this assigment than what was layed out in the
project document, but believe that I have still completed all of the necissary tasks.
I believe that the assignment has some inconsistencies that cause logical issues and
hope that my approach is acceptable.

In order to demonstrate the server/client connection. First run the serverup.py file
which is responsable for keeping the server constantly running. Once the server is
running, open udpclient.py and hit "Enter" to exchange public keys. Once the keys are 
recieved all communications between the client and server will be entirely encrypted.
Upon completion of REGISTRATION, the sockets will close and the client will severe its 
conection to the server. The running server file will automatically reboot the server
and wait for a new connection. Once a connection is established, the client also has
the option to LOG_IN, VIEW_REGISTRATION (once logged in), and DISCONNECT (severing the
connection to the server.
 
Attached is an example Wireshark packet capture and screenshot of the client using the
VIEW_REGISTRATION command and the server responding with the encrypted user data log.
