import unittest

import crypto_proj


class TestCryptoProject(unittest.TestCase):

    def setUp(self):
        self.proj = crypto_proj.CryptoProject()

    def test_task_1(self):
        m = self.proj.task_1()
        self.assertEqual(m, '0x9d20b02c627f60f82f2fe07b956c3ca')

    def test_task_2(self):
        password, salt = self.proj.task_2()
        self.assertEqual(password, 'friendster')
        self.assertEqual(salt, 'marcus')

    def test_task_3(self):
        d = self.proj.task_3()
        self.assertEqual(d, '0x6567d989205fc01')

    def test_task_4(self):
        d, waldo = self.proj.task_4()
        self.assertEqual(d, '0xb38a5359b6bc7f29a5ea53f6100a214d74f17bf7d5028555cf22bfea02014c2f5bc09abec1e1ada08bb725bf2911ab5e24a94eb0f43b7c1e84ddfa61637670e61e644b7ea626ccfcf5c099671bb58916e4a89f8549a8a416f480b69b1a113882f01f7b8c736ebbf407d2fd6e24c43cd3bc461e7840254ebe5789d7e25966ff61')
        self.assertEqual(waldo, 'be729fbeb59825c8cc22fe7255b71e5123f320cdb65987a197884b98')

    def test_task_5(self):
        msg = self.proj.task_5()
        self.assertEqual(msg, 'bdornier3, excuse me. I believe you have my stapler.')


if __name__ == '__main__':
    unittest.main()
