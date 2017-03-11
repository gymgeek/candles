import socket, time, codes

class Candle_server:
    clients = []
    server_socket = socket.socket()


    def startServer(self, ip, port):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((ip, port))

    def connectClients(self, count):
        self.server_socket.listen(5)
        self.server_socket.setblocking(0)
        print("Waiting for " + str(count) + " clients to connect")
        self.clients = []
        try:
            while len(self.clients) < count:
                try:
                    client_socket, addr = self.server_socket.accept()
                    client_socket.setblocking(0)
                    self.clients.append((client_socket, addr))
                    print("Connected client #%s at address %s" % (len(self.clients), addr))
                except IOError:
                    pass

        except KeyboardInterrupt:
            self.server_socket.setblocking(1)
            print("Canceled, currently connected %s clients" % (len(self.clients)))
        self.server_socket.listen(0)

        for client in self.clients:
            client[0].setblocking(0)

    def send_to_all_clients(self,data):
        for client in self.clients:
            try:
                print(client[1],data)
                client[0].send(data)
            except:
                pass

    def wipe_clients(self):
         for soc in self.clients:
             try:                
                 soc[0].recv(4096)
             except:
                pass

    def start_game(self):
        self.wipe_clients()
        self.send_to_all_clients(codes.byte_red)
        print("red")
        time.sleep(1)
        self.send_to_all_clients(codes.byte_orange)
        print("orange")
        time.sleep(1)
        self.send_to_all_clients(codes.byte_green)
        print("green")
        time.sleep(1)
        self.send_to_all_clients(codes.byte_start)
        print("start")
        time.sleep(1)
        self.wipe_clients()
        while 1:
            for  soc in self.clients:
                client = soc[0]
                try:
                    recv = client.recv(1)
                    if recv == codes.byte_lost:
                        client.send(codes.byte_lost)
                        print("client ",soc[1], " lost")
                        self.clients.remove(soc)
                except:
                    pass
            if len(self.clients) == 1:
                
                self.clients[0][0].send(codes.byte_win)
                print("client ",self.clients[0][1], " won")
                break

        
    
    

server = Candle_server()
server.startServer("0.0.0.0",2260)
server.connectClients(2)
time.sleep(3)
print("start")
server.start_game()
