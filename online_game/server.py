# install socket package: pip install sockets

import socket
import _thread 

SERVER = "192.168.0.103"
PORT = 5555

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Address Family, socket type

# bind our socket to a particular port
s.bind((SERVER,PORT))

s.listen(2) # max clients that can connect to the server

print("SERVER STARTED, WAITING FOR CONNECTION")



def make_str(tup):
    return str(tup[0])+","+str(tup[1])

def make_tuple(st):
    st = st.split(",")
    return int(st[0]), int(st[1])


pos = [(250,150), (50,50)]

def threaded_client(conn, player):
    data = make_str(pos[player])
    conn.send(str.encode(data)) # send the coordinates to the client

    while True:
        data = conn.recv(4096).decode() # 4096 is no. of bits, received data is in str format
        pos[player] = make_tuple(data)
        print(pos[player])
        
        if not data:
            print("LOST CONNECTION")
            break
        else:
            if player == 1:
                conn.send(str.encode(make_str(pos[0]))) # sending player 0 position
            else:
                conn.send(str.encode(make_str(pos[1])))
    conn.close()

num_client = 0
while True:
    print("inside loop", num_client)
    conn, addr = s.accept() # server waiting to accept connections
    print("Connected to ", conn, addr)

    _thread.start_new_thread(threaded_client, (conn, num_client))
    num_client += 1