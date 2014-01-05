###############################################################################
##
##  Copyright (C) 2013-2014 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################


import zope
from zope.interface import Interface, Attribute


class ISerializer(Interface):
   """
   Serialization and unserialization.
   """
   isBinary = Attribute("""Flag to indicate if serializer requires a binary clean transport (or if UTF8 transparency is sufficient).""")

   def serialize(self, obj):
      """
      Serialize an object to a byte string.

      :param obj: Object to serialize.
      :type obj: Any serializable type.

      :returns str -- Serialized byte string.
      """

   def unserialize(self, bytes):
      """
      Unserialize an object from a byte string.

      :param bytes: Object to serialize.
      :type bytes: Any serializable type.

      :returns obj -- Any type that can be unserialized.
      """


class IWampMessage(Interface):
   """
   A WAMP message.
   """

   # @classmethod
   # def parse(Klass, wmsg):
   #    """
   #    Verifies and parses an unserialized raw message into an actual WAMP message instance.

   #    :param wmsg: The unserialized raw message.
   #    :type wmsg: list
   #    :returns obj -- An instance of this class.
   #    """

   
   def serialize(serializer):
      """
      Serialize this object into a wire level bytestring representation.

      :param serializer: The wire level serializer to use.
      :type serializer: An instance that implements :class:`autobahn.interfaces.ISerializer`
      """

   def __eq__(other):
      """
      """

   def __ne__(other):
      """
      """

   def __str__():
      """
      Returns text representation of this message.

      :returns str -- Human readable representation (e.g. for logging or debugging purposes).
      """

#   serializer = Attribute("""The WAMP message serializer for this channel.""")



class IMessageChannel(Interface):

   def send(message):
      """
      """

   def isOpen():
      """
      """

   def close():
      """
      """

   def abort():
      """
      """


class IMessageChannelHandler(Interface):

   def onOpen(channel):
      """
      """

   def onMessage(message):
      """
      """

   def onClose():
      """
      """



class IWampDealer(Interface):
   """
   """

   def register(self, endpoint, obj):
      """
      """

   def registerMethod(self, endpoint, obj, method):
      """
      """

   def registerProcedure(self, endpoint, procedure):
      """
      """

   def unregister(self, endpoint):
      """
      """


class IWampBroker(Interface):
   """
   """

   def register(self, topic, prefix = False, publish = True, subscribe = True):
      """
      """

   def unregister(self, topic):
      """
      """


# class IWampPublishOptions(Interface):

#    excludeMe = Attribute("Exclude me, the publisher, from receiving the event (even though I may be subscribed).")



class IWampSession(Interface):
   """
   """

   def call(self, *args):
      """
      """

   def subscribe(self, topic, handler):
      """
      """

   def unsubscribe(self, topic, handler = None):
      """
      """

   def publish(self, topic, event,
               excludeMe = None,
               exclude = None,
               eligible = None,
               discloseMe = None):
      """
      """

   def setDealer(self, dealer = None):
      """
      """

   def setBroker(self, broker = None):
      """
      """



class IPeerRole(Interface):
   """
   Base interface for WAMP peer roles.
   """



class ICaller(IPeerRole):
   """
   Interface for WAMP peers implementing role "Caller".
   """

   def call(procedure, *args, **kwargs):
      """
      Call a remote procedure.

      This will return a deferred/future, that when resolved, provides the actual result.
      If the result is a single positional return value, it'll be returned "as-is". If the
      result contains multiple positional return values or keyword return values,
      the result is wrapped in an instance of :class:`autobahn.wamp2.types.CallResult`.

      If the call fails, the returned deferred/future will be rejected with an instance
      of :class:`autobahn.wamp2.error.CallError`.

      If the Caller and Dealer implementations support cancelling of calls, the call may
      be canceled by canceling the returned deferred/future.

      :param procedure: The URI of the remote procedure to be called, e.g. "com.myapp.hello" or
                        a procedure object specifying details on the call to be performed.
      :type procedure: str or an instance of :class:`autobahn.wamp2.types.Call`

      :returns: obj -- A deferred/future for the call -
                       an instance of :class:`twisted.internet.defer.Deferred` (when running under Twisted) or
                       an instance of :class:`asyncio.Future` (when running under asyncio).
      """



class ICallee(IPeerRole):
   """
   Interface for WAMP peers implementing role "Callee".
   """



class IPublisher(IPeerRole):
   """
   Interface for WAMP peers implementing role "Publisher".
   """

   def publish(topic, payload, options = None):
      """
      Publish an event to a topic.

      This will return a deferred/future, that when resolved provides the publication ID
      for the published event.

      If the publication fails, the returned deferred/future will be rejected with an instance
      of :class:`autobahn.wamp2.error.ApplicationError`.

      :param topic: The URI of the topic to publish to, e.g. "com.myapp.mytopic1".
      :type topic: str
      :param payload: The payload for the event to be published.
      :type payload: obj
      :param options: Options for publishing.
      :type options: None or an instance of :class:`autobahn.wamp2.types.PublishOptions`

      :returns: obj -- A deferred/future for the publication -
                       an instance of :class:`twisted.internet.defer.Deferred` (when running under Twisted)
                       or an instance of :class:`asyncio.Future` (when running under asyncio).
      """



class ISubscriber(IPeerRole):
   """
   Interface for WAMP peers implementing role "Subscriber".
   """

   def subscribe(topic, options = None):
      """
      Subscribe to a topic to (subsequently) receive events published to that topic.

      This will return a deferred/future, that when resolved provides
      an instance of :class:`autobahn.wamp2.types.Subscription`.

      If the subscription fails, the returned deferred/future will be rejected
      with an instance of :class:`autobahn.wamp2.error.ApplicationError`.

      :param topic: The URI (or URI pattern) of the topic to subscribe to.
      :type topic: str
      :param options: Options for subscribing.
      :type options: An instance of :class:`autobahn.wamp2.types.SubscribeOptions`.

      :returns: obj -- A deferred/future for the subscription -
                       an instance of :class:`twisted.internet.defer.Deferred` (when running under Twisted)
                       or an instance of :class:`asyncio.Future` (when running under asyncio).
      """


   def unsubscribe(subscription):
      """
      Unsubscribe the subscription that was previsouly subscribed.

      After a subscription has been unsubscribed, watchers won't get notified
      any more, and you cannot use the subscription anymore.

      This will return a deferred/future, that when resolved signales
      successful unsubscription.

      If the unsubscription fails, the returned deferred/future will be rejected
      with an instance of :class:`autobahn.wamp2.error.ApplicationError`.

      :param subscription: The subscription to unscribe from.
      :type subscription: An instance of :class:`autobahn.wamp2.types.Subscription`
                          that was previously subscribed.

      :returns: obj -- A deferred/future for the publication -
                       an instance of :class:`twisted.internet.defer.Deferred` (when running under Twisted)
                       or an instance of :class:`asyncio.Future` (when running under asyncio).
      """
