from pathlib import Path
from typing import ByteString, Callable, Dict, Tuple, Union

LoaderResult = Tuple[Union[None, ByteString, str], Dict]

LoaderFunction = Callable[[Path], LoaderResult]
