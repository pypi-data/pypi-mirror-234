""" pysubyt

.. module:: pysubyt
    :synopsis: python implementation for Semantic Uplifting by Templates.
        Helps to produces triples out of various datasources
    :noindex:

.. moduleauthor:: Marc Portier <marc.portier@gmail.com>

"""
from pysubyt.api import Generator, Settings, Sink, Source
from pysubyt.j2.generator import JinjaBasedGenerator
from pysubyt.sinks import SinkFactory
from pysubyt.sources import SourceFactory

__all__ = [
    "Sink",
    "Source",
    "Settings",
    "Generator",
    "SourceFactory",
    "SinkFactory",
    "JinjaBasedGenerator",
]
