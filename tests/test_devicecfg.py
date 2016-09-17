# encoding: utf-8
from nose2.tools import such

from ruckus.zoneflex import ZoneFlex


with such.A('ZoneFlex Host/IP') as it:
    @it.has_setup
    def setup():
        it.zf = ZoneFlex('192.168.10.125')
        it.fw = None

    @it.should('be logged in')
    def test(case):
        assert not it.zf.is_logged_in
        it.zf.login()
        assert it.zf.is_logged_in

    with it.having('an acceptable firmware'):
        @it.has_setup
        def setup():
            it.fw = it.zf.open_firmware('9.6.2.0.13')

        @it.should('be on channel 8')
        def test(case):
            assert it.fw.radio24_channel == 8

it.createTests(globals())