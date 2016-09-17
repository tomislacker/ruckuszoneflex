# encoding: utf-8
import time
from nose2.tools import such

from ruckus.zoneflex import ZoneFlex

orig_channel_24 = 9
new_channel_24 = 8


with such.A('ZoneFlex Host/IP') as it:
    @it.has_setup
    def setup():
        it.zf = ZoneFlex('192.168.10.125')
        it.fw = None

    @it.should('be logged in')
    def test(case):
        case.assertFalse(it.zf.is_logged_in)
        it.zf.login()
        case.assertTrue(it.zf.is_logged_in)

    with it.having('an acceptable firmware'):
        @it.has_setup
        def setup():
            it.fw = it.zf.open_firmware('9.6.2.0.13')

        @it.should('be on the original channel: ' + str(orig_channel_24))
        def test(case):
            assert it.fw.radio24_channel == orig_channel_24

        @it.should('goto a new channel: ' + str(new_channel_24))
        def test(case):
            it.fw.radio24_channel = new_channel_24
            it.fw.forget_params()
            time.sleep(5)

        @it.should('be on the new channel: ' + str(new_channel_24))
        def test(case):
            assert it.fw.radio24_channel == new_channel_24

        @it.should('go back to original channel: ' + str(orig_channel_24))
        def test(case):
            it.fw.radio24_channel = orig_channel_24
            it.fw.forget_params()
            time.sleep(5)

        @it.should('be back on original channel: ' + str(orig_channel_24))
        def test(case):
            case.assertEquals(it.fw.radio24_channel, orig_channel_24)

it.createTests(globals())