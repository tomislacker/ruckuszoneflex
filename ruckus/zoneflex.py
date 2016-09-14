import requests

class ZoneFlex(object):
    SESSION_COOKIE = 'sid'

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
        resp_index = self.session.get(self._get_url('/'))
        assert resp_index.status_code == 200, \
            "Failed to fetch cookie"

        # Attempt to login
        resp = self.session.post(
            self._get_url('/forms/doLogin'),
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

    def _get_url(self, uri):
        return "{proto}://{addr}:{port}{uri}".format(
            proto=self.proto,
            addr=self.addr,
            port=self.port,
            uri=uri)
