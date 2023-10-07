from .process_cmd import ProcessCmd


class CmdProvider:
    def provide(self) -> [ProcessCmd]:
        raise NotImplementedError()
