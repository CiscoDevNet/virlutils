from .credentials import get_credentials


class VIRLServer(object):
    def __init__(self):
        self._host, self._user, self._passwd, self._config = get_credentials()

    @property
    def host(self):
        return self._host

    @property
    def user(self):
        return self._user

    @property
    def passwd(self):
        return self._passwd

    @property
    def config(self):
        return self._config
