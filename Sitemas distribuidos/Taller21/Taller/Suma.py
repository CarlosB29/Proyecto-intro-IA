import socket
from datetime import datetime

class Suma:
    def __init__(self, suma_port):
        self.suma_port = suma_port

    def handle_client(self, client_socket):
        try:
            suma_precios = float(client_socket.recv(1024))
            suma_calculada = self.calcular_suma(suma_precios)
            client_socket.send(str(suma_calculada).encode())
            client_socket.close()
        except Exception as e:
            print(e)

    def calcular_suma(self, suma_precios):
        return suma_precios

    def run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(("localhost", self.suma_port))
            server_socket.listen(5)
            print(f"Esperando conexiones en el puerto {self.suma_port}")

            while True:
                client_socket, client_address = server_socket.accept()
                print(f"Conexión aceptada desde {client_address}")
                self.handle_client(client_socket)

if __name__ == '__main__':
    suma = Suma(12347)
    suma.run_server()
