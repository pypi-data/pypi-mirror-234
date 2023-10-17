import unittest

#import pytest

from scoamp.globals import (global_api, set_auth_info, set_endpoint)

class TestGlobals(unittest.TestCase):
    def test_global_api(self):
        ep = 'http://myendpoint.cn'
        set_endpoint(ep)
        self.assertEqual(global_api.endpoint, ep)

        ak = '1111111111'
        sk = '2222222222'
        set_auth_info(ak, sk)
        self.assertEqual(global_api.ak, ak)
        self.assertEqual(global_api.sk, sk)