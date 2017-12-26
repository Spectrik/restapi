import os
from cookie import Cookie

class Login():
    "Class for handling user logins"

    def __init__(self):
        "Class constructor"

        # Initialize instance class vars
        self.userfile = None
        self.username = None
        self.password = None

    def setUserFile(self, file):
        "Set the user file DB"

        # Does the file exist?
        try:
            open(file)
            self.userfile = file
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            return False

        # Is the file empty?
        if os.stat(self.userfile).st_size == 0:
            print("Provided user file DB is empty!")
            return False

    def setCredentials(self, credentials):
        "Store user credentials"

        self.username = credentials[0]
        self.password = credentials[1]

    def login(self):
        "Login process. Returns cookie in HTTP header raw text"

        # Checks
        if not self.username or not self.password:
            print("No credentials to use for login!")
            return False

        if not self.userfile:
            print("No user file DB was set!")
            return False

        # Loop through the file with users
        fd = open(self.userfile, "r")

        for user in fd.readlines():
            username, password = user.split(":")

            # If the user is found in the list and the corresponding password is correct
            if username == self.username:
                if password == self.password:
                    usercookie = Cookie().create_login()
                    return usercookie

        return False

    def isLoggedIn(self):
        "Is user logged in?"

        if "HTTP_COOKIE" in os.environ:
            return os.environ["HTTP_COOKIE"]
        else:
            return "HTTP_COOKIE not set!"


    def logout(self):
        "Logout process"
        return False
