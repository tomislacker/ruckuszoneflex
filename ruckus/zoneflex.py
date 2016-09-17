import requests
import logging
import re
from lxml import html

log = logging.getLogger(__name__)


class FirmwareVersion(object):
    def __init__(self):
        self._uris = {}
        self._uri_contents = {}

    def forget_all(self):
        """
        Clear cache of parsed DOC trees
        """
        self._uri_contents = {}
        self._uri_trees = {}

    def _get_contents(self, uri_name):
        """
        Fetch contents via requests module
        :param uri_name:
        :return:
        """
        if uri_name not in self._uri_contents:
            # Go fetch it
            pass

        return self._uri_contents[uri_name]

    def _get_tree(self, uri_name):
        """
        Parse via lxml
        :param uri_name:
        :return: lxml tree
        """
        if uri_name not in self._uri_trees:
            self._uri_trees[uri_name] = self._parse_tree(self._get_contents(uri_name))

        return self._uri_trees[uri_name]

    def _get_xpath(self, uri_name, xpath):
        """
        From a try, find some xpath
        :param uri_name:
        :param xpath:
        :return:
        """
        return self._get_tree(uri_name).xpath(xpath)

    def post(self, uri_name, data):
        """
        POST via requests
        :param uri_name:
        :param data:
        :return:
        """


class Firmware_9_6_2_0_13(FirmwareVersion):
    def __init__(self):
        # call parent
        self._uris = {
            'devicename': ['/configuration/device.asp', '/forms/configdevice']
        }

    @property
    def devicename(self):
        fetch_resp = self.zf.session.get(
            self.zf.get_url('/configuration/device.asp')
        )
        print("Fetch Status: {}".format(fetch_resp.status_code))
        print("Fetched {} bytes".format(len(fetch_resp.content)))
        return re.search(r'\$\(\'devicename\'\)\.value=\'(.*)\';', fetch_resp.content).group(1)

    @devicename.setter
    def devicename(self, new_name):
        return self.zf.session.post(
            self.zf.get_url('/forms/configdevice'),
            data={
                'devicename': new_name
            }
        )


class ZoneFlex(object):
    SESSION_COOKIE = 'sid'

    def open_firmware(self, ver):
        # TODO Replace ver to be class-name-save

        # TODO Make this read from `ver`
        fw = Firmware_9_6_2_0_13()
        fw.zf = self
        return fw

    def __init__(self, addr, port=443, proto='https', verify_ssl=False,
            username='super', passwd='sp-admin'):
        self.addr = addr
        self.port = port
        self.proto = proto
        self.ssl_verify = verify_ssl
        self.username = username
        self.passwd = passwd

        self.__session = None

    def login(self):
        # Fetch the index page first to get a cookie
        log.debug("Fetching index")
        resp_index = self.session.get(self.get_url('/'))
        assert resp_index.status_code == 200, \
            "Failed to fetch cookie"

        # Attempt to login
        log.info("Posting login")
        resp = self.session.post(
            self.get_url('/forms/doLogin'),
            data={
                'login_username': self.username,
                'password': self.passwd,
                'x': 0,
                'y': 0
            })
        assert resp.status_code == 200, \
            "Authentication failed"

    @property
    def is_logged_in(self):
        if self.SESSION_COOKIE in self.session.cookies:
            if self.session.cookies[self.SESSION_COOKIE] != '0':
                return True

        return False

    @property
    def session_id(self):
        if not self.is_logged_in:
            return False

        return self.session.cookies[self.SESSION_COOKIE]

    @property
    def session(self):
        if self.__session is None:
            self.__session = requests.Session()
            self.__session.verify = self.ssl_verify

        return self.__session

    def get_url(self, uri):
        return "{proto}://{addr}:{port}{uri}".format(
            proto=self.proto,
            addr=self.addr,
            port=self.port,
            uri=uri)