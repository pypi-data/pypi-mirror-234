from multiprocessing import JoinableQueue
from .cmd_provider import CmdProvider


class CmdProviderManager:
    def __init__(self, cmd_provider: CmdProvider, queue: JoinableQueue):
        self._cmd_provider = cmd_provider
        self._queue = queue

    def manage(self) -> None:
        while True:
            [self._queue.put(cmd) for cmd in self._cmd_provider.provide()]
