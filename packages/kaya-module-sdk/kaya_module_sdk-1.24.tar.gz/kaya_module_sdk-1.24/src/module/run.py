import inspect
#import pysnooper

from .template import Module


#@pysnooper.snoop()
def inspect_module_main(module):
    main_full_spec = inspect.getfullargspec(module.main)
    annotations = main_full_spec.annotations
    args = annotations.copy()
    del args['return']
    return {
        'args': args,
        'kwargs': main_full_spec.kwonlydefaults,
        'return': main_full_spec.annotations['return'],
    }


#@pysnooper.snoop()
def run(*modules: Module, args=(), kwargs={}) -> dict:
    failures, ok, nok = 0, [], []
    for module in modules:
        module_run = {
            'module': module,
            'main_inspection': inspect_module_main(module),
            'result': module.main(*args, **kwargs),
        }
        if not isinstance(
                module_run['result'], module_run['main_inspection']['return']):
            failures += 1
            nok.append(module_run)
        else:
            ok.append(module_run)
    return {'failures': failures, 'ok': ok, 'nok': nok,}
