import socket
import pickle
from datetime import datetime
import concurrent.futures

class Producto:
    def __init__(self, name, category, precio):
        self.name = name
        self.category = category
        self.precio = precio

def handle_client(client_socket, formatted_time):
    try:
        data = client_socket.recv(4096)
        productos = pickle.loads(data)
        productos_con_iva = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            productos_con_iva = list(executor.map(handle_iva, productos))

        suma_precios = sum(producto.precio for producto in productos_con_iva)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as suma_socket:
            suma_socket.connect(('localhost', 12347))
            with suma_socket.makefile('wb') as suma_output:
                suma_output.write(str(suma_precios).encode())

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as suma_socket:
            suma_socket.connect(('localhost', 12347))
            with suma_socket.makefile('rb') as suma_input:
                suma_calculada = suma_input.read()
                client_socket.send(suma_calculada)

    except Exception as e:
        print(f"Error: {e}")

def handle_iva(producto):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as iva_socket:
            iva_socket.connect(('localhost', 12346))
            with iva_socket.makefile('wb') as iva_output:
                iva_output.write(pickle.dumps(producto))

            with iva_socket.makefile('rb') as iva_input:
                producto_con_iva = pickle.loads(iva_input.read())
                return producto_con_iva

    except Exception as e:
        print(f"Error: {e}")
        if producto.category.lower() != "canasta":
            producto.precio *= 1.19
        return producto

def main():
    server_port = 12345

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('localhost', server_port))
            server_socket.listen(1)
            print(f"Esperando conexiones en el puerto {server_port}")

            while True:
                client_socket, client_addr = server_socket.accept()
                formatted_time = datetime.now().strftime("%hh:mm:ss a")
                print(f"Conexión aceptada desde {client_addr} a las {formatted_time}")
                handle_client(client_socket, formatted_time)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
