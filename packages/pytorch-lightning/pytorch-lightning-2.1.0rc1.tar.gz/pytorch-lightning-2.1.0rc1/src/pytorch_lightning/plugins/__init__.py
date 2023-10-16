from typing import Union

from lightning_fabric.plugins import CheckpointIO, ClusterEnvironment, TorchCheckpointIO, XLACheckpointIO
from pytorch_lightning.plugins.io.async_plugin import AsyncCheckpointIO
from pytorch_lightning.plugins.layer_sync import LayerSync, TorchSyncBatchNorm
from pytorch_lightning.plugins.precision.amp import MixedPrecisionPlugin
from pytorch_lightning.plugins.precision.bitsandbytes import BitsandbytesPrecisionPlugin
from pytorch_lightning.plugins.precision.deepspeed import DeepSpeedPrecisionPlugin
from pytorch_lightning.plugins.precision.double import DoublePrecisionPlugin
from pytorch_lightning.plugins.precision.fsdp import FSDPMixedPrecisionPlugin, FSDPPrecisionPlugin
from pytorch_lightning.plugins.precision.half import HalfPrecisionPlugin
from pytorch_lightning.plugins.precision.precision_plugin import PrecisionPlugin
from pytorch_lightning.plugins.precision.transformer_engine import TransformerEnginePrecisionPlugin
from pytorch_lightning.plugins.precision.xla import XLAPrecisionPlugin

PLUGIN = Union[PrecisionPlugin, ClusterEnvironment, CheckpointIO, LayerSync]
PLUGIN_INPUT = Union[PLUGIN, str]

__all__ = [
    "AsyncCheckpointIO",
    "CheckpointIO",
    "TorchCheckpointIO",
    "XLACheckpointIO",
    "BitsandbytesPrecisionPlugin",
    "DeepSpeedPrecisionPlugin",
    "DoublePrecisionPlugin",
    "HalfPrecisionPlugin",
    "MixedPrecisionPlugin",
    "PrecisionPlugin",
    "TransformerEnginePrecisionPlugin",
    "FSDPMixedPrecisionPlugin",
    "FSDPPrecisionPlugin",
    "XLAPrecisionPlugin",
    "LayerSync",
    "TorchSyncBatchNorm",
]
