import unittest

from kaya_module_sdk.sdk import Module, module_run


class DummyMortyModule(Module):

    def main(self, *args: int, debug='off', **kwargs) -> float:
        return float(sum(args))


class TestStrategyModule(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('\n[ TestSuit ]: Kaya Module SDK\n')
        cls.dummy_module = DummyMortyModule()

    @classmethod
    def tearDownClass(cls):
        print('\n[ DONE ]: Kaya Module SDK\n')
        del cls.dummy_module

    # Test cases

    def test_run_dummy_module(self):
        print('\n[ TEST ]: Run dummy module...\n{}\n'.format(self.dummy_module))

        test_run = module_run(self.dummy_module, args=(1,2,3,), kwargs={'debug': 'on',})

        self.assertTrue(test_run)
        self.assertTrue(isinstance(test_run, dict))
        self.assertEqual(len(test_run), 3)
        self.assertTrue(isinstance(test_run.get('failures'), int))
        self.assertEqual(test_run['failures'], 0)
        self.assertTrue(isinstance(test_run.get('ok'), list))
        self.assertTrue(isinstance(test_run.get('nok'), list))
        self.assertTrue(test_run['ok'])
        self.assertFalse(test_run['nok'])

        for module_result in test_run['ok']:
            self.assertTrue(isinstance(module_result.get('module'), Module))
            self.assertTrue(isinstance(module_result.get('main_inspection'), dict))
            self.assertEqual(len(module_result['main_inspection']), 3)
            self.assertTrue(isinstance(
                module_result['result'],
                module_result['main_inspection']['return']
            ))
            self.assertTrue(isinstance(module_result['result'], float))
            self.assertTrue(module_result['main_inspection']['args'])
            self.assertTrue(len(module_result['main_inspection']['kwargs']), 1)

