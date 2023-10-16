#import pysnooper
import unittest
import logging
import json
import re

from subprocess import Popen, PIPE
from abc import ABC, abstractmethod

log = logging.getLogger('')


class KIT(ABC, unittest.TestCase):
    '''
    [ KayaIntegrationTests ]: Morty puts his custom strategy module integration
        tests into subclasses of KIT.
    '''
    integration_tests = []
    runner_host = 'http://kaya_module_runner:8080'

#   @pysnooper.snoop()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.runer_host = kwargs.get('runner_host', 'http://127.0.0.1:8080')
        self.integration_tests = [
            method for method in dir(self) if callable(getattr(self, method))
            and not method.startswith('__') and method.startswith('test_')
        ]

    @classmethod
    @abstractmethod
    def setup(cls):
        pass

    @classmethod
    @abstractmethod
    def teardown(cls):
        pass

    def shell_cmd(self, command, user=None):
        log.debug('Issuing system command: ({})'.format(command))
        if user:
            command = "su {} -c \'{}\'".format(user, command)
        process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        output, errors = process.communicate()
        log.debug('Output: ({}), Errors: ({})'.format(output, errors))
        return  str(output).rstrip('\n'), str(errors).rstrip('\n'), process.returncode

#   @pysnooper.snoop()
    def module(self, module_name, *args, request_type='GET', **kwargs):
        if request_type not in ['GET', 'POST']:
            print(f'[ ERROR ]: Invalid request type! ({request_type})')
            return False
        # [ NOTE ]: Make sure request body uses double quotes!!
        return self.module_request(
            request_type, module_name, {"args": list(args), "kwargs": kwargs}
        )

#   @pysnooper.snoop()
    def module_request(self, verb: str, module_name: str, body: dict):
        cmd = f'curl -X {verb} -H "Content-Type: application/json" -d \'{body}\' '\
            f'{self.runner_host}/{module_name}'
        cmd = cmd.replace("'args'", '"args"').replace("'kwargs'", '"kwargs"')
        run_stdout, run_stderr, run_exit = self.shell_cmd(cmd)
        # Regular expression pattern to match everything between \n{ and $
        pattern = r'\{.*?\{.*?\}.*?\}'
        # Search for the JSON object using the pattern
        match = re.search(pattern, run_stdout)
        response = match.group() if match else '{}'
        result = {
            'response': json.loads(response),
            'exit': run_exit,
        }
        return result

#   @pysnooper.snoop()
    def run_test(self, method_name):
        try:
            test_run = getattr(self, method_name)()
        except Exception as e:
            return False
        return True

#   @pysnooper.snoop()
    def run(self, *args, setup=None, teardown=None, **kwargs):
        test_runs, ok, nok = {}, [], []
        kit_setup=None if not setup else setup()
        try:
            for method_name in self.integration_tests:
                run = self.run_test(method_name)
                if run:
                    print(f'[ OK ]: Integration Test ({method_name})')
                    ok.append(method_name)
                else:
                    print(f'[ NOK ]: Integration Test ({method_name})')
                    nok.append(method_name)
                test_runs.update({method_name: run})
        finally:
            kit_teardown = None if not teardown else teardown()
        return {
            'setup': kit_setup,
            'test-runs': test_runs,
            'teardown': kit_teardown,
            'ok': ok,
            'nok': nok,
        }

# CODE DUMP


