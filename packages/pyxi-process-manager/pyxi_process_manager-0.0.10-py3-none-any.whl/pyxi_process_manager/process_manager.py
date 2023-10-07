from multiprocessing import JoinableQueue, Process
from .cmd_provider_manager import CmdProviderManager
from .cmd_processor_manager import CmdProcessorManager
from .process_configuration import ProcessConfiguration


class ProcessManager:
    def __init__(
        self,
        process_configuration: ProcessConfiguration,
        cmd_processor_manager: CmdProcessorManager,
        cmd_provider_manager: CmdProviderManager,
    ):
        self._queue = JoinableQueue()
        self._process_configuration = process_configuration
        self._cmd_processor_manager = cmd_processor_manager
        self._cmd_provider_manager = cmd_provider_manager

    def manage(self):
        providers = []

        for _ in range(self._process_configuration.num_cmd_provider_processes):
            provider = Process(target=self._cmd_provider_manager.manage)
            providers.append(provider)
            provider.start()

        workers = []

        for _ in range(self._process_configuration.num_worker_processes):
            worker = Process(target=self._cmd_processor_manager.manage)
            workers.append(worker)
            worker.start()

        for provider in providers:
            provider.join()

        for _ in range(self._process_configuration.num_worker_processes):
            self._queue.put(None)  # Signal workers to exit

        for worker in workers:
            worker.join()
