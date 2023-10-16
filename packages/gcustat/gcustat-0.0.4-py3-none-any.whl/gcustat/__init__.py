"""
The npustat module.
"""

__version__ = "0.0.4"

from .cli import main, print_gcu_stat, loop_gcu_stat
from .core import GCUCardCollection, GCU
from .gcu_smi import GetEntryCardListV1, GetCardStatusWithGcuSmi

__all__ = (
    "__version__",
    "GCUCardCollection", "GCU",
    "GetEntryCardListV1", "GetCardStatusWithGcuSmi",
    "main", "print_gcu_stat", "loop_gcu_stat",
)
