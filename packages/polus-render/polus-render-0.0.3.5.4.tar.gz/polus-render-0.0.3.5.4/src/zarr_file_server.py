from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import PurePath
import threading
import os

# Thread local variable with .dir parameter specifying what dir the server should be on
local = threading.local()

class CORSRequestHandler (SimpleHTTPRequestHandler):
    """
    Handler which adds CORS functionality to python's built in http.server
    and uses directory referenced by local.dir

    Args:
        SimpleHTTPRequestHandler (_type_): http.server handler to extend functionality on
    """
    def __init__(self, *args, **kwargs):
        super().__init__(directory=local.dir, *args, **kwargs)

    def end_headers (self):
        """
        Sends CORS line ending the MIME headers
        """
        self.send_header('Access-Control-Allow-Origin', '*')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        """
        Handles OPTION requests as SimpleHTTPRequestHandler is unable to by default
        """
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
    
    def log_message(self, format, *args):
        """
        NOTE - Overrides HTTPServer.log_message()

        Omit output such that jupyter notebooks won't be covered in request info

        Args:
            format (_type_): _description_
        """
        pass

def host_file(path:PurePath, port:int=0)->None:
    """
    Generates a web server which points to a file directory.

    NOTE - runs forever, call in a separate thread to run concurrently.
    Args:
        path (Purepath): File path pointing to a .zarr file
        port (int): port number to plug server into (default is 0 which is 1st available socket found)
    """

    with HTTPServer(("", port), CORSRequestHandler) as httpd:
        # Set dir
        global local
        if os.path.isdir(path):
            local.dir = path
        else:
            local.dir = os.path.dirname(path)

        # Serve files
        httpd.serve_forever()