import sys


class YamlBind:
    __log_params = None
    @staticmethod
    def load(stream, Loader):
        loader = Loader(stream)
        try:
            result = loader.get_single_data()
            YamlBind.__log_params(result)
            return result
        finally:            
            loader.dispose()

    @classmethod
    def patch_load(cls, fn):
        # make sure we only patch once
        if not sys.modules.get('yaml') or hasattr(sys.modules['yaml'], '_load_patched'):
            return
        # mark patched argparse
        sys.modules['yaml']._load_patched = True
        cls.__log_params = fn
        # patch argparser
        YamlBind._load = sys.modules['yaml'].load
        sys.modules['yaml'].load = YamlBind.load
