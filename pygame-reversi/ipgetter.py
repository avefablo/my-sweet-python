from socket import socket, AF_INET, SOCK_STREAM
from urllib import request
from urllib.error import HTTPError, URLError
import re


class Popup:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.phrase = self.make_phrase()

    def get_external_ip(self):
        """
        Get external IP by parsing get-ip.me
        """
        try:
            site = request.urlopen("http://www.get-ip.me")
            site = site.read().decode('utf-8')
            ip_regex = re.compile(r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)')
            grab = re.findall(ip_regex, site)
            address = grab[0]
            return address
        except (OSError, HTTPError, URLError) as e:
            return "We can't get your ext. IP ({})".format(e)

    def get_internal_ip(self):
        """
        Get internal IP (local network IP)
        """
        try:
            self.sock.connect(('google.com', 80))
            return self.sock.getsockname()[0]
        except (OSError, HTTPError, URLError) as e:
            return "We can't get your int. IP ({})".format(e)

    def make_phrase(self):
        """
        Concat two IPs into one phrase
        """
        return "Local IP: {}\nGlobal IP: {}".format(self.get_internal_ip(),
                                                    self.get_external_ip())
