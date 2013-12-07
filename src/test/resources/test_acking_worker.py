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
from test import Assert
import vertigo

@vertigo.worker.message_handler
def message_handler(message, worker):
    Assert.not_null(message)
    Assert.not_null(message.id)
    Assert.not_null(message.body)
    Assert.equals('test', message.tag)
    worker.emit(message.body, parent=message)
    worker.ack(message)
