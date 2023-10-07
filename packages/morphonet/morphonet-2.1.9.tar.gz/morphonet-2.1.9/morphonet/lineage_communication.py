import os, sys
from threading import Thread
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote
from io import BytesIO
import signal

def _get_param(command,p): #Return the value of a specific parameter in http query
    params=unquote(str(command.decode('utf-8'))).split("&")
    for par in params:
        k=par.split("=")[0]
        if k==p:
            return par.split("=")[1].replace('%20',' ')
    return ""

class _MorphoLineageServer(Thread):
    def __init__(self, ploti, todo, host="", port=9875):
        Thread.__init__(self)
        self.ploti = ploti
        self.todo = todo
        self.host = host
        self.port = port
        self.server_address = (self.host, self.port)
        self.available = threading.Event()  # For Post Waiting function
        self.lock = threading.Event()
        self.lock.set()

    def run(self):  # START FUNCTION
        if self.todo == "send":
            handler = _MorphoLineageSendHandler(self.ploti, self)
        else:  # recieve
            handler = _MorphoLineageRecieveHandler(self.ploti, self)

        self.httpd = HTTPServer(self.server_address, handler)
        self.httpd.serve_forever()

    def reset(self):
        self.obj = None
        self.cmd = None
        self.available = threading.Event()  # Create a new watiing process for the next post request
        self.lock.set()  # Free the possibility to have a new command

    def wait(self):  # Wait free request to plot (endd of others requests)
        self.lock.wait()

    def post(self, cmd, obj):  # Prepare a command to post
        self.lock = threading.Event()  # LOCK THE OTHER COMMAND
        self.available.set()
        self.cmd = cmd
        self.obj = obj

    def stop(self):
        self.lock.set()
        self.available.set()
        self.httpd.shutdown()

class _MorphoLineageSendHandler(BaseHTTPRequestHandler):

    def __init__(self, ploti, ms):
        self.ploti = ploti
        self.ms = ms

    def __call__(self, *args, **kwargs):  # Handle a request
        super().__init__(*args, **kwargs)

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")  # To accept request from morphonet
        self.end_headers()

    def do_GET(self):  # NOT USED
        print("get send")
        self._set_headers()
        self.wfile.write(b'OK')

    def do_POST(self):
        print("POST send")
        self.ms.available.wait()  # Wait the commnand available
        self._set_headers()
        content_length = int(self.headers['Content-Length'])
        command = self.rfile.read(content_length)
        response = BytesIO()
        response.write(bytes(self.ms.cmd, 'utf-8'))
        response.write(b';')  # ALWAYS ADD A SEPARATOR
        if self.ms.obj is not None:
            response.write(bytes(self.ms.obj, 'utf-8'))
        self.wfile.write(response.getvalue())
        self.ms.cmd = ""
        self.ms.obj = None
        self.ms.reset()  # FREE FOR OTHERS COMMAND

    def log_message(self, format, *args):
        return


class _MorphoLineageRecieveHandler(BaseHTTPRequestHandler):

    def __init__(self, ploti, ms):
        self.ploti = ploti
        self.ms = ms

    def __call__(self, *args, **kwargs):  # Handle a request
        super().__init__(*args, **kwargs)

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")  # To accept request from morphonet
        self.end_headers()

    def do_GET(self):  # NOT USED
        print("GET recieve")
        #"get received command")
        self._set_headers()
        self.wfile.write(b'OK')

    def do_POST(self):
        print("POST recieve")
        self._set_headers()
        response = BytesIO()  # Read
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        command = self.rfile.read(content_length)
        action = _get_param(command, "action")
        current_time = int(_get_param(command, "time"))
        objects = _get_param(command, "data")
        print("Received action : "+str(action))
        if action == "lineage_info":
            self.ploti.send_lineage(objects)
        elif action == "select_cells":
            self.ploti.send_select_cells(objects)
        elif action == "send_times":
            self.ploti.send_times(objects)
        elif action == "load_info":
            self.ploti.send_info(objects)
        elif action == "load_color":
            self.ploti.send_color(objects)
        else:
            print("else")

        response.write(bytes("DONE", 'utf-8'))
        self.wfile.write(response.getvalue())

    def log_message(self, format, *args):
        return


class LineageMediator:  # Main function to initalize the plot mode
    """LineageMediator data onto the 3D viewer of the MorphoNet Window.

    Parameters (mostly for debuging )
    ----------
    log : bool
        keep the log
    start_browser : bool
        automatically start the browser when plot initliaze
    port : int
        port number to communicate with the MorphoNet Window.

    Returns
    -------
    MorphoPlot
        return an object of morphonet which will allow you to send data to the MorphoNet Window.


    Examples
    --------
    >>> import morphonet
    >>> mn=morphonet.LineageMediator()

    """

    def __init__(self, port_send_lineage=9800,port_send_morphonet=9801,port_receive_lineage=9802,port_receive_morphonet=9803):
        self.setup_mediator(port_send_lineage=port_send_lineage,port_send_morphonet=port_send_morphonet,port_receive_lineage=port_receive_lineage,port_receive_morphonet=port_receive_morphonet)

    def setup_mediator(self,port_send_lineage=9800,port_send_morphonet=9801,port_receive_lineage=9802,port_receive_morphonet=9803):
        self.server_send_lineage = _MorphoLineageServer(self, "send", port=port_send_lineage)  # Instantiate the local MorphoNet server
        self.server_send_lineage.daemon = False
        self.server_send_lineage.start()

        self.server_send_morphonet = _MorphoLineageServer(self, "send", port=port_send_morphonet)  # Instantiate the local MorphoNet server
        self.server_send_morphonet.daemon = False
        self.server_send_morphonet.start()

        self.server_recieve_lineage = _MorphoLineageServer(self, "recieve",
                                            port=port_receive_lineage)  # Instantiate the local MorphoNet server
        self.server_recieve_lineage.daemon = False
        self.server_recieve_lineage.start()

        self.server_recieve_morphonet = _MorphoLineageServer(self, "recieve",
                                            port=port_receive_morphonet)  # Instantiate the local MorphoNet server
        self.server_recieve_morphonet.daemon = False
        self.server_recieve_morphonet.start()
        print("server ok")
        #self.wait_for_servers()

    def send_lineage(self,lineage_string):
        self.send_to_lineage("lineage_info",lineage_string)
    def send_select_cells(self,cell_list):
        self.send_to_morphonet("select_cells",cell_list)
    def send_times(self,time):
        self.send_to_lineage("send_times",time)
    def send_info(self,info):
        self.send_to_lineage("load_info",info)
    def send_color(self,info):
        self.send_to_lineage("load_color",info)
    def send_to_lineage(self, cmd, obj=None):
        """ Send a command to the lineafe window

        Examples
        --------
        >>> mc.send_to_lineage("hello")
        """
        self.server_send_lineage.wait()  # Wait the commnand available
        print("Transfering command : "+str(cmd)+ " to lineage")
        if cmd is not None:
            cmd = cmd.replace(" ", "%20")
        if obj is not None:
            if type(obj) == str:
                obj = obj.replace(" ", "%20")
        self.server_send_lineage.post(cmd, obj)

    def send_to_morphonet(self, cmd, obj=None):
        """ Send a command to the 3D viewer

        Examples
        --------
        >>> mc.send_to_morphonet("hello")
        """
        self.server_send_morphonet.wait()  # Wait the commnand available
        print("Transfering command : " + str(cmd) + " to morphonet")
        if cmd is not None:
            cmd = cmd.replace(" ", "%20")
        if obj is not None:
            if type(obj) == str:
                obj = obj.replace(" ", "%20")
        self.server_send_morphonet.post(cmd, obj)

    def wait_for_servers(self):
        if self.server_send_morphonet is not None:
            self.server_send_morphonet.join()
        if self.server_recieve_morphonet is not None:
            self.server_recieve_morphonet.join()
        if self.server_send_lineage is not None:
            self.server_send_lineage.join()
        if self.server_recieve_lineage is not None:
            self.server_recieve_lineage.join()


plt = LineageMediator(port_send_lineage=9800,port_send_morphonet=9801,port_receive_lineage=9802,port_receive_morphonet=9803)