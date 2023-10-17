# Copyright (c) 2022-2023 Technica Engineering GmbH. All rights reserved.

"""
andi.e2e
============

Helper module to handle E2E messages.
See documentation for more details :doc:`/Tutorials/e2e`.
"""
import sys
import typing   

if not (typing.TYPE_CHECKING or ('sphinx' in sys.modules)):

  import clr
  clr.AddReference('PrimaTestCaseLibrary')
  from PrimaTestCaseLibrary.Utils import E2EUtils as _E2EUtils

def get_actual_crc(message, e2e = None):
	"""
	Get CRC value from a message based on e2e information.
    Args:
        message(:py:class:`IMessageBase`) : The concerned message.
        e2e(:py:class:`IE2EInformation`) : The e2e information.
    Returns:
        :py:class:`UInt64` actual crc value if coherent message and e2e otherwise 'None'.
    Return Type:
        :py:class:`UInt64`
	"""
	return _E2EUtils.GetActualCrc(message, e2e)
def get_actual_alive(message, e2e = None):
	"""
	Get ALIVE value from a message based on e2e information.
    Args:
        message(:py:class:`IMessageBase`) : The concerned message.
        e2e(:py:class:`IE2EInformation`) : The e2e information.
    Returns:
        :py:class:`UInt64` actual alive value if coherent message and e2e otherwise 'None'.
    Return Type:
        :py:class:`UInt64`
	"""
	return _E2EUtils.GetActualAlive(message, e2e)
def get_expected_crc(message, e2e = None):
	"""
	Calculates CRC value based on a message and e2e information.
    Args:
        message(:py:class:`IMessageBase`) : The concerned message.
        e2e(:py:class:`IE2EInformation`) : The e2e information.
    Returns:
        :py:class:`UInt64` expected crc value if coherent message and e2e otherwise 'None'..
    Return Type:
        :py:class:`UInt64`
	"""
	return _E2EUtils.GetExpectedCrc(message, e2e)
