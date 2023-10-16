#
# (c) 2023 Copyright, Real-Time Innovations, Inc.  All rights reserved.
#
# RTI grants Licensee a license to use, modify, compile, and create derivative
# works of the Software solely for use with RTI products.  The Software is
# provided "as is", with no warranty of any type, including any warranty for
# fitness for any purpose. RTI is under no obligation to maintain or support
# the Software.  RTI shall not be liable for any incidental or consequential
# damages arising out of the use or inability to use the software.
#


from abc import ABC, ABCMeta, abstractmethod
import asyncio
import ctypes
import dataclasses
import functools
import inspect
import keyword
import types
import hashlib
from typing import Any, List, Optional, Union, Dict

import rti.connextdds as dds
import rti.types as idl
from rti.idl_impl.sample_interpreter import get_field_factory
from rti.idl_impl import reflection_utils
from rti.rpc import Requester, Replier
import rti.asyncio


def _calculate_hash(name: str) -> int:
    name_hash = hashlib.md5(name.encode('utf-8')).digest()
    hash = ((name_hash[3]) << 24) | ((name_hash[2] << 16) & 0xFF0000) | (
        ((name_hash[1]) << 8) & 0xFF00) | (name_hash[0] & 0xFF)

    # The hash must be a value between int32_min and int32_max
    return ctypes.c_int32(hash).value


def _make_proto_dataclass(cls_name, fields, *, bases=(), namespace=None):
    """This function is the same as dataclasses.make_dataclass, except that it
    doesn't actually apply the dataclass decorator at the end (so it can be
    done by the caller at a later time).
    """

    if namespace is None:
        namespace = {}

    # While we're looking through the field names, validate that they
    # are identifiers, are not keywords, and not duplicates.
    seen = set()
    annotations = {}
    defaults = {}
    for item in fields:
        if isinstance(item, str):
            name = item
            tp = 'typing.Any'
        elif len(item) == 2:
            name, tp, = item
        elif len(item) == 3:
            name, tp, spec = item
            defaults[name] = spec
        else:
            raise TypeError(f'Invalid field: {item!r}')

        if not isinstance(name, str) or not name.isidentifier():
            raise TypeError(f'Field names must be valid identifiers: {name!r}')
        if keyword.iskeyword(name):
            raise TypeError(f'Field names must not be keywords: {name!r}')
        if name in seen:
            raise TypeError(f'Field name duplicated: {name!r}')

        seen.add(name)
        annotations[name] = tp

    # Update 'ns' with the user-supplied namespace plus our calculated values.
    def exec_body_callback(ns):
        ns.update(namespace)
        ns.update(defaults)
        ns['__annotations__'] = annotations

    # We use `types.new_class()` instead of simply `type()` to allow dynamic creation
    # of generic dataclasses.
    return types.new_class(cls_name, bases, {}, exec_body_callback)


def _make_dummy_field():
    field = dataclasses.field(default=0, metadata={"dummy": True})
    return ("dummy", idl.uint8, field)


def _is_dummy_field(field):
    return field.metadata.get("dummy", False)


def _make_in_struct(interface_name: str, operation_name: str, in_parameters: Dict[str, type], parameter_annotations):
    """Creates the python class for the IDL <Service>_<operation>_In struct.

    Given the arguments to an operation such as

    def attack(status: Status, id: int) -> Status: ...

    Create:

    @idl.struct
    class Robot_attack_In:
        status: Status = field(default_factory = Status)
        id: int = 0
    """

    fields = []
    for name, parameter_type in in_parameters.items():
        # skip self parameter
        if name == "self":
            continue
        if reflection_utils.is_primitive_or_enum(parameter_type):
            field = dataclasses.field(default=0)
        else:
            current_annotations = parameter_annotations.get(name, {})
            field = dataclasses.field(
                default_factory=get_field_factory(parameter_type, current_annotations))
        fields.append((name, parameter_type, field))

    if len(fields) == 0:
        fields = [_make_dummy_field()]

    return idl.struct(
        _make_proto_dataclass(f"{interface_name}_{operation_name}_In", fields),
        member_annotations=parameter_annotations)


def _make_out_struct(interface_name: str, operation_name: str, return_type: type, parameter_annotations):
    """Creates the python class for the IDL <Service>_<operation>_Out struct.

    Given the arguments to an operation such as

    def attack(status: Status, id: int) -> Status: ...

    Create:

    @idl.struct
    class Robot_attack_Out:
        return_: Status = field(default_factory = Status)
    """

    if return_type is not None:
        if reflection_utils.is_primitive_or_enum(return_type):
            field = dataclasses.field(default=0)
        else:
            current_annotations = parameter_annotations.get("return_", {})
            field = dataclasses.field(
                default_factory=get_field_factory(return_type, current_annotations))
        fields = [("return_", return_type, field)]
    else:
        fields = [("dummy", idl.uint8, dataclasses.field(default=0))]

    return idl.struct(
        _make_proto_dataclass(
            f"{interface_name}_{operation_name}_Out", fields),
        member_annotations=parameter_annotations)


def _make_result_union(interface_name: str, operation_name: str, out_struct: type, exceptions: List[type]):
    """Creates the python class for the IDL <Service>_<operation>_Result union."""

    fields = [
        ("discriminator", idl.int32, dataclasses.field(default=0)),
        ("value", Union[out_struct, type(None)],
         dataclasses.field(default_factory=out_struct)),
        ("result", out_struct, idl.case(0))
    ]

    fields.extend((f"{exception.__name__}_ex".lower(), exception, idl.case(_calculate_hash(exception.__name__)))
                  for exception in exceptions)

    result = idl.union(_make_proto_dataclass(
        f"{interface_name}_{operation_name}_Result", fields))
    result.out_struct = out_struct
    result.raises = exceptions

    return result


def _get_operations(cls: type):
    """Get the operations of a type as an iterator"""

    for name, member in cls.__dict__.items():
        if not getattr(member, '_is_rpc_operation', False):
            continue

        yield name, member


def _make_in_structs_for_interface(cls: type):
    """Creates the in structs for all operations in an interface."""

    in_structs = {}
    for name, member in _get_operations(cls):
        parameters = {k: v for k,
                      v in member.__annotations__.items() if k != "return"}

        in_structs[_calculate_hash(name)] = (
            name, _make_in_struct(cls.__name__, name, parameters, member._parameter_annotations))

    return in_structs


def _make_result_types_for_interface(cls: type):
    """Creates the result types for all operations in an interface."""

    result_unions = {}
    for name, member in _get_operations(cls):
        return_type = member.__annotations__.get("return", None)
        out_struct = _make_out_struct(
            cls.__name__, name, return_type, member._parameter_annotations)
        result_unions[_calculate_hash(name)] = (name, _make_result_union(
            cls.__name__, name, out_struct, member._raises))

    return result_unions


def _make_call_union(cls: type):
    """Creates the python class for the IDL <Service>_Call union.

    For a class like:

    class Robot:
        def attack(status: Status, id: int) -> Status: ...
        def retreat() -> None: ...

    Creates the following union type:

    @idl.union
    class Robot_Call:

        discriminator: idl.int32 = Robot_retreat_Hash
        value: Union[Robot_attack_In, Robot_retreat_In] = field(default_factory = Robot_retreat_In)

        attack: Robot_attack_In = idl.case(Robot_attack_Hash)
        retreat: Robot_retreat_In = idl.case(Robot_retreat_Hash)
    """

    in_structs = _make_in_structs_for_interface(cls)
    if len(in_structs) == 0:
        raise TypeError(f"{cls.__name__} has no @operation methods")

    fields = [
        ("discriminator", idl.int32, dataclasses.field(default=0)),
        ("value", Union, dataclasses.field(default=None))
    ]

    for name, in_struct in in_structs.values():
        fields.append((name, in_struct, idl.case(_calculate_hash(name))))

    call_union = idl.union(_make_proto_dataclass(
        f"{cls.__name__}_Call", fields))
    call_union.in_structs = in_structs

    return call_union


def _make_return_union(cls: type):
    """Creates the python class for the IDL <Service>_Return union.

    For a class like:

    class Robot:
        def attack(status: Status, id: int) -> Status: ...
        def retreat() -> None: ...

    Creates the following union type:

    @idl.union
    class Robot_Return:

        discriminator: idl.int32 = Robot_retreat_Hash
        value: Union[Robot_attack_Result, Robot_retreat_Result] = field(default_factory = Robot_retreat_Result)

        attack: Robot_attack_Result = idl.case(Robot_attack_Hash)
        retreat: Robot_retreat_Result = idl.case(Robot_retreat_Hash)
    """

    result_unions = _make_result_types_for_interface(cls)

    fields = [
        ("discriminator", idl.int32, dataclasses.field(default=0)),
        ("value", Union, dataclasses.field(default=None))
    ]

    for name, result_union in result_unions.values():
        fields.append((name, result_union, idl.case(_calculate_hash(name))))

    return_union = idl.union(_make_proto_dataclass(
        f"{cls.__name__}_Return", fields))
    return_union.result_unions = result_unions

    return return_union


def service(cls=None, *, type_annotations=[], member_annotations={}):
    """This decorator marks an abstract base class as a remote service interface.

    A class annotated with this decorator can be used to create a Client
    or to define the implementation to be run in a Service.

    The operations that will be remotely callable need to be marked with the
    @operation decorator.
    """

    def wrapper(cls):
        cls.call_type = _make_call_union(cls)
        cls.return_type = _make_return_union(cls)
        return cls

    if cls is None:
        # Decorator used with arguments
        return wrapper
    else:
        # Decorator used without arguments
        return wrapper(cls)


def operation(funcobj=None, *, raises=[], parameter_annotations={}):
    """This decorator marks a method as an remote operation of a service interface.

    It also marks it as an @abc.abstractmethod.

    Only methods marked with this decorator will be callable using an RPC Client
    or an RPC Service.
    """
    def wrapper(funcobj):
        funcobj._is_rpc_operation = True
        funcobj._raises = raises
        funcobj._parameter_annotations = parameter_annotations
        return abstractmethod(funcobj)

    if funcobj is None:
        # Decorator used with arguments
        return wrapper
    else:
        # Decorator used without arguments
        return wrapper(funcobj)


class RemoteUnknownOperationError(Exception):
    """Exception thrown by a client operation when the server indicates that
    the operation is unknown to the server.
    """


class RemoteUnknownExceptionError(Exception):
    """Exception thrown by a client operation when the server operation fails
    with an exception that is not declared in the interface.
    """


class _ClientMeta(ABCMeta):
    """This meta-class injects the code necessary to call RPC operations on a
    DDS domain.
    """

    def __new__(cls, name, bases, attrs):

        # This is the generic implementation of all operations, which will be
        # partially bound below for each @operation method in the class being
        # created.
        async def call_remote_operation_impl(self, method, in_struct, *args, **kwargs):

            # Send request with the operation arguments
            sample = type(self).call_type()
            setattr(sample, method, in_struct(*args, **kwargs))
            request_id = self.requester.send_request(sample)

            # Wait for the reply
            if not await self.requester.wait_for_replies_async(self.max_wait_per_call, 1, request_id):
                self.failed_request_collector.add_failed_request(request_id)
                raise dds.TimeoutError(
                    f"{type(self).__name__}.{method} timed out waiting for reply")

            reply = self.requester.take_replies(request_id)[0]
            if not reply.info.valid:
                raise dds.Error("Invalid return value received")

            if reply.data.discriminator != sample.discriminator:
                if reply.data.discriminator == 0:
                    raise RemoteUnknownOperationError()
                else:
                    raise dds.Error(
                        "Received result for invalid operation")

            out_value = reply.data.value
            if out_value.discriminator == 0:
                out_value = out_value.value
                # Return the received return value or none for operations
                # without a return value
                return getattr(out_value, "return_", None)
            elif out_value.discriminator != -1:
                # Rethrow a remote exception
                raise out_value.value
            else:
                raise RemoteUnknownExceptionError()

        if name == "ClientBase":
            # The metaclass is being applied to ClientBase itself, so we don't
            # do anything. Only ClientBase subclasses need to be modified.
            return super().__new__(cls, name, bases, attrs)

        if len(bases) == 0 or not hasattr(bases[0], "call_type"):
            raise TypeError(
                "An RPC Client must inherit from an @rti.rpc.service class")

        service_cls = bases[0]
        in_structs = service_cls.call_type.in_structs.values()
        for method_name, _ in _get_operations(service_cls):
            in_struct = None
            for search_name, search in in_structs:
                if search_name == method_name:
                    in_struct = search
                    break
            if in_struct is None:
                raise TypeError(
                    f"Method {method_name} is not an operation of {name}")

            # Create a new version of send_request_impl for each method_name:
            attrs[method_name] = functools.partialmethod(
                call_remote_operation_impl, method_name, in_struct)

        return super().__new__(cls, name, bases, attrs)


class FailedRequestCollector:
    def __init__(self, requester: Requester, max_size: int):
        self.requester = requester
        self.max_size = max_size
        self.failed_requests = []

    def add_failed_request(self, request_id: dds.SampleIdentity):
        self.purge()

        self.failed_requests.append(request_id)
        if len(self.failed_requests) >= self.max_size:
            self.failed_requests.pop(0)

    def purge(self):
        for request_id in self.failed_requests:
            samples = self.requester.take_replies(request_id)
            if len(samples) > 0:
                self.failed_requests.remove(request_id)

class ClientBase(ABC, metaclass=_ClientMeta):
    """Base class for RPC clients.

    An actual Client must inherit from a service interface and from this class,
    for example:

    ```
    class RobotClient(Robot, rpc.ClientBase): ...
    ```

    This base class injects an implementation for all the @operation methods
    found in Robot, which uses a Requester to make RPC calls and
    return the values it receives.

    The base class also provides an __init__, close and other methods.
    """

    def __init__(
        self,
        participant: dds.DomainParticipant,
        service_name: str,
        max_wait_per_call: dds.Duration = dds.Duration(10),
        datawriter_qos: Optional[dds.DataWriterQos] = None,
        datareader_qos: Optional[dds.DataReaderQos] = None,
        publisher: Optional[dds.Publisher] = None,
        subscriber: Optional[dds.Subscriber] = None
    ) -> None:
        """Creates the DDS entities needed by this client using the given
        participant and service name.

        The ``max_wait_per_call`` is an optional argument that allows configuring
        how much a client will wait for a return value before timing out. The
        default is 10 seconds. Note that the tasks returned by client operations
        can also be cancelled by the application, so a large maximum wait
        (even ``dds.Duration.infinite``) can also be set.

        The rest of optional arguments are used to create the underlying
        ``Requester``.
        """
        self.requester = Requester(
            type(self).call_type,
            type(self).return_type,
            participant=participant,
            service_name=service_name,
            datawriter_qos=datawriter_qos,
            datareader_qos=datareader_qos,
            publisher=publisher,
            subscriber=subscriber)
        self.max_wait_per_call = max_wait_per_call
        self.failed_request_collector = FailedRequestCollector(
            self.requester, 200)

    def close(self):
        """Closes the DDS entities used by this client."""
        self.requester.close()

    @property
    def matched_service_count(self) -> int:
        """The number of RPC services that match this client."""
        return self.requester.matched_replier_count


def _create_return_reply(cls: type, operation_id: int, operation_result: Any, is_exception: bool = False):
    """Creates a reply for a given operation id, and return value."""

    return_value = cls.return_type()
    return_value.discriminator = operation_id

    if operation_id != 0:
        result_union = cls.return_type.result_unions[operation_id][1]

        if not is_exception:
            result = result_union(result=result_union.out_struct(
                operation_result or 0))
        else:
            ex_field = f"{type(operation_result).__name__}_ex".lower()
            result = result_union()
            if type(operation_result) in result_union.raises:
                setattr(result, ex_field, operation_result)
            else:
                result.discriminator = -1
                result.value = None
    else:
        result = None

    return_value.value = result

    return return_value


class Service:
    """A service allows running a service_instance in a DDS domain using asyncio.

    The service useses a Replier to receive RPC calls and then dispatches them
    to the service_instance, calling the appropriate method. The value returned
    by the method is then sent back to the remote caller.

    The service runs asynchronously (run method) until the task is cancelled.
    """

    def __init__(
            self,
            service_instance: ABC,
            participant: dds.DomainParticipant,
            service_name: str,
            task_count: int = 4,
            datawriter_qos: Optional[dds.DataWriterQos] = None,
            datareader_qos: Optional[dds.DataReaderQos] = None,
            publisher: Optional[dds.Publisher] = None,
            subscriber: Optional[dds.Subscriber] = None
    ) -> None:
        """Creates a new service for a service_instance in a DDS domain.

        The ``task_count`` is an optional argument that allows setting the number
        of tasks that will be used to process the requests. The default is 4.

        The rest of optional arguments are used to create the underlying
        ``Replier``.
        """

        if not hasattr(service_instance, "call_type"):
            raise TypeError(
                "service_instance is not a @service interface")

        self.service_instance = service_instance
        self.service_interface = type(service_instance)
        self.in_structs = self.service_interface.call_type.in_structs
        self.task_count = task_count
        self.queue = asyncio.Queue(task_count * 4)
        self.replier = Replier(
            request_type=self.service_interface.call_type,
            reply_type=self.service_interface.return_type,
            participant=participant,
            service_name=service_name,
            datawriter_qos=datawriter_qos,
            datareader_qos=datareader_qos,
            publisher=publisher,
            subscriber=subscriber)
        self.running = False

    async def _read_requests(self):
        """Reads requests from the replier and puts them in self.queue for
        _process_requests to process.

        When the queue is full, this method awaits until there is space and
        stops reading data from the DataReader.
        """

        async for request_sample in self.replier.request_datareader.take_async():
            if not request_sample.info.valid:
                continue

            await self.queue.put(request_sample)

    async def _process_requests(self):
        """Retrieves the requests from self.queue, calls the corresponding operation
        on the service_instance and sends the return value as a reply.
        """

        while self.running:
            operation_name = None
            request_sample = await self.queue.get()

            try:
                request = request_sample.data
                operation_id = request.discriminator
                operation = self.in_structs.get(operation_id)
                if operation is not None:
                    operation_name = self.in_structs[operation_id][0]
                    operation = getattr(
                        self.service_interface, operation_name)

                    # Unpack the in_struct dataclass fields in a list
                    operation_parameters = [
                        getattr(request.value, field.name)
                        for field in dataclasses.fields(request.value)
                        if not _is_dummy_field(field)
                    ]

                    try:
                        # Call the operation on the service instance with the
                        # unpacked parameters
                        result = operation(
                            self.service_instance, *operation_parameters)
                        if inspect.isawaitable(result):
                            result = await result

                        # Create an return reply with the value returned by the
                        # operation on the service instance
                        reply = _create_return_reply(
                            self.service_interface, operation_id, result)
                    except Exception as e:
                        # If the operation raises an exception, create a return
                        # reply with the exception
                        reply = _create_return_reply(
                            self.service_interface, operation_id, e, is_exception=True)
                else:
                    reply = _create_return_reply(
                        self.service_interface, operation_id=0, operation_result=None)

                # Send the reply containing the return value or an exception to
                # the client (requester)
                self.replier.send_reply(reply, request_sample.info)

            except Exception as e:
                msg = f"Exception while processing {self.service_interface.__name__}.{operation_name}: {e}" \
                    if operation_name is not None \
                    else f"Exception in {self.service_interface.__name__}: {e}"
                dds.Logger.instance._log_dds_warning(msg)
            finally:
                self.queue.task_done()

    async def run(self, close_on_cancel: bool = False):
        """Starts receiving RPC calls (requests) and processing them.

        This method runs until the task it returns is cancelled.

        If close_on_cancel is True, the service will close the DDS entities when
        the task is canceled. By default it is False, which means you can call
        run() again after a run() task is cancelled.

        Exceptions raised during the execution of the service are logged as
        warnings module and do not stop the execution of the service.
        """
        if self.replier.closed:
            raise dds.AlreadyClosedError()

        self.running = True
        try:

            # Run the task that reads requests and as many tasks to process
            # (call the service_instance methods) as specified by task_count
            await asyncio.gather(
                self._read_requests(),
                *(self._process_requests() for _ in range(self.task_count)))
        except asyncio.CancelledError:
            pass  # Cancellation is the expected way to stop the service
        finally:
            self.running = False
            if close_on_cancel:
                self.close()

    def close(self):
        """Closes the DDS entities used by this service."""

        if self.running:
            raise dds.PreconditionNotMetError(
                "Cannot close a running service. Cancel the run() task first.")

        self.replier.close()

    @property
    def matched_client_count(self) -> int:
        """The number of RPC clients that match this service."""
        return self.replier.matched_requester_count


def get_interface_types(interface: type) -> List[type]:
    """Returns a list of all the IDL types used by this interface (call, return, in, out, result)"""

    types = [interface.call_type, interface.return_type]

    for operation in interface.call_type.in_structs.values():
        types.append(operation[1])

    for operation in interface.return_type.result_unions.values():
        types.append(operation[1])
        types.append(operation[1].out_struct)

    return types


def print_interface_idl_types(interface: type):
    """Prints the IDL types used by this interface (call, return, in, out, result)"""

    for type in get_interface_types(interface):
        print(idl.get_type_support(type).dynamic_type)
