from typing import Optional


class ProcessConfiguration:
    num_worker_processes: int
    num_cmd_provider_processes: int

    def __init__(
        self,
        num_worker_processes: Optional[int] = 1,
        num_cmd_provider_processes: Optional[int] = 1,
    ):
        self.num_worker_processes = num_worker_processes
        self.num_cmd_provider_processes = num_cmd_provider_processes
