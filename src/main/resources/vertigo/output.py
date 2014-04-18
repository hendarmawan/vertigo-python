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
import org.vertx.java.core.Handler
from core.javautils import map_to_java

class OutputCollector(object):
    """Output collector."""
    def __init__(self, java_obj):
        self.java_obj = java_obj
        self._ports = {}

    def port(self, name):
        """Loads an output port.

        Keyword arguments:
        @param name: The output port name.

        @return: An output port.
        """
        if name not in self._ports:
            self._ports[name] = OutputPort(self.java_obj.port(name))
        return self._ports[name]

    def __getattr__(self, name):
        if self.__dict__.has_key(name):
            return self.__dict__.get(name)
        return OutputPort(self.java_obj.port(name))

class Output(object):
    """Base output."""
    def __init__(self, java_obj):
        self.java_obj = java_obj

    def set_send_queue_max_size(self, max_size):
        """Sets the maximum send queue size for the output."""
        self.java_obj.setSendQueueMaxSize(max_size)
        return self

    def get_send_queue_max_size(self, max_size):
        """Returns the maximum send queue size for the output."""
        return self.java_obj.getSendQueueMaxSize()

    send_queue_max_size = property(get_send_queue_max_size, set_send_queue_max_size)

    def send_queue_full(self):
        """Indicates whether the send queue is full."""
        return self.java_obj.sendQueueFull()

    def drain_handler(self, handler):
        """Sets a drain handler on the output."""
        self.java_obj.drainHandler(DrainHandler(handler))
        return self

    def group(self, name, handler=None):
        """Creates an output group.

        @param name: The name of the group to create.
        @param handler: A handler to be called once the group is created.

        @return: self
        """
        if handler is None:
            def wrap(func):
                self.java_obj.group(name, GroupHandler(func))
            return wrap
        else:
            self.java_obj.group(name, GroupHandler(handler))
        return self

    def send(self, message):
        """Sends a message.

        Keyword arguments:
        @param message: The message to send.

        @return: self
        """
        self.java_obj.send(map_to_java(message))
        return self

class OutputPort(Output):
    """Output port."""

class OutputGroup(Output):
    """Output group."""

class GroupHandler(org.vertx.java.core.Handler):
    def __init__(self, handler):
        self.handler = handler;
    def handle(self, group):
        self.handler(OutputGroup(group))

class DrainHandler(org.vertx.java.core.Handler):
    def __init__(self, handler):
        self.handler = handler;
    def handle(self, nothing):
        self.handler()