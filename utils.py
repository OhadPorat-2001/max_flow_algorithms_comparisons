
# for measure time without garbage collector time
import gc
import time


class PrintTime:
    def __init__(self, algorithm: str):
        self.alg_name = algorithm

    def __enter__(self):
        gc.disable()
        self.start_time = time.perf_counter()

    def __exit__(self, exc_type, exc_value, exc_tb):
        duration = time.perf_counter() - self.start_time
        duration_ms = duration * 1000
        gc.enable()
        print(f"{self.alg_name} time: {duration_ms} ms")
