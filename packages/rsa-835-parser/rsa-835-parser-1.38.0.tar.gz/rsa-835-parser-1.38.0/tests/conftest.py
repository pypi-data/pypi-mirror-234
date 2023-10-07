""" pytest configuration file. """
import os
import sys
import pytest

import rsa_835_parser

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

current_path = os.path.dirname(os.path.realpath(__file__))

@pytest.fixture
def blue_cross_nc_sample():
    """Blue Cross NC sample"""
    path = current_path + "/test_edi_835_files/blue_cross_nc_sample.txt"
    return rsa_835_parser.parse(path)

@pytest.fixture
def emedny_sample():
    """Emedny sample"""
    path = current_path + "/test_edi_835_files/emedny_sample.txt"
    return rsa_835_parser.parse(path)

@pytest.fixture
def united_healthcare_legacy_sample():
    """United Healthcare Legacy sample"""
    path = current_path + "/test_edi_835_files/united_healthcare_legacy_sample.txt"
    return rsa_835_parser.parse(path)

@pytest.fixture
def all_samples():
    """All samples"""
    path = current_path + "/test_edi_835_files"
    return rsa_835_parser.parse(path)
