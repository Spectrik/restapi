from http import cookies
from http import client
from datetime import datetime, timedelta

class Cookie():
    "Class for creating cookies"

    def create_custom(self, key, value, expires=None, path=None):
        """
        Method for creating custom cookie
        Returns raw HTTP cookie header as a list, [Set-cookie, key=value(s)]
        """

        # Create empty cookie
        cookie = cookies.SimpleCookie()
        cookie[key] = value

        # Add path value
        if path:
            if isinstance(path, str):
                cookie[key]["path"] = path
            else:
                print("Path value for cookie must be an string!")
                return False

        # Add expires value
        if expires:
            if isinstance(expires, int):

                currenttime = datetime.utcnow()
                duration = timedelta(hours=expires)
                expiration = currenttime + duration

                # Format the expiration time
                expiration = '{:%a, %d %b %Y %H:%m:%S GMT}'.format(expiration)
                cookie[key]["expires"] = expiration
            else:
                print("Expire value for cookie must be an integer!")
                return False

        cookie = str(cookie).split(": ")
        return cookie

    def create_login(self):
        """
        Method for creating a login cookie
        Returns raw HTTP cookie header as a list
        """

        # Create a cookie
        cookie = cookies.SimpleCookie()

        # TODO: Make this more sophisticated
        cookie["logged"] = "yes"

        # Reformat the cookie
        # Set-cookie: key=value ---> [Set-cookie, key=value(s)]
        cookie = str(cookie).split(": ")

        return cookie
