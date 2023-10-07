from .process_cmd import ProcessCmd
from .cmd_provider import CmdProvider


class CmdProviderEmulator(CmdProvider):
    def provide(self) -> [ProcessCmd]:
        return [ProcessCmd() for _ in range(10)]
