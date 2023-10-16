# coding=utf-8
# Copyright 2021 DeepMind Technologies Limited.
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

"""Android simulators package."""

from android_env.components.simulators.emulator import emulator_simulator
from android_env.components.simulators.fake import fake_simulator
from android_env.components.simulators.remote import remote_simulator

EmulatorSimulator = emulator_simulator.EmulatorSimulator
FakeSimulator = fake_simulator.FakeSimulator
RemoteSimulator = remote_simulator.RemoteSimulator
