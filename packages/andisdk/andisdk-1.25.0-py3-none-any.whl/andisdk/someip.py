# Copyright (C) 2023 Technica Engineering GmbH. All rights reserved.
import sys
import typing
from functools import update_wrapper
from typing import Iterable, Callable
from .modules import MessageSomeIP


if not (typing.TYPE_CHECKING or ('sphinx' in sys.modules)):
    import clr
    clr.AddReference('PrimaTestCaseLibrary')
    from PrimaTestCaseLibrary.RestBusSimulation.RestBusSimulationSOMEIP import (
        SomeIpTpSegmenter,
        SomeIpTpAssembler,
    )


def segmentize(someip: MessageSomeIP, max_segment_length: int) -> Iterable[MessageSomeIP]:
    """Segmentize the given SOME/IP message into a list of
    TP segment messages.
    If the payload length <= the given max segment length
    the original message is returned as a one-element list.

    someip: the original message
    max_segment_length: a segment's maximum payload length

    returns: segmented messages as a list
    """
    return SomeIpTpSegmenter.Segmentize(someip, max_segment_length)


SomeIPCallback = Callable[[MessageSomeIP], None]


def reassemble(timeout: float = 1, forward_discarded: bool = True) -> Callable[[SomeIPCallback], SomeIPCallback]:
    """
    This is a Python decorator factory you can add to on_message_received callbacks
    It changes the callback so that it receives reassembled SOME/IP-TP messages

    See https://docs.python.org/3/glossary.html#term-decorator for more inforamtion about Python decorators

    timeout: Maximum time, after which incomplete TP transmissions are discarded
    forward_discarded: Should discarded TP messages be forwarded to the callback or not

    returns: a Python decorator
    """
    def decorator(func):
        assembler = SomeIpTpAssembler(timeout, forward_discarded, func)

        def wrapper(msg):
            assembler.OnReceive(msg)
        return update_wrapper(wrapper, func)
    return decorator
