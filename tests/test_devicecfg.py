# encoding: utf-8
from nose2.tools import such

from ruckus.zoneflex import ZoneFlex


with such.A('ZoneFlex Host/IP') as it:
    @it.has_setup
    def setup():
        it.zf = ZoneFlex('192.168.10.125')

    @it.should('be logged in')
    def test(case):
        assert not it.zf.is_logged_in
        it.zf.login()
        assert it.zf.is_logged_in

it.createTests(globals())