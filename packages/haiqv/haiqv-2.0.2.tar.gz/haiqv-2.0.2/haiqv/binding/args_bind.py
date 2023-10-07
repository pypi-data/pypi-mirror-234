import sys
from argparse import ArgumentParser, Namespace

try:
    from argparse import _SubParsersAction
except ImportError:
    _SubParsersAction = type(None)


class ArgBind:
    __log_params = None
    @staticmethod
    def parse_args(self, args=None, namespace=None):        
        result = ArgBind._original_parse_args(self, args, namespace)
        if isinstance(result, Namespace):            
            ArgBind.__log_params(vars(result))
        elif isinstance(result, dict):            
            ArgBind.__log_params(result)
        return result

    @classmethod
    def patch_argparse(cls, fn):
        # make sure we only patch once
        if not sys.modules.get('argparse') or hasattr(sys.modules['argparse'].ArgumentParser, '_parse_args_patched'):
            return
        # mark patched argparse
        sys.modules['argparse'].ArgumentParser._parse_args_patched = True
        cls.__log_params = fn
        # patch argparser
        ArgBind._original_parse_args = sys.modules['argparse'].ArgumentParser.parse_args
        sys.modules['argparse'].ArgumentParser.parse_args = ArgBind.parse_args