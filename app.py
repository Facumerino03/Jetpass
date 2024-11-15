from app import create_app
import logging

logging.basicConfig(level=logging.INFO, format = '%(asctime)s [%(levelname)s] %(message)s')
app = create_app()

if __name__ == "__main__":
    app.run(host = "0.0.0.0", debug = True, port = 5000)
'''
Server Startup
Ref: Book Flask Web Development Page 9
host = "0.0.0.0" makes the server receive requests from any IP
port = 5000 makes reference to the port where the server will run
debug = True makes the server run in debug mode, that is, if there is an error, it will be displayed in the console
'''

