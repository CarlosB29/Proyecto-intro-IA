import socket
import pickle
import time

# Importa la clase Producto
from Producto import Producto

class Client:
    def __init__(self, server_address, server_port, backup_server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.backup_server_port = backup_server_port

    def communicate_with_server(self):
        connected = False
        while not connected:
            try:
                connected = self.connect_to_server(self.server_address, self.server_port)
            except ConnectionRefusedError:
                print("No se pudo conectar al servidor principal. Intentando con el servidor de respaldo...")
                time.sleep(2)
                try:
                    connected = self.connect_to_server(self.server_address, self.backup_server_port)
                except ConnectionRefusedError:
                    print("No se pudo conectar al servidor de respaldo. Verifique la conexión.")

    def connect_to_server(self, server_address, server_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((server_address, server_port))
            productos = []
            print("Ingrese la cantidad de productos: ")
            cantidad_productos = int(input())
            for i in range(cantidad_productos):
                print(f"Ingrese el nombre del producto {i + 1}: ")
                nombre = input()
                print(f"Ingrese la categoría del producto {i + 1}: ")
                categoria = input()
                print(f"Ingrese el precio del producto {i + 1}: ")
                precio = float(input())
                producto = Producto(nombre, categoria, precio)
                productos.append(producto)

            serialized_productos = pickle.dumps(productos)
            client_socket.send(serialized_productos)
            suma_calculada = float(client_socket.recv(1024))
            print(f"Total a pagar: {suma_calculada}")
            return True

if __name__ == '__main':
    client = Client("localhost", 12345, 12356)
    client.communicate_with_server()
