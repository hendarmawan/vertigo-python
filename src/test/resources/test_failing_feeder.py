# Copyright 2013 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from test import Assert, Test
import vertigo

feeder = vertigo.create_basic_feeder()

def start_handler(error, feeder):
  if error:
    Assert.true(False)
  else:
    def ack_handler(error=None):
      Assert.not_null(error)
      Test.complete()
    feeder.emit({'body': 'Hello world!'}, tag='test', handler=ack_handler)

feeder.start(start_handler)
