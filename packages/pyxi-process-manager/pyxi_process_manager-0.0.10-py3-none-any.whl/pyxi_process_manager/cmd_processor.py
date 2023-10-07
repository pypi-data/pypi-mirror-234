from .process_cmd import ProcessCmd


class CmdProcessor:
    def process(self, cmd: ProcessCmd) -> None:
        raise NotImplementedError()
