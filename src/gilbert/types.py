from collections.abc import ByteString, Callable
from pathlib import Path

LoaderResult = tuple[None | ByteString | str, dict]

LoaderFunction = Callable[[Path], LoaderResult]
