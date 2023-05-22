# Author : Aaron Luchan
import socket
import time

HOST = '127.0.0.1'  # IP address of sender
PORT = 65432  # Port to listen on
Half_buffer = 1048576  # half size of the file
BUFFER_SIZE = 8192  # common buffer size for network socket programming is 8192 bytes
# Authentication number - XOR of the last 4 numbers of our IDs
auth_xor = 9515 ^ 1940

# CC Algorithms:
CC_Algorithm1 = "reno"  # CC Algorithm reno
CC_Algorithm2 = "cubic"  # CC Algorithm cubic

# 2 lists to measure the average times of the 2 parts
firstpart_time = []
secondpart_time = []


def file_rcc():
    # Create a TCP connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    # Listen for incoming connections
    sock.listen()
    # Wait for a connection
    print('Waiting for the connection...')
    connection, sender_address = sock.accept()
    print(f'Connection established from {sender_address[0]}')  # To show the connection with the IP
    while True:
        print('Receiving first part of file...')
        # Set the CC algorithm to Reno
        cc = CC_Algorithm1.encode()
        connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, cc)
        # Start measuring the time
        start_time1 = time.time()
        # Receive the first part of the file
        data = bytes()  # Initialize an empty data
        while len(data) < Half_buffer:
            data = data + connection.recv(BUFFER_SIZE)

        print("The reception of the first half was successful")
        # Measuring the end time of the sending
        end_time1 = time.time()
        # measure the total time
        time_total1 = end_time1 - start_time1
        firstpart_time.append(time_total1)

        # Send back authentication to sender
        print("Sending authentication")
        connection.sendall(str(auth_xor).encode())
        # Changing the CC Algorithm
        cc = CC_Algorithm2.encode()
        connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_CONGESTION, cc)
        print('Authentication was successful')

        # Receive the second part of the file
        # Start measuring the time
        start_time2 = time.time()
        print('Receiving second part of file...')
        data = bytes()
        while len(data) < Half_buffer:
            data = data + connection.recv(BUFFER_SIZE)
        print("The reception of the second half was successful\n")
        # Measuring the end time of the sending
        end_time2 = time.time()
        # measure the total time
        time_total2 = end_time2 - start_time2
        secondpart_time.append(time_total2)

        # Checking if we want to send the file again
        # Receive data from sender
        print('Waiting to receive data...\n')
        # check if sender wants to send another file
        connection.send("wait".encode())
        message = connection.recv(1024).decode()
        if message == "n":
            print("Calculating sending times of the file... \n")

            print("Sending times for the first part - RENO algorithm: ")
            print("* * * * * * * * * * * *")
            j = 1
            for i in firstpart_time:
                print(f"Sending number: {j}: {i} seconds")
                j = j + 1
            print("* * * * * * * * * * * *\n")

            print("Sending times for the second part - CUBIC algorithm: ")
            print("* * * * * * * * * * * *")
            j = 1
            for i in secondpart_time:
                print(f"Sending number: {j}: {i} seconds")
                j = j + 1
            print("* * * * * * * * * * * *\n")

            # Total average time calculation :
            print("Calculating average times of the file: ")
            firstpart_timeav = sum(firstpart_time) / len(firstpart_time)
            secondpart_timeav = sum(secondpart_time) / len(secondpart_time)
            print("* * * * * * * * * * * *")
            print(f"The average time of the first part - RENO algorithm : {firstpart_timeav} seconds")
            print(f"The average time of the second part - CUBIC algorithm : {secondpart_timeav} seconds")
            print("* * * * * * * * * * * *\n")
            connection.close()
            return
        elif message == "y":
            print("Receiving the file again\n")
            continue
        else:
            connection.close()
            break


file_rcc()
