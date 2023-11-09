import socket
import pickle
import time
from datetime import datetime

class CopiaServer:
    def __init__(self, server_port):
        self.server_port = server_port

    def handle_client(self, client_socket, formatted_time):
        try:
            received_data = client_socket.recv(1024)
            productos = pickle.loads(received_data)
            productos_con_iva = []

            for producto in productos:
                iva_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                iva_socket.connect(("localhost", 12346))
                iva_socket.send(pickle.dumps(producto))
                producto_con_iva = pickle.loads(iva_socket.recv(1024))
                productos_con_iva.append(producto_con_iva)
                iva_socket.close()

            suma_precios = sum([producto.get_precio() for producto in productos_con_iva])
            suma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            suma_socket.connect(("localhost", 12347))
            suma_socket.send(str(suma_precios).encode())
            suma_calculada = float(suma_socket.recv(1024))
            suma_socket.close()

            client_socket.send(str(suma_calculada).encode())
            client_socket.close()
        except Exception as e:
            print(e)

    def run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(("localhost", self.server_port))
            server_socket.listen(5)
            print(f"Esperando conexiones en el puerto {self.server_port}")

            while True:
                client_socket, client_address = server_socket.accept()
                print(f"Conexión aceptada desde {client_address}")
                connection_time = datetime.now().strftime("%H:%M:%S")
                self.handle_client(client_socket, connection_time)

if __name__ == '__main__':
    copia_server = CopiaServer(12356)
    copia_server.run_server()
