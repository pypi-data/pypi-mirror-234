# Copyright 2020 The TensorFlow Authors. All Rights Reserved.
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
# ==============================================================================
"""Keras mixed precision API.

See [the mixed precision guide](
  https://www.tensorflow.org/guide/tf_keras/mixed_precision) to learn how to
use the API.
"""

from tf_keras.src.mixed_precision.loss_scale_optimizer import LossScaleOptimizer
from tf_keras.src.mixed_precision.policy import Policy
from tf_keras.src.mixed_precision.policy import global_policy
from tf_keras.src.mixed_precision.policy import set_global_policy

