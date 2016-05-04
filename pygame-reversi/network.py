import socket


class Network:
    def __init__(self):
        """
        Create sock for network game
        """
        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)
        self.main_sock = self.sock
        self.closed = False

    def wait_for_move(self):
        """
        Waiting for opponent move
        It use try/except to check if connection live.
        """
        while not self.closed:
            data = ''
            try:
                data = self.main_sock.recv(2).decode('utf-8')
                if not data:
                    pass
                elif data == 'ch':
                    self.main_sock.send(bytes('ch', 'utf-8'))
                    continue
                else:
                    return data
            except socket.timeout:
                pass

    def send_move(self, move):
        """
        Send move to opponent
        """
        move_str = str(move[0]) + str(move[1])
        self.main_sock.send(bytes(move_str, 'utf-8'))

    def send_end(self):
        """
        Send 'end' ('en', because always transfer 2 bytes) command to opponent
        """
        self.main_sock.send(bytes('en', 'utf-8'))


class Client(Network):
    def __init__(self):
        super().__init__()
        self.main_sock = self.sock

    def establish(self, ip, color):
        """
        Try to connect to the host by given IP
        When connected and received 'ch' ('check') command from host,
        send 'ch' ('check') for him
        """
        try:
            self.sock.connect((ip, 10000))
            self.sock.send(bytes('c'+str(color), 'utf-8'))
        except ConnectionRefusedError:
            print('No games on this IP')
            return False
        for i in range(100):
            data = self.sock.recv(2)
            data = data.decode('utf-8')
            if data == 'ch':
                self.main_sock.settimeout(1)
                return True
        return False


class Server(Network):
    def __init__(self):
        super().__init__()
        self.client_sock = None
        self.main_sock = self.client_sock

    def wait(self):
        """
        Wait for client connection
        If there is a connection, send 'ch' ('check') command
        and wait for the same ('ch') response
        """
        addr = ('', 10000)
        try:
            self.sock.bind(addr)
            self.sock.listen(1)
            while True:
                self.client_sock = self.sock.accept()[0]
                self.main_sock = self.client_sock
                data = self.client_sock.recv(2).decode('utf-8')
                if data in ['c1', 'c2']:
                    self.client_sock.send(bytes('ch', 'utf-8'))
                    self.main_sock.settimeout(1)
                    return int(data[1])
        except OSError:
            print('Try again later')
            return
