# Author : Aaron Luchan 
import socket

IP_ADDRESS = "127.0.0.1"
PORT = 65432
FILE_SIZE = 2097152 # the size of the 2MB file
Half_buffer = 1048576 # half size of the file

# CC Algorithms:
CC_Algorithm1 = "reno"  # CC Algorithm reno
CC_Algorithm2 = "cubic"  # CC Algorithm cubic

# Authentication number - XOR of the last 4 numbers of our IDs
auth_xor = str(9515 ^ 1940)

# Reading the file:
with open('2MB.txt', 'rb') as file:  # read binary mode because the file doesn't content data
    file_data = file.read()
    # Parting the file on 2
    f_A = file_data[:Half_buffer]
    f_B = file_data[Half_buffer:]

# Creating TCP Connection between the sender and receiver
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((IP_ADDRESS, PORT))

while True:
    print(f"Connection established to {IP_ADDRESS}\n")
    # Setting the first algorithm - Reno
    cc = CC_Algorithm1.encode()
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, cc)
    print(f"Set CC algorithm to {CC_Algorithm1}")
    # Sending first part of file:
    print("Sending the first part...")
    sock.sendall(f_A)
    print("The first part of the file has been successfully sent\n")

    # Authentication:
    print("Waiting for authentication...")
    auth_receiver = sock.recv(1024).decode()
    auth_receiver = str(auth_receiver)
    if auth_xor == auth_receiver:

        print("Authentication successful.\n")
    else:
        print("Authentication failed. Closing connection...\n")
        sock.close()
        break

    # Changing CC algorithm to Cubic
    cc = CC_Algorithm2.encode()
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, cc)
    print(f"Changed CC algorithm to {CC_Algorithm2}")

    # Sending second part of file:
    print("Sending the second part...")
    sock.sendall(f_B)
    print("The second part of the file has been successfully sent\n")

    # Asking user if they want to send the file again:
    message = sock.recv(1024).decode()
    message = str(message)
    if message == "wait":
        send_another_file = input("DO YOU WANT TO SEND THIS FILE AGAIN?---(y/n): ")
        if send_another_file == "y":
            sock.send("y".encode())
            print("Notified receiver that file will be sent again.\n")
            # Changing CC algorithm back:
            cc = CC_Algorithm1.encode()
            sock.setsockopt(socket.IPPROTO_TCP ,socket.TCP_CONGESTION ,cc)

        elif send_another_file == "n":
            # closing the socket communication
            sock.sendall("n".encode())
            sock.close()
            print("Exiting program...")
            exit()
            break

        else:
            print("Invalid response. Please try again.")
