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
import net.kuujo.vertigo.network.Network
import net.kuujo.vertigo.network.Component
import net.kuujo.vertigo.hooks.EventBusHook
import org.vertx.java.platform.impl.JythonVerticleFactory
import org.vertx.java.core.json.JsonObject
from core.javautils import map_to_java
from context import InstanceContext
from input import Input
from grouping import Grouping

class Network(object):
    """
    A Vertigo network.
    """
    def __init__(self, network):
        self._network = network

    @property
    def address(self):
        return self._network.getAddress()

    def get_num_auditors(self):
        """The number of network auditors."""
        return self._network.getNumAuditors()
    
    def set_num_auditors(self, num):
        """The number of network auditors."""
        self._network.setNumAuditors(num)
    
    num_auditors = property(get_num_auditors, set_num_auditors)

    def enable_acking(self):
        """Enables acking on the network."""
        self._network.enableAcking()
        return self

    def disable_acking(self):
        """Disables acking on the network."""
        self._network.disableAcking()
        return self
    
    def set_acking(self, acking):
        """Sets network acking."""
        if acking:
          self._network.enableAcking()
        else:
          self._network.disableAcking()
    
    def get_acking(self):
        """Gets network acking."""
        return self._network.isAckingEnabled()
    
    acking = property(get_acking, set_acking)
    
    def get_ack_timeout(self):
        """Gets the network ack timeout."""
        return self._network.getAckTimeout()
    
    def set_ack_timeout(self, timeout):
        """Sets the network ack timeout."""
        self._network.setAckTimeout(timeout)
    
    ack_timeout = property(get_ack_timeout, set_ack_timeout)
    
    def add_component(self, component):
        """Adds a component to the network."""
        self._network.addComponent(component._component)
        return component

    def add_feeder(self, address, main, config=None, instances=1):
        """Adds a feeder component to the network.
    
        Keyword arguments:
        @param address: The component event bus address.
        @param main: The feeder main or module name.
        @param config: The feeder component configuration.
        @param instances: The number of feeder instances.
    
        @return: A new feeder component definition.
        """
        if main is not None and config is not None:
            return Component(self._network.addFeeder(address, main, map_to_java(config), instances))
        elif main is not None:
            return Component(self._network.addFeeder(address, main, instances))
        elif config is not None:
            return Component(self._network.addFeeder(address, map_to_java(config), instances))
        else:
            return Component(self._network.addFeeder(address).setInstances(instances))

    def add_executor(self, address, main, config=None, instances=1):
        """Adds an executor component to the network.
    
        Keyword arguments:
        @param address: The component event bus address.
        @param main: The executor main or module name.
        @param config: The executor component configuration.
        @param instances: The number of executor instances.
    
        @return: A new executor component definition.
        """
        if main is not None and config is not None:
            return Component(self._network.addExecutor(address, main, map_to_java(config), instances))
        elif main is not None:
            return Component(self._network.addExecutor(address, main, instances))
        elif config is not None:
            return Component(self._network.addExecutor(address, map_to_java(config), instances))
        else:
            return Component(self._network.addExecutor(address).setInstances(instances))

    def add_worker(self, address, main, config=None, instances=1):
        """Adds a worker component to the network.
    
        Keyword arguments:
        @param address: The component event bus address.
        @param main: The worker main or module name.
        @param config: The worker component configuration.
        @param instances: The number of worker instances.
    
        @return: A new worker component definition.
        """
        if main is not None and config is not None:
            return Component(self._network.addWorker(address, main, map_to_java(config), instances))
        elif main is not None:
            return Component(self._network.addWorker(address, main, instances))
        elif config is not None:
            return Component(self._network.addWorker(address, map_to_java(config), instances))
        else:
            return Component(self._network.addWorker(address).setInstances(instances))

class Component(object):
    """
    A network component.
    """
    FEEDER = 'feeder'
    EXECUTOR = 'executor'
    WORKER = 'worker'

    HOOK_START = 'start'
    HOOK_RECEIVE = 'receive'
    HOOK_ACK = 'ack'
    HOOK_FAIL = 'fail'
    HOOK_EMIT = 'emit'
    HOOK_ACKED = 'acked'
    HOOK_FAILED = 'failed'
    HOOK_TIMEOUT = 'timeout'
    HOOK_STOP = 'stop'

    def __init__(self, component):
        self._component = component
        self.__hook = None
    
    @property
    def address(self):
        """The component address."""
        return self._component.getAddress()
    
    @property
    def type(self):
        """The component type, either "module" or "verticle"."""
        return net.kuujo.vertigo.util.Component.serializeType(self._component.getType())
    
    def is_verticle(self):
        """Indicates whether this component is a verticle."""
        return self._component.isVerticle()
    
    def is_module(self):
        """Indicates whether this component is a module."""
        return self._component.isModule()
    
    def get_main(self):
        """Gets the verticle main."""
        return self._component.getMain()
    
    def set_main(self, main):
        """Sets the verticle main."""
        self._component.setMain(main)
    
    main = property(get_main, set_main)
    
    def get_module(self):
        """Gets the module name."""
        return self._component.getModule()
    
    def set_module(self, module):
        """Sets the module name."""
        self._component.setModule(module)
    
    module = property(get_module, set_module)
    
    def set_config(self, config):
        """Sets the component configuration."""
        self._component.setConfig(org.vertx.java.core.json.JsonObject(map_to_java(config)))
    
    def get_config(self):
        """Gets the component configuration."""
        return map_from_java(self._component.getConfig().toMap())
    
    config = property(get_config, set_config)
    
    def get_instances(self):
        """Gets the number of component instances."""
        return self._component.getInstances()
    
    def set_instances(self, instances):
        """Sets the number of component instances."""
        self._component.setInstances(instances)
    
    instances = property(get_instances, set_instances)
    
    def add_input(self, address, stream=None, grouping=None):
        """Adds an input to the component.
    
        Keyword arguments:
        @param address: The input address. This is the event bus address of the component
        from which this component should receive messages via the added input.
        @param stream: The stream from which this input receives messages.
        @param grouping: An input grouping.
    
        @return: A new Input instance.
        """
        if grouping is not None:
            if stream is not None:
                return Input(self._component.addInput(address).groupBy(grouping._grouping).setStream(stream))
            else:
                return Input(self._component.addInput(address).groupBy(grouping._grouping))
        else:
            if stream is not None:
                return Input(self._component.addInput(address).setStream(stream))
            else:
                return Input(self._component.addInput(address))
    
    @property
    def inputs(self):
        """A list of component inputs."""
        iterator = self._component.getInputs().iterator()
        inputs = []
        while iterator.hasNext():
          inputs.append(Input(iterator.next()))
        return inputs

    def add_hook(self, event, handler):
        """Adds a hook to the component.

        This hook implementation adds an event bus based hook to the component.
        Component events are delivered to the handler via the Vert.x event bus.

        Keyword arguments:
        @param event: The event for which to trigger the hook.
        @param handler: The hook handler.
        @return: self
        """
        if self.__hook is None:
            self._component.addHook(net.kuujo.vertigo.hooks.EventBusHook())
            self.__hook = net.kuujo.vertigo.hooks.EventBusHookListener(self._component.getAddress(), org.vertx.java.platform.impl.JythonVerticleFactory.vertx.eventBus())

        if event == self.HOOK_START:
            self.__hook.startHandler(_ContextHandler(handler))
        elif event == self.HOOK_RECEIVE:
            self.__hook.receiveHandler(_MessageIdHandler(handler))
        elif event == self.HOOK_ACK:
            self.__hook.ackHandler(_MessageIdHandler(handler))
        elif event == self.HOOK_FAIL:
            self.__hook.failHandler(_MessageIdHandler(handler))
        elif event == self.HOOK_EMIT:
            self.__hook.emitHandler(_MessageIdHandler(handler))
        elif event == self.HOOK_ACKED:
            self.__hook.ackedHandler(_MessageIdHandler(handler))
        elif event == self.HOOK_FAILED:
            self.__hook.failedHandler(_MessageIdHandler(handler))
        elif event == self.HOOK_TIMEOUT:
            self.__hook.timeoutHandler(_MessageIdHandler(handler))
        elif event == self.HOOK_STOP:
            self.__hook.stopHandler(_ContextHandler(handler))
        return self

    def hook(self, event):
        """Decorator for registering a component hook.

        Keyword arguments:
        @param event: The hook event.
        """
        def add_hook(handler):
            self.add_hook(event, handler)
            return handler
        return add_hook

class _ContextHandler(org.vertx.java.core.Handler):
    """A hook context handler."""
    def __init__(self, handler):
        self._handler = handler

    def handle(self, jcontext):
        self._handler(InstanceContext(jcontext))

class _MessageIdHandler(org.vertx.java.core.Handler):
    """A message ID handler."""
    def __init__(self, handler):
        self._handler = handler

    def handle(self, messageid):
        self._handler(messageid.correlationId())
