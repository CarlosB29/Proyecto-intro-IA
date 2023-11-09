import socket
import pickle

def main():
    server_port = 12346

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('localhost', server_port))
            server_socket.listen()

            while True:
                client_socket, client_addr = server_socket.accept()
                with client_socket:
                    data = client_socket.recv(4096)
                    producto = pickle.loads(data)

                    if producto.category.lower() != "canasta":
                        nuevo_precio = producto.precio * 1.19
                        producto.precio = nuevo_precio
                        print(f"El precio del producto {producto.name} es: {producto.precio}")

                    with client_socket.makefile('wb') as client_output:
                        client_output.write(pickle.dumps(producto))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
