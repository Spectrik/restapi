from http.server import BaseHTTPRequestHandler
from login import Login
from cookie import Cookie
import urllib

class WebApiHandler(BaseHTTPRequestHandler):
    "Handler class for handling user requests"

    def sendMessage(self, message, returncode, headers=None):
        """
        Send message to client (str)
        HTTP headers (list) = (name of the header, header value)
        Return code (int) = HTTP response code
        """

        if not isinstance(returncode, (int)):
            print("HTTP return code has to be an integer")
            return False

        if not isinstance(message, (str)):
            print("Message has to be a string")
            return False

        # Send HTTP response code
        self.send_response(returncode)

        # Add headers
        self.send_header("Content-type", "text/html")

        if headers:
            for header in headers:
                if header:
                    self.send_header(header[0], header[1])

        self.end_headers()

        # Send message body
        self.wfile.write(bytes(message, "utf8"))

    def do_GET(self):
        "Process GET requests"

        self.allowedUrls = ["/logout"]

        # Is the request path in allowed list?
        if self.path in self.allowedUrls:

            # User is trying to log out?
            if self.path == "/logout":
                login = Login()

                if login.isLoggedIn(self.headers.get("Cookie")):
                    if not login.logout():
                        print("Error: could not log out!")
                        return
                    return

        self.sendMessage("Hello world!", 200)
        return

    def do_POST(self):
        "Process POST requests"

        self.allowedUrls = ["/login"]

        # Create login class
        login = Login()

        # Is the request path in allowed list?
        if self.path in self.allowedUrls:

            # User is trying to log in?
            if self.path == "/login":

                # Get POSTed data
                length = int(self.headers['Content-Length'])
                post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))

                # Get credentials
                try:
                    credentials = (post_data["username"][0], post_data["password"][0])
                except KeyError:
                    self.sendMessage("No credentials provided!", 403)
                    return

                # Start the login process
                login.setCredentials(credentials)
                login.setUserFile("/root/webapi/users.txt")

                # Try to log in
                if not login.login():
                    self.sendMessage("Failed to log in!", 403)
                    return

                logincookie = login.login()
                self.sendMessage("Logged in!", 200, headers=[logincookie])

                return
        else:
            self.sendMessage("Forbidden, biatch!", 403)

        return
