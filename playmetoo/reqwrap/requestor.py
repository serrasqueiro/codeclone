#-*- coding: utf-8 -*-
# requestor.py	(c)2022  Henrique Moreira

""" requestor.py - requests (module) wrapper!
"""

# pylint: disable=missing-function-docstring

import requests

ENCODING_LATIN1 = "ISO-8859-1"


class AnyWrap():
    """ Textual Sequence - text file with media elements. """
    def __init__(self, name):
        assert isinstance(name, str)
        self._name = name

    def get_name(self) -> str:
        return self._name

class Requestor(AnyWrap):
    """ Wrapper for requests.get() et al. """
    def __init__(self, url, name=""):
        super().__init__(name)
        self.url = url
        self.req = None
        self._http_code = 0	# invalid
        self.data = ""

    def get(self, **kwargs) -> int:
        """ HTTP GET
        """
        self.req = None
        # allow_redirects = True
        allow_redirects = kwargs.pop("allow_redirects", True)
        assert len(kwargs) <= 0, f"get(): wrong dictionary --> {kwargs}"
        req = requests.get(self.url, allow_redirects=allow_redirects)
        self.req = req
        self._http_code = req.status_code
        self.data = req.content
        return self._http_code

    def pure_get(self) -> int:
        http_code = self.get(allow_redirects=False)
        return 300 if self.is_redirect() else http_code

    def is_redirect(self):
        return 300 <= self._http_code < 400

    def what_redirect(self) -> str:
        """ Returns the redirected string, if any (e.g. HTTP CODE 302) """
        http_code = self.pure_get()
        if http_code != 300:
            return ""
        dir_to = self.req.headers.get("Location")
        if dir_to is None:
            return ""
        return dir_to


# Main script
if __name__ == "__main__":
    print("Please import me!")
