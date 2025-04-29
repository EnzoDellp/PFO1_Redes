import socket
import sqlite3
from datetime import datetime
#configuracion inicial TCP/IP
def iniciar_socket(host="localhost",puerto=5000):
    try:
        servidor=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        servidor.bind((host,puerto)) #asociar el socket
        servidor.listen(5) #escucha hasta 5 conexiones simultaneas
        print(f"Servidor escuchando en {host}:{puerto}")
        return servidor
    except OSError as e:
        print(f" Eror al iniciar el servidor :{e}")
        exit(1) 
    # BDD
def iniciar_db(nombre_db="mensajes.db"):
    try:
        conn=sqlite3.connect(nombre_db)
        cursor=conn.cursor()
        #tabla
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            );
        """)
        conn.commit()
        return conn
    except sqlite3.Error as e:
        print(f"Eror al conectar a la BDD{e}")
        exit(1)

#Guardar mensaje
def guardar_mensaje(db_conn,contenido,ip_cliente):
    cursor=db_conn.cursor()
    fecha_envio=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)"
                   ,(contenido,fecha_envio,ip_cliente))
    db_conn.commit()
    return fecha_envio
#aceptar conexiones
def aceptar_Conexiones(servidor,db_conn):
    while True:
        cliente_socket,direccion=servidor.accept()
        print(f"Conexion establecido con {direccion}")
        try:
            while True:
                mensaje=cliente_socket.recv(1024).decode()
                if not mensaje:
                    break
                print(f"Mensaje recibido de {direccion}:{mensaje}")
                timestamp=guardar_mensaje(db_conn,mensaje,direccion[0])
                respuesta=f"mensaje recibido {timestamp}"
                cliente_socket.send(respuesta.encode())
        except Exception as e:
            print(f"Eror durante la comunicacion con {direccion}:{e}")
        finally:
            cliente_socket.close()
            print(f"conexion cerrada con {direccion}")
if __name__ =="__main__":
    servidor=iniciar_socket()
    db_conn=iniciar_db()
    aceptar_Conexiones(servidor,db_conn)
