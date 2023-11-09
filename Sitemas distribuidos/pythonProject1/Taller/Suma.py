import socket

def main():
    suma_port = 12347

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('localhost', suma_port))
            server_socket.listen()

            while True:
                client_socket, client_addr = server_socket.accept()
                handle_client(client_socket)

    except Exception as e:
        print(f"Error: {e}")

def handle_client(client_socket):
    try:
        suma_precios = client_socket.recv(4096)
        suma_calculada = calcular_suma(float(suma_precios))
        with client_socket.makefile('wb') as suma_output:
            suma_output.write(str(suma_calculada).encode())

    except Exception as e:
        print(f"Error: {e}")

def calcular_suma(suma_precios):
    return suma_precios

if __name__ == "__main__":
    main()
