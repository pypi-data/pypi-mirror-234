import unittest


class TestKayaSDK(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\n[ TestSuit ]: Kaya SDK\n')

    @classmethod
    def tearDownClass(cls):
        print('\n[ DONE ]: Kaya SDK\n')

    # Test cases

    def test_sdk_imports(self):
        print('\n[ TEST ]: Test imports from Kaya SDK...\n')
        try:
            from kaya_module_sdk.sdk import module_run, Module, KTimeSeries, KList
        except Exception as e:
            print('\n[ NOK ]: Importing from SDK failed!\n')
            self.assertTrue(False)
