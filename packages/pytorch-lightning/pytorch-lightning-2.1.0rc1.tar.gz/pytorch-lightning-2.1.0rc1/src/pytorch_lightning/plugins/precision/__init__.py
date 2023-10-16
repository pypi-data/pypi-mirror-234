# Copyright The Lightning AI team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from pytorch_lightning.plugins.precision.amp import MixedPrecisionPlugin
from pytorch_lightning.plugins.precision.bitsandbytes import BitsandbytesPrecisionPlugin
from pytorch_lightning.plugins.precision.deepspeed import DeepSpeedPrecisionPlugin
from pytorch_lightning.plugins.precision.double import DoublePrecisionPlugin
from pytorch_lightning.plugins.precision.fsdp import FSDPMixedPrecisionPlugin, FSDPPrecisionPlugin
from pytorch_lightning.plugins.precision.half import HalfPrecisionPlugin
from pytorch_lightning.plugins.precision.precision_plugin import PrecisionPlugin
from pytorch_lightning.plugins.precision.transformer_engine import TransformerEnginePrecisionPlugin
from pytorch_lightning.plugins.precision.xla import XLAPrecisionPlugin

__all__ = [
    "BitsandbytesPrecisionPlugin",
    "DeepSpeedPrecisionPlugin",
    "DoublePrecisionPlugin",
    "FSDPMixedPrecisionPlugin",
    "FSDPPrecisionPlugin",
    "HalfPrecisionPlugin",
    "MixedPrecisionPlugin",
    "PrecisionPlugin",
    "TransformerEnginePrecisionPlugin",
    "XLAPrecisionPlugin",
]
