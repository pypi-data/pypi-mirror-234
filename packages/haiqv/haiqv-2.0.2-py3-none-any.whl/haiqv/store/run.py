from ..entities.run import Run


class RunStore:
    __instance = None
    __status = False

    def __new__(cls, *args, **kwargs) -> Run:
        assert isinstance(cls.__instance, cls) or (args or kwargs), 'Not Found Active Run'

        if not isinstance(cls.__instance, cls):
            cls.__instance = super().__new__(cls)
            if args:
                assert sum([isinstance(arg, Run) for arg in args]) > 0, f'not matched variable type: Run'
                cls.__instance.run = args[0]
            if kwargs:
                assert 'run' in kwargs.keys(), f'not matched key: run'
                cls.__instance.run = kwargs['run']
            cls.__status = True

        return cls.__instance.run

    @classmethod
    def status(cls):
        return cls.__status

    @classmethod
    def id(cls):
        r_id = None
        try:
            r_id = cls.__instance.run.id
        except:
            pass
        return r_id

    @classmethod
    def flush(cls):
        cls.__status = False
        cls.__instance = None
