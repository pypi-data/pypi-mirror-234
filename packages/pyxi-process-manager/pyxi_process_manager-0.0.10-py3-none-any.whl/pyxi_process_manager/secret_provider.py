from environs import Env


class SecretProvider:
    def __init__(self):
        self._env = Env()
        self._env.read_env()

    def get_secret(self, secret_name: str) -> str:
        return self._env(secret_name)
