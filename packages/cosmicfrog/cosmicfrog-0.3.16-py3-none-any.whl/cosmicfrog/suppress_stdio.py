import sys
import os

class Suppress_stdio:
    def __enter__(self) -> None:
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        sys.stdout = self._original_stdout
