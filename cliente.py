import socket

# Conectarse al server y enviar mensaje
def iniciar_cliente(host="127.0.0.1", puerto=5000):
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((host, puerto))
        print(f"Conectado al servidor {host}:{puerto}")

        while True:
            mensaje = input("Escribí un mensaje ('exito' para salir): ")
            if mensaje.lower() == "exito":
                print("Cerrando conexión...")
                break
            cliente.send(mensaje.encode())
            respuesta = cliente.recv(1024).decode()
            print(f"Servidor: {respuesta}")

        cliente.close()
    except Exception as e:
        print(f"Error al conectarse al servidor: {e}")

# Punto de entrada del script
if __name__ == "__main__":
    iniciar_cliente()
