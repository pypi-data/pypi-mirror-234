from threading import Thread
import threading

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote
from io import BytesIO
from morphonet import tools
from morphonet.tools import _get_param, printv
# ****************************************************************** MORPHONET SERVER


class _MorphoServer(Thread):
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
            handler = _MorphoSendHandler(self.ploti, self)
        else:  # recieve
            handler = _MorphoRecieveHandler(self.ploti, self)

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
        self.httpd.server_close()


class _MorphoSendHandler(BaseHTTPRequestHandler):

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
        self._set_headers()
        self.wfile.write(b'OK')

    def do_POST(self):
        self.ms.available.wait()  # Wait the commnand available
        self._set_headers()
        content_length = int(self.headers['Content-Length'])
        command = self.rfile.read(content_length)
        response = BytesIO()
        response.write(bytes(self.ms.cmd, 'utf-8'))
        response.write(b';')  # ALWAYS ADD A SEPARATOR
        if self.ms.obj is not None:
            if self.ms.cmd.find("RAW") == 0 or self.ms.cmd.find("EX") == 0 or self.ms.cmd.find("IC") == 0:
                response.write(self.ms.obj)
            else:
                response.write(bytes(self.ms.obj, 'utf-8'))
        self.wfile.write(response.getvalue())
        self.ms.cmd = ""
        self.ms.obj = None
        self.ms.reset()  # FREE FOR OTHERS COMMAND

    def log_message(self, format, *args):
        return


class _MorphoRecieveHandler(BaseHTTPRequestHandler):

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
        #"get received command")
        self._set_headers()
        self.wfile.write(b'OK')

    def do_POST(self):
        self._set_headers()
        response = BytesIO()  # Read
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        command = self.rfile.read(content_length)
        action = _get_param(command, "action")
        current_time = int(_get_param(command, "time"))
        objects = _get_param(command, "objects").split(";")
        printv("action "+action+ " at "+str(current_time),3)

        #RECUPERER MESH DEFORMATION
        mesh_deform=_get_param(command, "mesh_deform").split(";") #TODO TAO

        if action == "showraw":
            self.ploti.plot_raws(current_time)
        if action == "hideraw":
            self.ploti.hide_raws()
        elif action == "upload":
            self.ploti.upload(objects[0], 2)
        elif action == "cancel":
            self.ploti.cancel()
        elif action=="exit":
            self.ploti.quit_and_exit()
        elif action=="restart":
            self.ploti.restart_plot()
        elif action=="leave":
            #this one has to be i a thread : we cannot shutdown a server while it is used for a request
            t2 = threading.Thread(target=self.ploti.quit)
            t2.start()
        elif action == "get_info_field":
            self.ploti.get_property_field(_get_param(command, "info"))
        elif action == "reload_infos":
            self.ploti.reload_properties()
        elif action == "create_curation":
            self.ploti.annotate(_get_param(command, "info"), _get_param(command, "objects"),
                                   _get_param(command, "value"), _get_param(command, "date"))
        elif action == "delete_curation":
            self.ploti.delete_annotation(_get_param(command, "info"), _get_param(command, "objects"),
                                          _get_param(command, "value"), date=_get_param(command, "date"))
        elif action == "delete_curation_value":
            self.ploti.delete_annotation(_get_param(command, "info"), _get_param(command, "objects"),
                                                      _get_param(command, "value"))
        elif action == "create_info_unity":
            self.ploti.create_property_from_unity(_get_param(command, "name"), _get_param(command, "datatype"),
                                              _get_param(command, "infos"))
        elif action == "delete_info_unity":
            self.ploti.delete_property_from_unity(_get_param(command, "info"))
        elif action == "delete_selection":
            self.ploti.delete_label_from_unity(_get_param(command, "info"), _get_param(command, "selection"))
        elif action == "get_information_full":
            self.ploti.get_property_field(objects[0])
        elif action == "recompute":
            self.ploti.recompute_data()
        elif action == "get_sk_information":
            name=objects[0]
            if name.startswith("SK"):name=name[2:]
            self.ploti.get_regionprop(name)
        else:
            actions = unquote(str(command.decode('utf-8'))).split("&")
            for plug in self.ploti.plugins:
                if plug._cmd() == action:
                    printv("Found Plugin "+plug._cmd(),2)
                    ifo = 0
                    for tf in plug.inputfields:
                        plug._set_inputfield(tf, actions[3 + ifo][actions[3 + ifo].index("=") + 1:])
                        ifo += 1

                    for dd in plug.dropdowns:
                        plug._set_dropdown(dd, actions[3 + ifo][actions[3 + ifo].index("=") + 1:])
                        ifo += 1
                    for cd in plug.coordinates:
                        plug._set_coordinates(cd, actions[3 + ifo][actions[3 + ifo].index("=") + 1:])
                        ifo += 1

                    if tools.verbose<=1:
                        step_before_execution = self.ploti.dataset.step
                        try: #Exectue the coordinate with exception ...
                            if plug._cmd()=="Manual mesh deformation":
                                plug.process(current_time, self.ploti.dataset, objects,mesh_deform)
                            else:
                                plug.process(current_time, self.ploti.dataset, objects)
                        except Exception as e:
                            printv("the plugin had an error ",0)
                            printv("ERROR "+str(e),1)
                            if step_before_execution!=self.ploti.dataset.step:
                                printv("cancel last step "+str(self.ploti.dataset.step),1)
                                self.ploti.dataset.cancel()
                    else: #DEV MODE EXCUDE THE PLUGIN WITHOUT CATCHIG THE ERROR
                        if plug._cmd() == "Manual mesh deformation":
                            plug.process(current_time, self.ploti.dataset, objects, mesh_deform)
                        else:
                            plug.process(current_time, self.ploti.dataset, objects)


        response.write(bytes("DONE", 'utf-8'))
        self.wfile.write(response.getvalue())

    def log_message(self, format, *args):
        return
