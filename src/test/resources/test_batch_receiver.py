# Copyright 2014 the original author or authors.
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
from vertigo import input
from test import Test, Assert

@input.batch_handler(port='in')
def foo_handler(batch):
    messages = []

    @batch.message_handler
    def message_handler(message):
        messages.append(message)

    @batch.end_handler
    def end_handler():
        Assert.true('foo' in messages)
        Assert.true('bar' in messages)
        Assert.true('baz' in messages)
        Test.complete()
