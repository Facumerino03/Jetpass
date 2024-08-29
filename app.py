from app import create_app
import logging

logging.basicConfig(level=logging.INFO, format = '%(asctime)s [%(levelname)s] %(message)s')
app = create_app()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True, port = 5000)
'''
Server Startup
Ref: Book Flask Web Development Page 9
host = "0.0.0.0" hace referencia a que recibe peticiones desde cualquier IP
port = 5000 hace referencia al puerto en el que se ejecutará el servidor
debug = True hace referencia a que se ejecutará en modo debug, es decir, si hay un error, se mostrará en la consola
'''

