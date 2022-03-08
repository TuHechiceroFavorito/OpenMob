from bluetooth import *

class Connection:
    def __init__(self):     
        self.buf_size = 1024

    def start_socket(self):
        self.sock = BluetoothSocket(RFCOMM)
        self.sock.bind(("", PORT_ANY))

    def start_server(self):
        self.sock.listen(1)
        print("Starting bluetooth server")
        advertise_service(self.sock, "OpenMobServer", service_classes=[SERIAL_PORT_CLASS])

    def server_connect(self):
        print('Listening for connection...')
        self.client, self.address = self.sock.accept()
        print(f'Connected to {self.address}')

    def recv(self):
        data = self.client.recv(self.buf_size).decode('utf-8')
        if data:
            print(f"New message: {data}")
            return data

    def close_connection(self):
        self.client.close()

    def close_socket(self):
        self.sock.close()

if __name__ == "__main__":
    conn = Connection()
    conn.start_socket()
    conn.start_server()
    conn.server_connect()
    while True:
        conn.recv()