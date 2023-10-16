#  (c) 2021 Copyright, Real-Time Innovations, Inc.  All rights reserved.
#  RTI grants Licensee a license to use, modify, compile, and create derivative
#  works of the Software.  Licensee has the right to distribute object form only
#  for use with RTI products.  The Software is provided "as is", with no warranty
#  of any type, including any warranty for fitness for any purpose. RTI is under
#  no obligation to maintain or support the Software.  RTI shall not be liable for
#  any incidental or consequential damages arising out of the use or inability to
#  use the software.


import rti.connextdds as dds
from . import _util
from . import _util_async
from . import _basic
from typing import Union, Optional, Callable


class Requester(_basic.Requester):
    """A Requester allows sending requests and receiving replies

    :param request_type: The type of the request data. It can be an ``@idl.struct``, an ``@idl.union``, or a dds.DynamicType. (See :ref:`types:Data Types`.)
    :param reply_type: The type of the reply data.
    :param participant: The DomainParticipant that will hold the request writer and reply reader.
    :param service_name: Name that will be used to derive the topic name, defaults to None (rely only on custom topics).
    :param request_topic: Topic object or name that will be used for the request data, must be set if service_name is None, otherwise overrides service_name, defaults to None (use service_name).
    :param reply_topic: Topic object or name that will be used for the reply data, must be set if service_name is None, otherwise overrides service_name, defaults to None (use service_name).
    :param datawriter_qos: QoS object to use for request writer, defaults to None (use default RequestReply QoS).
    :param datareader_qos: QoS object to use for reply reader, defaults to None (use default RequestReply QoS).
    :param publisher: Publisher used to hold request writer, defaults to None (use participant builtin publisher).
    :param subscriber: Subscriber used to hold reply reader, defaults to None (use participant builtin subscriber).
    :param on_reply_available: The callback that handles incoming replies.
    """
    def __init__(
        self,
        request_type: Union[type, dds.DynamicType],
        reply_type: Union[type, dds.DynamicType],
        participant: dds.DomainParticipant,
        service_name: Optional[str] = None,
        request_topic: Union[dds.Topic, dds.DynamicData.Topic, str, object] = None,
        reply_topic: Union[dds.Topic, dds.DynamicData.Topic, str, object] = None,
        datawriter_qos: Optional[dds.DataWriterQos] = None,
        datareader_qos: Optional[dds.DataReaderQos] = None,
        publisher: Optional[dds.Publisher] = None,
        subscriber: Optional[dds.Subscriber] = None,
        on_reply_available: Optional[Callable[[object], object]] = None
    ) -> None:
        super(Requester, self).__init__(
            request_type,
            reply_type,
            participant,
            service_name,
            request_topic,
            reply_topic,
            datawriter_qos,
            datareader_qos,
            publisher,
            subscriber,
            on_reply_available,
        )


    async def wait_for_replies_async(
        self,
        max_wait: dds.Duration,
        min_count: int = 1,
        related_request_id: Optional[dds.SampleIdentity] = None
    ) -> bool:
        """Wait for received replies asynchronously.

        :param max_wait: Maximum time to wait for replies before timing out.
        :param min_count: Minimum number of replies to receive, default 1.
        :param related_request_id: The request id used to correlate replies, default None (receive any replies).
        :return: Boolean indicating whether min_count replies were received within max_wait time.
        """
        if related_request_id is None:
            return _util.wait_for_samples(
                    self._reader,
                    min_count,
                    max_wait,
                    self._waitset,
                    self._any_sample_condition,
                    self._notread_sample_condition)
        else:
            initial_condition = dds.AnyDataReader._create_correlation_condition(
                    self._reader,
                    dds.SampleState.ANY,
                    related_request_id.sequence_number)
            correlation_condition = dds.AnyDataReader._create_correlation_condition(
                    self._reader,
                    dds.SampleState.NOT_READ,
                    related_request_id.sequence_number)
            waitset = dds.WaitSet()
            waitset += correlation_condition
            return await _util_async.wait_for_samples_async(
                    self._reader,
                    min_count, max_wait,
                    waitset, initial_condition,
                    correlation_condition)


class Replier(_basic.Replier):
    """A replier object for handling request-reply interactions with DDS.

    :param request_type: The type of the request data.
    :param reply_type: The type of the reply data.
    :param participant: The DomainParticipant that will hold the reply writer and request reader.
    :param service_name: Name that will be used to derive the topic name, defaults to None (rely only on custom topics).
    :param request_topic: Topic object or name that will be used for the request data, must be set if service_name is None, otherwise overrides service_name, defaults to None (use service_name).
    :param reply_topic: Topic object or name that will be used for the reply data, must be set if service_name is None, otherwise overrides service_name, defaults to None (use service_name).
    :param datawriter_qos: QoS object to use for reply writer, defaults to None (use default RequestReply QoS).
    :param datareader_qos: QoS object to use for request reader, defaults to None (use default RequestReply QoS).
    :param publisher: Publisher used to hold reply writer, defaults to None (use participant builtin publisher).
    :param subscriber: Subscriber used to hold request reader, defaults to None (use participant builtin subscriber).
    :param on_reply_available: The callback that handles incoming requests.
    """
    def __init__(
        self,
        request_type: Union[type, dds.DynamicType],
        reply_type: Union[type, dds.DynamicType],
        participant: dds.DomainParticipant,
        service_name: Optional[str] = None,
        request_topic: Optional[Union[dds.DynamicData.Topic, dds.DynamicData.ContentFilteredTopic, str, object]] = None,
        reply_topic: Optional[Union[dds.DynamicData.Topic, str, object]] = None,
        datawriter_qos: Optional[dds.DataWriterQos] = None,
        datareader_qos: Optional[dds.DataReaderQos] = None,
        publisher: Optional[dds.Publisher] = None,
        subscriber: Optional[dds.Subscriber] = None,
        on_request_available: Optional[Callable[[object], object]] = None
    ) -> None:
        super(Replier, self).__init__(
            request_type,
            reply_type,
            participant,
            service_name,
            request_topic,
            reply_topic,
            datawriter_qos,
            datareader_qos,
            publisher,
            subscriber,
            on_request_available
        )


    async def wait_for_requests_async(
        self,
        max_wait: dds.Duration,
        min_count: Optional[int] = 1
    ) -> bool:
        """Wait asynchronously for a minimum number of requests within a timeout period.

        :param max_wait: Maximum time to wait for requests before timing out. .
        :param min_count: Minimum number of requests to receive, default 1.
        :return: Boolean indicating whether min_count requests were received within max_wait time.
        """
        return await _util_async.wait_for_samples_async(
                self._reader,
                min_count,
                max_wait,
                self._waitset,
                self._any_sample_condition,
                self._notread_sample_condition)
