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
from typing import Union, Optional, Callable


class Requester(_util.RequestReplyBase):
    """A requester object for handling request-reply interactions with DDS.

    :param request_type: The type of the request data.
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
        request_type: Union[dds.DynamicType, type],
        reply_type: Union[dds.DynamicType, type],
        participant: dds.DynamicData,
        service_name: Optional[str] = None,
        request_topic: Union[dds.DynamicData.Topic, str, object] = None,
        reply_topic: Union[dds.DynamicData.Topic, str, object] = None,
        datawriter_qos: Optional[dds.DataWriterQos] = None,
        datareader_qos: Optional[dds.DataReaderQos] = None,
        publisher: Optional[dds.Publisher] = None,
        subscriber: Optional[dds.Subscriber] = None,
        on_reply_available=None     # type: Optional[Callable[[object]]]
    ):
        # type: (...) -> None
        super(Requester, self).__init__(
            'Requester',
            request_type,
            reply_type,
            participant,
            'Request',
            'Reply',
            service_name,
            request_topic,
            reply_topic,
            datawriter_qos,
            datareader_qos,
            publisher,
            subscriber,
            on_reply_available,
            True,
            True
        )

        dds.AnyDataReader._create_correlation_index(self._reader)

    def send_request(
        self,
        request: Union[object, dds.DynamicData],
        params: Optional[dds.WriteParams] = None
    ) -> dds.SampleIdentity:
        """Send a request and return the identity of the request for correlating received replies.

        :param request: The request to send.
        :param params: Parameters used for writing the request.
        :return: The identity of the request.
        """
        if params is None:
            params = dds.WriteParams()
            params.replace_automatic_values = True
        self._writer.write(request, params)
        return params.identity

    def receive_replies(
        self,
        max_wait: dds.Duration,
        min_count: int = 1,
        related_request_id: Optional[dds.SampleIdentity] = None
    ) -> Union[dds.DataReader.LoanedSamples, dds.DynamicData.LoanedSamples, object]:
        """Wait for replies and take them.

        :param max_wait: Maximum time to wait for replies before timing out.
        :param min_count: Minimum number of replies to receive, default 1.
        :param related_request_id: The request id used to correlate replies, default None (receive any replies).
        :raises dds.TimeoutError: Thrown if min_count not received within max_wait.
        :return: A loaned samples object containing the replies.
        """
        if not self.wait_for_replies(max_wait, min_count, related_request_id):
            raise dds.TimeoutError("Timed out waiting for replies")
        else:
            return self.take_replies(related_request_id)

    def take_replies(
            self,
            related_request_id: Optional[dds.SampleIdentity] = None
    ) -> Union[dds.DataReader.LoanedSamples, dds.DynamicData.LoanedSamples]:
        """Take received replies.

        :param related_request_id: The id used to correlate replies to a specific request, default None (take any replies).
        :return: A loaned samples object containing the replies.
        """
        if related_request_id is None:
            return self._reader.take()
        else:
            condition = dds.AnyDataReader._create_correlation_condition(
                self._reader,
                dds.SampleState.ANY,
                related_request_id.sequence_number)
            return self._reader.select().condition(condition).take()

    def read_replies(
        self,
        related_request_id: Optional[dds.SampleIdentity] = None
    ) -> Union[dds.DataReader.LoanedSamples, dds.DynamicData.LoanedSamples]:
        """Read received replies.

        :param related_request_id: The id used to correlate replies to a specific request, default None (read any replies).
        :return: A loaned samples object containing the replies.
        """
        if related_request_id is None:
            return self._reader.read()
        else:
            condition = dds.AnyDataReader._create_correlation_condition(
                self._reader,
                dds.SampleState.ANY,
                related_request_id.sequence_number)
            return self._reader.select().condition(condition).read()


    def wait_for_replies(
        self,
        max_wait: dds.Duration,
        min_count: int = 1,
        related_request_id: Optional[dds.SampleIdentity] = None
    ) -> bool:
        """Wait for received replies.

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
            return _util.wait_for_samples(
                    self._reader,
                    min_count, max_wait,
                    waitset, initial_condition,
                    correlation_condition)


    @property
    def request_datawriter(self) -> Union[dds.DataWriter, dds.DynamicData.DataWriter]:
        """The DataWriter used to send request data.

        :getter: Returns the request DataWriter.
        """
        return self._writer


    @property
    def reply_datareader(self) -> Union[dds.DataReader, dds.DynamicData.DataReader, object]:
        """The DataReader used to receive reply data.

        :getter: Returns the reply DataReader.
        """
        return self._reader


    @property
    def matched_replier_count(self) -> int:
        """The number of discovered matched repliers.

        :getter: Returns the number of matched repliers.
        """
        return _util.match_count(self._reader, self._writer, 'Replier')


    @property
    def on_reply_available(self) -> Optional[Callable[[object], object]]:
        """The listener callback used to process received replies.

        :getter: Returns the callback function.
        :setter: Set the callback function.
        """
        return self._callback


    @on_reply_available.setter
    def on_reply_available(self, callback):
        # type: (Optional[Callable[[Requester]]]) -> None
        if callback is None:
            self._callback = callback
            self._reader.set_listener(None, dds.StatusMask.NONE)
        else:
            self._callback = callback
            listener_cls = _util.get_listener_class(self._reader_type)
            listener = listener_cls(self, callback)
            self._reader.set_listener(listener, dds.StatusMask.DATA_AVAILABLE)


    @classmethod
    def is_related_reply(
        cls,
        request_id: dds.SampleIdentity,
        reply_info: dds.SampleInfo
    ) -> bool:
        """Check a request if against a reply's metadata for correlation.

        :param request_id: The request id used to correlate replies.
        :param reply_info: The reply info used for the correlation check.
        :return: Boolean indicating whether the request and reply are correlated.
        """
        return reply_info.related_original_publication_virtual_sample_identity == request_id


    @classmethod
    def is_final_reply(cls, reply_info: Union[dds.SampleInfo, object]) -> bool:
        """Check a reply is the last of the sequence.

        :param reply_info: The reply info with the flags to check.
        :return: Boolean indicating whether reply is the last for a request.
        """
        if isinstance(reply_info, dds.SampleInfo):
            return dds.SampleFlag.INTERMEDIATE_REPLY_SEQUENCE not in reply_info.flag

        _, info = reply_info
        return dds.SampleFlag.INTERMEDIATE_REPLY_SEQUENCE not in info.flag

class Replier(_util.RequestReplyBase):
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
        request_type: Union[dds.DynamicType, type],
        reply_type: Union[dds.DynamicType, type],
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
            'Replier',
            reply_type,
            request_type,
            participant,
            'Reply',
            'Request',
            service_name,
            reply_topic,
            request_topic,
            datawriter_qos,
            datareader_qos,
            publisher,
            subscriber,
            on_request_available,
            True,
            False
        )

    def send_reply(
        self,
        reply: Union[dds.DynamicData, object],
        param: Union[dds.SampleIdentity, dds.SampleInfo, dds.WriteParams],
        final: bool = True
    ) -> None:
        """Send a reply to a received request.

        :param reply: The reply to send.
        :param param: Parameters used for writing the request.
        :param final: Indicates whether this is the final reply for a specific request, default True.
        :raises dds.InvalidArgumentError: Thrown if param is not a type that can be used for correlation.
        """
        if isinstance(param, dds.SampleIdentity):
            _util.send_with_request_id(self._writer, reply, param, final)
        elif isinstance(param, dds.SampleInfo):
            _util.send_with_request_id(
                    self._writer,
                    reply,
                    param.original_publication_virtual_sample_identity,
                    final)
        elif isinstance(param, dds.WriteParams):
            _util.validate_related_request_id(param.related_sample_identity)
            if final:
                param.flag &= dds.SampleFlag.INTERMEDIATE_REPLY_SEQUENCE.flip()
            else:
                param.flag |= dds.SampleFlag.INTERMEDIATE_REPLY_SEQUENCE
            self._writer.write(reply, param)
        else:
            raise dds.InvalidArgumentError("Invalid param type")


    def receive_requests(
                self,
                max_wait: dds.Duration,
                min_count: int = 1
    ) -> Union[dds.DataReader.LoanedSamples, dds.DynamicData.LoanedSamples]:
        """Receive a minimum number of requests within a timeout period.

        :param max_wait: Maximum time to wait for requests before timing out. .
        :param min_count: Minimum number of requests to receive, default 1.
        :raises dds.TimeoutError: Thrown if min_count not received within max_wait.
        :return: A loaned samples object containing the requests.
        """
        if not self.wait_for_requests(max_wait, min_count):
            raise dds.TimeoutError("Timed out waiting for requests")
        else:
            return self.take_requests()

    def take_requests(self) -> Union[dds.DataReader.LoanedSamples, dds.DynamicData.LoanedSamples]:
        """Take received requests.

        :return: A loaned samples object containing the requests.
        :rtype: Union[dds.DynamicData.LoanedSamples, object]
        """
        return self._reader.take()

    def read_requests(self) -> Union[dds.DataReader.LoanedSamples, dds.DynamicData.LoanedSamples]:
        """Read received requests.

        :return: A loaned samples object containing the requests.
        """
        return self._reader.read()

    def wait_for_requests(
            self,
            max_wait: dds.Duration,
            min_count: int = 1
    ) -> bool:
        """Wait for a minimum number of requests within a timeout period.

        :param max_wait: Maximum time to wait for requests before timing out. .
        :param min_count: Minimum number of requests to receive, default 1.
        :return: Boolean indicating whether min_count requests were received within max_wait time.
        """
        return _util.wait_for_samples(
                self._reader,
                min_count,
                max_wait,
                self._waitset,
                self._any_sample_condition,
                self._notread_sample_condition)


    @property
    def reply_datawriter(self) -> Union[dds.DataWriter, dds.DynamicData.DataWriter]:
        """The DataWriter used to send reply data.

        :getter: Returns the reply DataWriter.
        """
        return self._writer


    @property
    def request_datareader(self) -> Union[dds.DataReader, dds.DynamicData.DataReader]:
        """The DataReader used to receive request data.

        :getter: Returns the request DataReader.
        """
        return self._reader


    @property
    def matched_requester_count(self) -> int:
        """The number of discovered matched requesters.

        :getter: Returns the number of matched requesters.
        """
        return _util.match_count(self._reader, self._writer, 'Requester')


    @property
    def on_request_available(self):
        # type() -> Optional[Callable[[Replier]]]
        """The listener callback used to process received requests.

        :getter: Returns the callback function.
        :setter: Set the callback function.
        :type: Optional[Callable[[Replier]]]
        """
        return self._callback


    @on_request_available.setter
    def on_request_available(self, callback):
        # type(Optional[Callable[[Replier]]]) -> None
        if callback is None:
            self._reader.set_listener(None, dds.StatusMask.NONE)
            self._callback = None
        else:
            self._callback = callback
            listener_cls = _util.get_listener_class(self._reader_type)
            listener = listener_cls(self, callback)
            self._reader.set_listener(listener, dds.StatusMask.DATA_AVAILABLE)


class SimpleReplier(_util.RequestReplyBase):
    """A special replier that uses a user callback to produce one reply per request.

    :param request_type: The type of the request data.
    :param reply_type: The type of the reply data.
    :param participant: The DomainParticipant that will hold the request reader and reply writer.
    :param handler: The callback that handles incoming requests and returns a reply. The callback must have a single argument of type ``request_type`` and must return an instance of type ``reply_type``.
    :param service_name: Name that will be used to derive the topic name, defaults to None (rely only on custom topics).
    :param request_topic: Topic object or name that will be used for the request data, must be set if service_name is None, otherwise overrides service_name, defaults to None (use service_name).
    :param reply_topic: Topic object or name that will be used for the reply data, must be set if service_name is None, otherwise overrides service_name, defaults to None (use service_name).
    :param datawriter_qos: QoS object to use for reply writer, defaults to None (use default RequestReply QoS).
    :param datareader_qos: QoS object to use for request reader, defaults to None (use default RequestReply QoS).
    :param publisher: Publisher used to hold reply writer, defaults to None (use participant builtin publisher).
    :param subscriber: Subscriber used to hold request reader, defaults to None (use participant builtin subscriber).
    """
    @classmethod
    def _create_data_available_callback(cls, handler):
        # type: (Callable[[object], object]) -> Callable[[SimpleReplier]]
        def callback(replier):
            for data, info in replier._reader.take():
                if info.valid:
                    reply = handler(data)
                    _util.send_with_request_id(
                        replier._writer,
                        reply,
                        info.original_publication_virtual_sample_identity,
                        True)

        return callback

    def __init__(
        self,
        request_type: Union[dds.DynamicType, type],
        reply_type: Union[dds.DynamicType, type],
        participant: dds.DomainParticipant,
        handler: Callable[[object], object],
        service_name: Optional[str] = None,
        request_topic: Optional[Union[dds.DynamicData.Topic,
                                      dds.DynamicData.ContentFilteredTopic, str, object]] = None,
        reply_topic: Optional[Union[dds.DynamicData.Topic,
                                    str, object]] = None,
        datawriter_qos: Optional[dds.DataWriterQos] = None,
        datareader_qos: Optional[dds.DataReaderQos] = None,
        publisher: Optional[dds.Publisher] = None,
        subscriber: Optional[dds.Subscriber] = None,
    ) -> None:
        callback = SimpleReplier._create_data_available_callback(handler)

        super(SimpleReplier, self).__init__(
            'Replier',
            reply_type,
            request_type,
            participant,
            'Reply',
            'Request',
            service_name,
            reply_topic,
            request_topic,
            datawriter_qos,
            datareader_qos,
            publisher,
            subscriber,
            callback,
            False,
            False
        )

    @property
    def matched_requester_count(self) -> int:
        """The number of discovered matched requesters.

        :getter: Returns the number of matched requesters.
        """
        return _util.match_count(self._reader, self._writer, 'Requester')
