class ClientStore:
    __client_ip = None

    @classmethod
    def __init__(cls, client_ip):
        cls.__client_ip = client_ip

    @classmethod
    def ip(cls):
        return cls.__client_ip
