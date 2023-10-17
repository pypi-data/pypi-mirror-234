"""
An interface for constant property values to define user message properties that have a special
reserved meaning or behaviour.
"""

QUEUE_PARTITION_KEY = "JMSXGroupID"

"""
A standard property key that clients should use if they want to group messages. It is used to
specify a partition queue name, when supported by a PubSub+ messaging broker. Expected value
is UTF-8 encoded up to 255 bytes long string. This constant can be passed as the property
string to any generic property setter on the OutboundMessageBuilder that can take properties from
:py:mod:`message_properties<solace.messaging.config.solace_properties.message_properties>` as a parameter, such as
:py:meth:`with_property()<solace.messaging.publisher.outbound_message.OutboundMessageBuilder.with_property>`.
"""
