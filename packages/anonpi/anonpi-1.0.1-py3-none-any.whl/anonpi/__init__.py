"""
anonpi: Python Module for Calling Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The "anonpi" module is a powerful Python package that provides a convenient interface for interacting with calling systems. It simplifies the development of applications that require functionalities such as machine detection, IVR (Interactive Voice Response), DTMF (Dual-Tone Multi-Frequency) handling, recording, playback, and more.
"""

import os
import typing as t
from anonpi.resources import Call, Language, Recording

api_key: str = os.environ.get("ANONPI_API_KEY")
api_base: str = os.environ.get(
    "ANONPI_API_BASE", "https://api.anonpi.co/api/v1/")


__author__ = "EvenueStar"
__version__ = "1.0.1"
__license__ = "MIT"
__name__ = "anonpi"
__annotations__ = {"api_key": api_key, "api_base": api_base,
                   "Call": Call, "Language": Language, "Recording": Recording}
__slots__ = ['api_key', 'api_base', 'Call', 'Language', 'Recording']

def app_info():
    return {
        "name": __name__,
        "version": __version__,
        "author": __author__,
        "license": __license__,
    }
