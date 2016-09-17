import requests
import logging
import re

log = logging.getLogger(__name__)


class FirmwareVersion(object):
    def __init__(self):
        self._params = {}


class Firmware_9_6_2_0_13(FirmwareVersion):
    def __init__(self):
        super(Firmware_9_6_2_0_13, self).__init__()

        # call parent
        self._uris = {
            'devicename': ['/configuration/device.asp', '/forms/configdevice']
        }

    @property
    def devicename(self):
        if 'devicename' not in self._params:
            self._params['devicename'] = re.search(
                r'\$\(\'devicename\'\)\.value=\'(.*)\';',
                self.zf.session.get(self.zf.get_url('/configuration/device.asp')).content
            ).group(1)
        return self._params['devicename']

    @devicename.setter
    def devicename(self, new_name):
        resp = self.zf.session.post(
            self.zf.get_url('/forms/configdevice'),
            data={
                'devicename': new_name
            }
        )
        del self._params['devicename']
        assert resp.status_code in [200, 302], \
            "Request failed"
        self._params['devicename'] = new_name

    @property
    def devicelocation(self):
        if 'devicelocation' not in self._params:
            self._params['devicelocation'] = re.search(
                r'\$\(\'devicelocation\'\)\.value=\'(.*)\';',
                self.zf.session.get(self.zf.get_url('/configuration/device.asp')).content
            ).group(1)

        return self._params['devicelocation']

    @devicelocation.setter
    def devicelocation(self, new_loc):
        resp = self.zf.session.post(
            self.zf.get_url('/forms/configdevice'),
            # If updated w/o the devicename, devicename becomes blank
            data={
                'devicename': self.devicename,
                'devicelocation': new_loc
            }
        )
        del self._params['devicelocation']
        assert resp.status_code in [200, 302], \
            "Request failed"
        self._params['devicelocation'] = new_loc

    @property
    def radio24_channel(self):
        if 'radio24_channel' not in self._params:
            self._params['radio24_channel'] = int(re.search(
                r'\$\(\'channel\'\)\.selectedIndex=option_values\(\'channel\'\).indexOf\(\'([0-9]+)\'\);',
                self.zf.session.get(self.zf.get_url('/cWireless.asp?wifi=0&subp=common')).content
            ).group(1))
        return self._params['radio24_channel']

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