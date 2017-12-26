from http.server import BaseHTTPRequestHandler
from login import Login
import urllib

class WebApiHandler(BaseHTTPRequestHandler):
    "Handler class for user GET requests"

    def sendMessage(self, message, returncode, headers=None):
        'Send message to client'

        if not isinstance(returncode, (int)):
            print("HTTP return code has to be an integer")
            return False

        if not isinstance(message, (str)):
            print("Message has to be a string")
            return False

        self.send_response(returncode)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><head><title>REST API</title></head>")
        self.wfile.write("<body><p>" + message +"</p>")
        self.wfile.write("</body></html>")
    
    def do_GET(self):
        "Process GET requests"

        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        message = "Hello world!"    

        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))

        return

    def do_POST(self):
        "Process POST requests"

        # List of allowed urls for user to use
        allowedUrls = ["/login"]

        # Is the request path in allowed list?
        if self.path in allowedUrls:

            # User is trying to log in?
            if self.path == "/login":

                # Get POSTed data
                length = int(self.headers['Content-Length'])
                post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))

                # Get credentials
                try:
                    credentials = (post_data["username"][0], post_data["password"][0])
                except KeyError:
                    print("No credentials provided!")
                    return

                # Start the login process
                login = Login(credentials)

                if not login.login():
                    self.sendMessage("Failed to log in!", 403)
        else:
            # GTFO
            self.send_response(403)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("Forbidden, biatch!", "utf8"))

        return
