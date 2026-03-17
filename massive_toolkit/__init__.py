"""
Massive for Windows Toolkit - Python automation and utilities

A comprehensive toolkit for working with Massive for Windows files and automation.
"""
from .client import MassiveForClient
from .processor import MassiveForProcessor
from .metadata import MassiveForMetadataReader
from .batch import BatchProcessor
from .exporter import DataExporter

__version__ = "0.1.0"
__author__ = "Open Source Community"

__all__ = [
    "MassiveForClient",
    "MassiveForProcessor",
    "MassiveForMetadataReader",
    "BatchProcessor",
    "DataExporter",
]
