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
import net.kuujo.vertigo.network.Verticle
import net.kuujo.vertigo.network.Module
import org.vertx.java.core.json.JsonObject
from core.javautils import map_to_java
from input import Input
from grouping import Grouping

class Network(object):
  """
  A Vertigo network.
  """
  def __init__(self, address):
    self._network = net.kuujo.vertigo.network.Network(address)

  @property
  def address(self):
    return self._network.getAddress()

  def get_num_auditors(self):
    return self._network.getNumAuditors()

  def set_num_auditors(self, num):
    self._network.setNumAuditors(num)

  num_auditors = property(get_num_auditors, set_num_auditors)

  def enable_acking(self):
    self._network.enableAcking()
    return self

  def disable_acking(self):
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

  def get_ack_expire(self):
    """Gets the network ack expiration."""
    return self._network.getAckExpire()

  def set_ack_expire(self, expire):
    """Sets the network ack expiration."""
    self._network.setAckExpire(expire)

  ack_expire = property(get_ack_expire, set_ack_expire)

  def get_ack_delay(self):
    """Gets the network ack delay."""
    return self._network.getAckDelay()

  def set_ack_delay(self, delay):
    """Sets the network ack delay."""
    self._network.setAckDelay(delay)

  ack_delay = property(get_ack_delay, set_ack_delay)

  def add_component(self, component):
    """Adds a component to the network."""
    self._network.addComponent(component._component)
    return component

  def add_verticle(self, address, main=None, config=None, instances=1):
    """
    Adds a verticle component to the network.
    """
    if main is not None and config is not None:
      return Verticle(self._network.addVerticle(address, main, map_to_java(config), instances))
    elif main is not None:
      return Verticle(self._network.addVerticle(address, main, instances))
    elif config is not None:
      return Verticle(self._network.addVerticle(address, map_to_java(config), instances))
    else:
      return Verticle(self._network.addVerticle(address).setNumInstances(instances))

  def add_module(self, address, module=None, config=None, instances=1):
    """
    Adds a module component to the network.
    """
    if module is not None and config is not None:
      return Module(self._network.addModule(address, module, map_to_java(config), instances))
    elif module is not None:
      return Module(self._network.addModule(address, module, instances))
    elif config is not None:
      return Module(self._network.addModule(address, map_to_java(config), instances))
    else:
      return Module(self._network.addModule(address).setNumInstances(instances))

  @property
  def components(self):
    components = []
    iterator = self._network.getComponents().iterator()
    while iterator.hasNext():
      info = iterator.next()
      if info.isModule():
        components.append(Module(info))
      elif info.isVerticle():
        components.append(Verticle(info))
    return components

class Component(object):
  """
  A base component.
  """
  def __init__(self, component):
    self._component = component

  @property
  def address(self):
    """The component address."""
    return self._component.getAddress()

  @property
  def type(self):
    """The component type, either "module" or "verticle"."""
    return self._component.getType()

  def set_config(self, config):
    """Sets the component configuration."""
    self._component.setConfig(org.vertx.java.core.json.JsonObject(map_to_java(config)))

  def get_config(self):
    """Gets the component configuration."""
    return map_from_java(self._component.getConfig().toMap())

  config = property(get_config, set_config)

  def get_instances(self):
    """Gets the number of component instances."""
    return self._component.getNumInstances()

  def set_instances(self, instances):
    """Sets the number of component instances."""
    self._component.setNumInstances(instances)

  instances = property(get_instances, set_instances)

  def add_input(self, address, grouping=None, *filters):
    """
    Adds an input to the component.
    """
    if grouping is not None:
      if isinstance(grouping, Grouping):
        return Input(self._component.addInput(address, grouping._grouping, *[filter._filter for filter in filters]))
      else:
        return Input(self._component.addInput(address, grouping._filter, *[filter._filter for filter in filters]))
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

class Verticle(Component):
  """
  A verticle component.
  """
  def get_main(self):
    """Gets the verticle main."""
    return self._component.getMain()

  def set_main(self, main):
    """Sets the verticle main."""
    self._component.setMain(main)

  main = property(get_main, set_main)

class Module(Component):
  """
  A module component.
  """
  def get_module(self):
    """Gets the module name."""
    return self._component.getModule()

  def set_module(self, module):
    """Sets the module name."""
    self._component.setModule(module)

  module = property(get_module, set_module)
