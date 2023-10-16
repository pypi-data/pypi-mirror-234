#import pysnooper
import importlib
import os
import sys
import inspect


#@pysnooper.snoop()
def run(package: str, test_dir: str):
    files, frame = os.listdir(test_dir), inspect.currentframe()
    module = inspect.getmodule(frame)
    sanitized_dir = test_dir.replace('/', '.').strip('.')
    runs = {}
    for file_name in files:
        if not file_name.endswith('.py') or file_name == '__init__.py':
            continue
        # Removes the .py extension
        module_name = file_name[:-3]
        module_path = f'{package}.{sanitized_dir}.{module_name}'
        module = importlib.import_module(module_path)
        for attr_name in dir(module):
            if attr_name in ('ABC', 'KIT'):
                continue
            attribute = getattr(module, attr_name)
            # Check attribute is a class
            if not isinstance(attribute, type):
                continue
            # Check if its a test class (e.g. has a run method)
            if hasattr(attribute, 'run') and callable(attribute.run):
                # Instantiates test calss
                instance = attribute()
                # Run all integration tests in specified Docker container
                run = instance.run(
                    setup=instance.setup, teardown=instance.teardown
                )
                runs.update({attr_name: run})
    return runs

