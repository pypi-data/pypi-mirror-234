import importlib.metadata

from asyncur.aio import gather, run_async, start_tasks
from asyncur.xls import Path, load_xls, read_excel

__version__ = importlib.metadata.version(Path(__file__).parent.name)
__all__ = (
    "__version__",
    "run_async",
    "gather",
    "start_tasks",
    "load_xls",
    "read_excel",
)
