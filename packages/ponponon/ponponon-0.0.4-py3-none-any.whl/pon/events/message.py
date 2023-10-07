import inspect
from inspect import signature
from typing import (
    Any,
    Callable,
    Dict,
    ForwardRef,
    Type,
    Union,
    cast,
    get_args
)
from loguru import logger
from kombu.transport.pyamqp import Message
from kombu import Queue
from pon.events.hints import Message as PMessage
from pon.events.hints import Property, Header


class MessageEncoder:
    def encode(self, message_body: Union[str, bytes]):
        pass


def evaluate_forwardref(type_: ForwardRef, globalns: Any, localns: Any) -> Any:
    # Even though it is the right signature for python 3.9, mypy complains with
    # `error: Too many arguments for "_evaluate" of "ForwardRef"` hence the cast...
    return cast(Any, type_)._evaluate(globalns, localns, set())


def get_typed_signature(call: Callable[..., Any]) -> inspect.Signature:
    signature = inspect.signature(call)
    globalns = getattr(call, "__globals__", {})
    typed_params = [
        inspect.Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=get_typed_annotation(param, globalns),
        )
        for param in signature.parameters.values()
    ]
    typed_signature = inspect.Signature(typed_params)
    return typed_signature


def get_typed_annotation(param: inspect.Parameter, globalns: Dict[str, Any]) -> Any:
    annotation = param.annotation
    if isinstance(annotation, str):
        annotation = ForwardRef(annotation)
        annotation = evaluate_forwardref(annotation, globalns, globalns)
    return annotation


class MessageConsumer:

    queue: Queue
    service_cls: Type
    consumer_method: Callable

    def __init__(self, queue: Queue, service_cls: Type, consumer_method: Callable) -> None:
        self.queue = queue
        self.service_cls = service_cls
        self.consumer_method = consumer_method

    def handle_message(self, message: Message):
        """
        body 的 type 取决于 message 的 Properties 的 content_type
        content_type:
        - application/json 对应的 type 就是 dict
        """
        # assert isinstance(message.body, bytes)
        typed_signature = get_typed_signature(
            self.consumer_method).parameters.items()

        method_args = [None for _ in range(len(typed_signature))]
        try:
            for index, (parameter_name, parameter) in enumerate(typed_signature):
                if parameter_name == 'self':
                    service = self.service_cls()
                    method_args[index] = service
                if parameter_name == 'data':
                    content_encoding = message.properties.get(
                        'content_encoding', None)
                    if (str in get_args(parameter.annotation)):
                        message_body = message.body.decode(
                            content_encoding or 'utf-8')
                    else:
                        message_body = message.body
                    method_args[index] = message_body
                if parameter.annotation == PMessage:
                    method_args[index] = message

                if isinstance(parameter.default, Property):
                    method_args[index] = message.properties.get(
                        parameter_name, None)

                if isinstance(parameter.default, Header):
                    header_value = message.headers.get(parameter_name, None)
                    if header_value and (int in get_args(parameter.annotation)):
                        header_value = int(header_value)
                    method_args[index] = header_value

            self.consumer_method(*method_args)
        except Exception as error:
            logger.exception(error)
            if not message.acknowledged:
                message.reject()
        else:
            if not message.acknowledged:
                message.ack()
