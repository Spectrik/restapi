from http import cookies

class Cookie():
    "Class for creating cookies"

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
        # Set-cookie: key=value ---> [Set-cookie, key=value]
        cookie = str(cookie).replace(" ", "").split(":")

        return cookie
