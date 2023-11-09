import socket
import pickle

class IvaNode:
    def __init__(self, iva_port):
        self.iva_port = iva_port

    def handle_client(self, client_socket):
        try:
            received_data = client_socket.recv(1024)
            producto = pickle.loads(received_data)

            if producto.get_category().lower() != "canasta":
                nuevo_precio = producto.get_precio() * 1.19
                producto.set_precio(nuevo_precio)
                print(f"El precio del producto {producto.get_name()} es: {producto.get_precio()}")

            client_socket.send(pickle.dumps(producto))
            client_socket.close()
        except Exception as e:
            print(e)

    def run_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(("localhost", self.iva_port))
            server_socket.listen(5)
            print(f"Esperando conexiones en el puerto {self.iva_port}")

            while True:
                client_socket, _ = server_socket.accept()
                self.handle_client(client_socket)

if __name__ == '__main__':
    iva_node = IvaNode(12346)
    iva_node.run_server()
