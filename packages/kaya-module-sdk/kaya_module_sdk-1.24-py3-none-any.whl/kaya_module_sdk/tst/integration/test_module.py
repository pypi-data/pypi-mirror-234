from kaya_module_sdk.sdk import KIT


class KayaIntegrationTests(KIT):

    package_name = 'dummy'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def setup(cls):
        print('\n[ SETUP ]: Kaya Integration Test Suit (KITS)')

    @classmethod
    def teardown(cls):
        print('\n[ DONE ]: Kaya Integration Test Suit (KITS)')

    def test_add_two(self):
        print('\n[ TEST ]: Good Weather - AddTwo')
        response = self.module(f'{self.package_name}/AddTwo', *[13, 420])
        self.assertTrue(isinstance(response, dict))
        self.assertTrue(response.get('response'))
        self.assertEqual(response['response'], 433)

    def test_subtract_two(self):
        print('\n[ TEST ]: Good Weather - SubtractTwo')
        response = self.module(f'{self.package_name}/SubtractTwo', *[420, 13])
        self.assertTrue(isinstance(response, dict))
        self.assertTrue(response.get('response'))
        self.assertEqual(response['response'], 407)


