import multiprocessing as mp


class ProcessMetadataService:
    def pid(self) -> int:
        current_process = mp.current_process()
        pid = current_process.pid
        return pid
