# encoding: utf-8
from nose2.tools import such

from ruckus.zoneflex import ZoneFlex


with such.A('ZoneFlex Host/IP') as it:
    @it.has_setup
    def setup():
        it.zf = ZoneFlex('192.168.101.25')

    @it.should('be logged in')
    def test(case):
        assert not it.zf.logged_in
        it.zf.login()
        assert it.zf.logged_in

